from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

class CourseStructureResponse(BaseModel):
    """
    Response model for course structure
    """
    course_id: UUID
    title: str
    chapters: List[Dict[str, Any]]
    total_chapters: int

class NextContentResponse(BaseModel):
    """
    Response model for next content navigation
    """
    course_id: UUID
    user_id: UUID
    has_next_content: bool
    next_content_id: Optional[UUID] = None
    next_content_title: Optional[str] = None
    next_content_type: Optional[str] = None
    message: str

class PrevContentResponse(BaseModel):
    """
    Response model for previous content navigation
    """
    course_id: UUID
    current_content_id: UUID
    has_prev_content: bool
    prev_content_id: Optional[UUID] = None
    prev_content_title: Optional[str] = None
    message: str

class BookmarkRequest(BaseModel):
    """
    Request model for setting bookmarks
    """
    content_id: UUID
    position: int
    note: Optional[str] = None

class BookmarkResponse(BaseModel):
    """
    Response model for bookmark operations
    """
    user_id: UUID
    content_id: UUID
    position: int
    note: Optional[str] = None
    bookmarked_at: datetime
    message: str

class GetUserBookmarksResponse(BaseModel):
    """
    Response model for user bookmarks
    """
    user_id: UUID
    course_id: Optional[UUID] = None
    bookmarks: List[Dict[str, Any]]
    total_bookmarks: int