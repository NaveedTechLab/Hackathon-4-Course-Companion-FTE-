import boto3
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any
import logging
from io import BytesIO
from config import settings

logger = logging.getLogger(__name__)

class CloudflareR2Service:
    """
    Service for interacting with Cloudflare R2 storage
    """

    def __init__(self):
        if not all([
            settings.cloudflare_account_id,
            settings.cloudflare_r2_access_key_id,
            settings.cloudflare_r2_secret_access_key,
            settings.cloudflare_r2_bucket_name
        ]):
            raise ValueError("Cloudflare R2 configuration is incomplete. Please set all required environment variables.")

        # Construct the R2 endpoint URL
        self.endpoint_url = f"https://{settings.cloudflare_account_id}.r2.cloudflarestorage.com"

        # Initialize the S3 client with R2 settings
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=settings.cloudflare_r2_access_key_id,
            aws_secret_access_key=settings.cloudflare_r2_secret_access_key
        )

        self.bucket_name = settings.cloudflare_r2_bucket_name

    def upload_file(self, file_data: bytes, object_key: str, content_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file to Cloudflare R2

        Args:
            file_data: File content as bytes
            object_key: The key (path) to store the file under
            content_type: Optional content type for the file

        Returns:
            Dictionary with upload result information
        """
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type

            # Upload the file
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=file_data,
                **extra_args
            )

            # Generate public URL for the uploaded file
            file_url = f"{self.endpoint_url}/{self.bucket_name}/{object_key}"

            return {
                "success": True,
                "object_key": object_key,
                "file_url": file_url,
                "bucket": self.bucket_name,
                "content_type": content_type
            }

        except ClientError as e:
            logger.error(f"Error uploading file to R2: {e}")
            return {
                "success": False,
                "error": str(e),
                "object_key": object_key
            }

    def download_file(self, object_key: str) -> Optional[bytes]:
        """
        Download a file from Cloudflare R2

        Args:
            object_key: The key (path) of the file to download

        Returns:
            File content as bytes, or None if not found
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=object_key
            )

            return response['Body'].read()

        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.warning(f"File not found in R2: {object_key}")
            else:
                logger.error(f"Error downloading file from R2: {e}")
            return None

    def delete_file(self, object_key: str) -> Dict[str, Any]:
        """
        Delete a file from Cloudflare R2

        Args:
            object_key: The key (path) of the file to delete

        Returns:
            Dictionary with deletion result information
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )

            return {
                "success": True,
                "object_key": object_key,
                "message": "File deleted successfully"
            }

        except ClientError as e:
            logger.error(f"Error deleting file from R2: {e}")
            return {
                "success": False,
                "error": str(e),
                "object_key": object_key
            }

    def file_exists(self, object_key: str) -> bool:
        """
        Check if a file exists in Cloudflare R2

        Args:
            object_key: The key (path) of the file to check

        Returns:
            True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                logger.error(f"Error checking if file exists in R2: {e}")
                return False

    def get_file_metadata(self, object_key: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a file in Cloudflare R2

        Args:
            object_key: The key (path) of the file to get metadata for

        Returns:
            Dictionary with file metadata, or None if not found
        """
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=object_key
            )

            return {
                "content_type": response.get('ContentType'),
                "content_length": response.get('ContentLength'),
                "last_modified": response.get('LastModified'),
                "etag": response.get('ETag').strip('"'),  # Remove quotes from ETag
                "object_key": object_key
            }

        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logger.warning(f"File not found in R2: {object_key}")
            else:
                logger.error(f"Error getting file metadata from R2: {e}")
            return None

    def list_files(self, prefix: str = "", max_keys: int = 1000) -> Dict[str, Any]:
        """
        List files in Cloudflare R2 bucket with optional prefix

        Args:
            prefix: Optional prefix to filter files
            max_keys: Maximum number of keys to return

        Returns:
            Dictionary with list of files and pagination info
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys
            )

            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append({
                        "object_key": obj['Key'],
                        "size": obj['Size'],
                        "last_modified": obj['LastModified'],
                        "etag": obj['ETag'].strip('"')
                    })

            return {
                "success": True,
                "files": files,
                "prefix": prefix,
                "truncated": response.get('IsTruncated', False),
                "key_count": len(files)
            }

        except ClientError as e:
            logger.error(f"Error listing files in R2: {e}")
            return {
                "success": False,
                "error": str(e),
                "files": []
            }

    def generate_presigned_url(self, object_key: str, expiration: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for accessing a file in Cloudflare R2

        Args:
            object_key: The key (path) of the file
            expiration: URL expiration time in seconds (default 1 hour)

        Returns:
            Presigned URL string, or None if error
        """
        try:
            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expiration
            )

            return presigned_url

        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None

    def upload_from_url(self, source_url: str, object_key: str) -> Dict[str, Any]:
        """
        Download file from URL and upload to Cloudflare R2

        Args:
            source_url: URL of the source file to download
            object_key: The key (path) to store the file under

        Returns:
            Dictionary with upload result information
        """
        import requests

        try:
            # Download the file from the source URL
            response = requests.get(source_url)
            response.raise_for_status()

            # Upload to R2
            return self.upload_file(response.content, object_key)

        except Exception as e:
            logger.error(f"Error downloading from URL and uploading to R2: {e}")
            return {
                "success": False,
                "error": str(e),
                "object_key": object_key
            }