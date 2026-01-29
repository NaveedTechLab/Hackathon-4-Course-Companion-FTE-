from sqlalchemy.orm import Session
from models.content import Content, ContentType
from storage.r2_client import r2_client
from typing import Optional, List
import uuid
from io import BytesIO
from datetime import datetime

class ContentService:
    def __init__(self):
        pass

    def get_content_by_id(self, db: Session, content_id: uuid.UUID) -> Optional[Content]:
        """Get content by ID"""
        return db.query(Content).filter(Content.id == content_id).first()

    def get_content_by_r2_key(self, db: Session, r2_key: str) -> Optional[Content]:
        """Get content by R2 key"""
        return db.query(Content).filter(Content.r2_key == r2_key).first()

    def create_content(self, db: Session, course_id: uuid.UUID, title: str, content_type: ContentType,
                      r2_key: str, file_size: int = None, content_metadata: str = None) -> Content:
        """Create new content entry"""
        content = Content(
            course_id=course_id,
            title=title,
            content_type=content_type,
            r2_key=r2_key,
            file_size=file_size,
            content_metadata=content_metadata
        )
        db.add(content)
        db.commit()
        db.refresh(content)
        return content

    def upload_content_to_r2(self, file_data: bytes, object_key: str, content_type: str = "application/octet-stream") -> str:
        """Upload content to R2 storage"""
        file_stream = BytesIO(file_data)
        return r2_client.upload_content(file_stream, object_key, content_type)

    def get_content_from_r2(self, object_key: str) -> Optional[bytes]:
        """Retrieve content from R2 storage"""
        return r2_client.get_content(object_key)

    def get_presigned_url(self, object_key: str, expiration: int = 3600) -> str:
        """Generate presigned URL for content access"""
        return r2_client.get_presigned_url(object_key, expiration)

    def delete_content_from_r2(self, object_key: str) -> bool:
        """Delete content from R2 storage"""
        return r2_client.delete_content(object_key)

    def check_content_exists_in_r2(self, object_key: str) -> bool:
        """Check if content exists in R2 storage"""
        return r2_client.object_exists(object_key)

    def get_course_content(self, db: Session, course_id: uuid.UUID) -> List[Content]:
        """Get all content for a specific course"""
        return db.query(Content).filter(Content.course_id == course_id).all()

    def update_content_metadata(self, db: Session, content_id: uuid.UUID, metadata: str) -> Optional[Content]:
        """Update content metadata"""
        content = db.query(Content).filter(Content.id == content_id).first()
        if content:
            content.content_metadata = metadata
            content.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(content)
        return content