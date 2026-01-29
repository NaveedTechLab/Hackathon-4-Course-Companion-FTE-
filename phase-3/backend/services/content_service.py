from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from ..models.content import Content
from ..storage.r2_client import r2_client
from datetime import datetime

class ContentService:
    """
    Service for content management and delivery
    """

    def __init__(self):
        self.r2_client = r2_client

    def get_content_by_id(self, db: Session, content_id: UUID) -> Optional[Content]:
        """
        Get content by ID
        """
        return db.query(Content).filter(Content.id == content_id).first()

    def get_course_content(self, db: Session, course_id: UUID) -> List[Content]:
        """
        Get all content for a specific course
        """
        return db.query(Content).filter(
            Content.course_id == course_id
        ).order_by(Content.position).all()

    def get_presigned_url(self, r2_key: str) -> str:
        """
        Generate presigned URL for content access
        """
        return self.r2_client.get_presigned_url(r2_key)

    def get_content_from_r2(self, r2_key: str) -> Optional[bytes]:
        """
        Retrieve content from R2 storage
        """
        return self.r2_client.get_content(r2_key)

    def upload_content_to_r2(self, content_data: bytes, r2_key: str, content_type: str) -> str:
        """
        Upload content to R2 storage
        """
        from io import BytesIO
        file_stream = BytesIO(content_data)
        return self.r2_client.upload_content(file_stream, r2_key, content_type)

    def create_content(self, db: Session, course_id: UUID, title: str, content_type: str,
                      r2_key: str, file_size: int = None, content_metadata: str = None) -> Content:
        """
        Create a new content item in the database
        """
        from ..models.content import ContentType
        from datetime import datetime
        import uuid

        # Get position for new content (append to end)
        last_content = db.query(Content).filter(
            Content.course_id == course_id
        ).order_by(Content.position.desc()).first()

        position = (last_content.position + 1) if last_content else 0

        content = Content(
            course_id=course_id,
            title=title,
            content_type=ContentType(content_type),
            r2_key=r2_key,
            file_size=file_size,
            content_metadata=content_metadata,
            position=position,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(content)
        db.commit()
        db.refresh(content)

        return content

    def update_content_metadata(self, db: Session, content_id: UUID, metadata: str) -> Optional[Content]:
        """
        Update content metadata
        """
        content = db.query(Content).filter(Content.id == content_id).first()
        if content:
            content.content_metadata = metadata
            content.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(content)
        return content

    def delete_content(self, db: Session, content_id: UUID) -> bool:
        """
        Delete content from database and R2 storage
        """
        content = db.query(Content).filter(Content.id == content_id).first()
        if content:
            # Delete from R2 storage
            self.r2_client.delete_content(content.r2_key)

            # Delete from database
            db.delete(content)
            db.commit()
            return True
        return False