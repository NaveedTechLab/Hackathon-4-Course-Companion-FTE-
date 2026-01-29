from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

class ProgressStatusEnum(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class UpdateProgressRequest(BaseModel):
    """
    Request model for updating content progress
    """
    status: ProgressStatusEnum
    completion_percentage: float = 0.0
    time_spent_seconds: int = 0

class UpdateProgressResponse(BaseModel):
    """
    Response model for progress updates
    """
    user_id: UUID
    content_id: UUID
    status: str
    completion_percentage: float
    time_spent_seconds: int
    updated_at: datetime
    message: str

class GetUserProgressResponse(BaseModel):
    """
    Response model for user progress summary
    """
    user_id: UUID
    total_content: int
    completed_content: int
    in_progress_content: int
    not_started_content: int
    overall_completion_percentage: float
    current_streak_days: int
    last_active: Optional[datetime] = None
    progress_distribution: Dict[str, int]

class GetUserCourseProgressResponse(BaseModel):
    """
    Response model for course-specific progress
    """
    user_id: UUID
    course_id: UUID
    total_content_items: int
    completed_items: int
    completion_percentage: float
    content_progress: List[Dict[str, Any]]
    milestones: List[Dict[str, Any]]
    recommendations: List[str]

class StreakResponse(BaseModel):
    """
    Response model for learning streak
    """
    user_id: UUID
    current_streak_days: int
    longest_streak_days: int
    last_learning_date: Optional[datetime] = None
    message: str

class LearningAnalyticsResponse(BaseModel):
    """
    Response model for detailed learning analytics
    """
    user_id: UUID
    course_id: Optional[UUID] = None
    total_content_accessed: int
    total_time_spent_seconds: int
    completed_content_count: int
    average_time_per_content: float
    learning_patterns: List[Dict[str, Any]]
    performance_insights: List[Dict[str, Any]]
    last_active: Optional[datetime] = None