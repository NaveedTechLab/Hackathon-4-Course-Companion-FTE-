# Cloudflare R2 Setup Guide for Course Companion FTE

## Overview
This document provides instructions for setting up Cloudflare R2 object storage for the Course Companion FTE project.

## R2 Configuration Steps

### 1. Create R2 Bucket
1. Log in to your Cloudflare dashboard
2. Navigate to R2 Object Storage
3. Click "Create a bucket"
4. Set bucket name to `course-companion-fte` (or your preferred name)
5. Choose location (default is fine for most use cases)
6. Set storage class to "Standard" (recommended for frequently accessed content)

### 2. Generate R2 Credentials
1. In the R2 dashboard, go to "Manage R2 API Tokens"
2. Create a new API token with the following permissions:
   - `r2:write` - for uploading content
   - `r2:read` - for downloading content
   - `r2:delete` - for removing content
3. Copy the Access Key ID and Secret Access Key

### 3. Configure Environment Variables
Update your `.env` file with the following settings:

```env
# Cloudflare R2 Configuration
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_R2_ACCESS_KEY_ID=your_access_key_id
CLOUDFLARE_R2_SECRET_ACCESS_KEY=your_secret_access_key
CLOUDFLARE_R2_BUCKET_NAME=course-companion-fte
```

### 4. Environment Variable Details

- `CLOUDFLARE_ACCOUNT_ID`: Your 32-character Cloudflare account ID (found in Cloudflare dashboard)
- `CLOUDFLARE_R2_ACCESS_KEY_ID`: Your R2 access key ID (generated in R2 dashboard)
- `CLOUDFLARE_R2_SECRET_ACCESS_KEY`: Your R2 secret access key (generated in R2 dashboard)
- `CLOUDFLARE_R2_BUCKET_NAME`: Name of your R2 bucket (e.g., "course-companion-fte")

## Storage Service Features

The `CloudflareR2Service` provides the following functionality:

### File Operations
- `upload_file()`: Upload content to R2
- `download_file()`: Download content from R2
- `delete_file()`: Remove content from R2
- `file_exists()`: Check if a file exists

### Metadata Management
- `get_file_metadata()`: Retrieve file information
- `list_files()`: List files with optional prefix filtering

### Security Features
- `generate_presigned_url()`: Create temporary access URLs
- `upload_from_url()`: Upload content from external URLs

## Integration with Course Companion FTE

### Phase 1 Integration
- Content storage for course materials
- Media files (videos, images, documents)
- Automatic upload/download of learning resources

### Phase 2 Integration
- Premium feature content
- Generated content (synthesis reports, personalized materials)
- Assessment materials and results

### Phase 3 Integration
- Frontend asset delivery
- User-generated content storage
- Dynamic content serving

## Best Practices

### Security
- Never commit API keys to version control
- Use environment variables for all credentials
- Rotate API keys periodically
- Use least-privilege access principles

### Performance
- Use appropriate content types for better caching
- Implement CDN caching where possible
- Use presigned URLs for temporary access instead of direct downloads
- Consider compression for large files

### Cost Optimization
- Monitor storage usage regularly
- Implement lifecycle rules for temporary content
- Use appropriate storage classes based on access patterns
- Consider R2 Infrequent Access for rarely accessed content

## Troubleshooting

### Common Issues
1. **Permission Denied**: Verify all R2 credentials are correct and have proper permissions
2. **Bucket Not Found**: Ensure the bucket name matches exactly
3. **Upload Failures**: Check file size limits and network connectivity
4. **Authentication Errors**: Verify Account ID and API keys are correct

### Testing Connection
To test your R2 connection, you can run a simple test:

```python
from services.storage_service import CloudflareR2Service

try:
    r2_service = CloudflareR2Service()
    print("R2 connection successful!")
except ValueError as e:
    print(f"R2 configuration error: {e}")
```

## Architecture Considerations

### Data Flow
1. Course content is uploaded to R2 via the storage service
2. Content URLs are stored in the database for quick access
3. Frontend requests content via presigned URLs for security
4. Generated premium content (from Phase 2) is stored in R2

### Backup and Recovery
- R2 provides built-in redundancy across multiple locations
- Regular backups are managed automatically by Cloudflare
- Versioning can be enabled for additional protection

## Scaling Considerations

### Storage Capacity
- R2 scales automatically with your needs
- No storage quotas to worry about
- Pay only for what you use

### Performance
- R2 integrates with Cloudflare's global network
- Automatic edge caching for improved performance
- High availability and durability (99.999999999% durability)

---

Following this guide will ensure your Course Companion FTE project has a robust, scalable, and secure content storage solution using Cloudflare R2.