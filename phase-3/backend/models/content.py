from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Enum as SQLEnum

class ContentType(Enum):
    TEXT = "text"
    VIDEO = "video"
    PDF = "pdf"
    IMAGE = "image"
    HTML = "html"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    LECTURE = "lecture"

class Content(Base):
    """
    Database model for educational content
    """
    __tablename__ = "content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)  # Foreign key to Course
    title = Column(String, nullable=False)
    content_type = Column(SQLEnum(ContentType), nullable=False)
    r2_key = Column(String, nullable=False)  # Reference to R2 storage key
    file_size = Column(Integer)  # Size in bytes
    content_metadata = Column(Text)  # JSON serialized metadata about content
    position = Column(Integer, default=0)  # Position in course sequence
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="content_items")

    def get_content_url(self) -> str:
        """Generate content URL for retrieval"""
        return f"/api/v1/content/{self.id}/download"

    def __repr__(self):
        return f"<Content(id={self.id}, title={self.title}, type={self.content_type.value})>"


# Add relationship to Course model if it doesn't exist in the course model file
# This should be added to the Course model file as well:
"""
content_items = relationship("Content", back_populates="course", order_by=Content.position)
"""