from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
import uuid
from enum import Enum

class ContentType(Enum):
    TEXT = "text"
    VIDEO = "video"
    PDF = "pdf"
    IMAGE = "image"
    HTML = "html"
    QUIZ = "quiz"

class Content(Base):
    __tablename__ = "content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"))  # Foreign key to Course
    title = Column(String, nullable=False)
    content_type = Column(SQLEnum(ContentType), nullable=False)
    r2_key = Column(String, nullable=False)  # Reference to R2 storage
    file_size = Column(Integer)  # Size in bytes
    content_metadata = Column(Text)  # JSON serialized metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    course = relationship("Course")