import boto3
from botocore.config import Config
import os
from typing import Optional, BinaryIO
from io import BytesIO
from dotenv import load_dotenv

# Load .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

class R2Client:
    """
    Client for interacting with Cloudflare R2 storage
    This is a deterministic client that only stores and retrieves content without any LLM processing
    """

    def __init__(self):
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.access_key_id = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID")
        self.secret_access_key = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
        self.bucket_name = os.getenv("CLOUDFLARE_R2_BUCKET_NAME")

        if not all([self.account_id, self.access_key_id, self.secret_access_key, self.bucket_name]):
            raise ValueError("Missing required R2 configuration environment variables")

        # Configure boto3 client for R2
        self.client = boto3.client(
            's3',
            endpoint_url=f'https://{self.account_id}.r2.cloudflarestorage.com',
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            config=Config(signature_version='s3v4'),
        )

    def upload_content(self, file_data: BinaryIO, object_key: str, content_type: str = "application/octet-stream") -> str:
        """
        Upload content to R2 storage
        """
        try:
            self.client.upload_fileobj(
                file_data,
                self.bucket_name,
                object_key,
                ExtraArgs={'ContentType': content_type}
            )
            return f"https://{self.bucket_name}.{self.account_id}.r2.cloudflarestorage.com/{object_key}"
        except Exception as e:
            raise Exception(f"Failed to upload to R2: {str(e)}")

    def get_content(self, object_key: str) -> Optional[bytes]:
        """
        Retrieve content from R2 storage
        """
        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return response['Body'].read()
        except self.client.exceptions.NoSuchKey:
            return None
        except Exception as e:
            raise Exception(f"Failed to retrieve from R2: {str(e)}")

    def get_presigned_url(self, object_key: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL for content access
        """
        try:
            presigned_url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expiration
            )
            return presigned_url
        except Exception as e:
            raise Exception(f"Failed to generate presigned URL: {str(e)}")

    def delete_content(self, object_key: str) -> bool:
        """
        Delete content from R2 storage
        """
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to delete from R2: {str(e)}")

    def object_exists(self, object_key: str) -> bool:
        """
        Check if an object exists in R2 storage
        """
        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return True
        except self.client.exceptions.NoSuchKey:
            return False
        except Exception:
            return False

# Global R2 client instance
r2_client = R2Client()