from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum

class ContentTypeEnum(str, Enum):
    TEXT = "text"
    VIDEO = "video"
    PDF = "pdf"
    IMAGE = "image"
    HTML = "html"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    LECTURE = "lecture"

class ContentResponse(BaseModel):
    """
    Response model for content retrieval
    """
    id: UUID
    title: str
    content_type: str
    file_size: Optional[int] = None
    download_url: str
    content_metadata: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CourseContentResponse(BaseModel):
    """
    Response model for course content listing
    """
    course_id: UUID
    content_items: List[ContentResponse]
    total_items: int

class UploadContentRequest(BaseModel):
    """
    Request model for content upload
    """
    course_id: UUID
    title: str
    content_type: ContentTypeEnum
    file_data: bytes  # In a real implementation, this would be handled differently
    content_metadata: Optional[Dict[str, Any]] = None

class UploadContentResponse(BaseModel):
    """
    Response model for content upload
    """
    content_id: UUID
    title: str
    content_type: str
    file_size: int
    r2_key: str
    message: str

class UpdateContentRequest(BaseModel):
    """
    Request model for content updates
    """
    title: Optional[str] = None
    content_metadata: Optional[Dict[str, Any]] = None