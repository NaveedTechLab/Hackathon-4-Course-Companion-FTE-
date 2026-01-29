from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid

class ContentTypeEnum(str, Enum):
    TEXT = "text"
    VIDEO = "video"
    PDF = "pdf"
    IMAGE = "image"
    HTML = "html"
    QUIZ = "quiz"

class ContentResponse(BaseModel):
    id: uuid.UUID
    title: str
    content_type: str
    file_size: Optional[int]
    created_at: datetime
    updated_at: datetime
    download_url: str

    class Config:
        from_attributes = True