from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

class ProgressStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class SubscriptionTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class ContentType(str, Enum):
    TEXT = "text"
    VIDEO = "video"
    PDF = "pdf"
    IMAGE = "image"
    HTML = "html"
    QUIZ = "quiz"

class QuestionType(str, Enum):
    MCQ = "mcq"  # Multiple Choice Question
    TF = "tf"    # True/False
    FILL_BLANK = "fill_blank"
    ESSAY = "essay"

class ProgressTrackingRequest(BaseModel):
    """
    Request model for updating progress
    """
    user_id: str
    content_id: str
    status: ProgressStatus
    completion_percentage: float = 0.0
    time_spent_seconds: int = 0

class ProgressTrackingResponse(BaseModel):
    """
    Response model for progress tracking
    """
    user_id: UUID
    content_id: UUID
    status: ProgressStatus
    completion_percentage: float
    time_spent_seconds: int
    updated_at: datetime
    message: str

class QuizSubmissionRequest(BaseModel):
    """
    Request model for submitting quiz answers
    """
    user_id: str
    quiz_id: str
    answers: List[Dict[str, Any]]  # List of {question_id, answer_text}

class QuizGrade(BaseModel):
    """
    Response model for quiz grading
    """
    quiz_id: UUID
    user_id: UUID
    overall_score: float
    max_score: float
    breakdown: List[Dict[str, Any]]
    detailed_feedback: str
    suggested_improvements: List[str]
    misconceptions_identified: List[str]
    next_learning_recommendations: List[str]
    confidence_level: str  # high, medium, low

class AssessmentGradeRequest(BaseModel):
    """
    Request model for assessment grading
    """
    user_id: str
    assessment_id: str
    question: str
    expected_criteria: List[Dict[str, Any]]
    user_response: str
    context: Optional[Dict[str, Any]] = None

class AssessmentGradeResponse(BaseModel):
    """
    Response model for assessment grading
    """
    assessment_id: UUID
    user_id: UUID
    grade: QuizGrade
    detailed_feedback: str
    suggested_improvements: List[str]
    misconceptions_identified: List[str]
    next_learning_recommendations: List[str]
    confidence_level: str  # high, medium, low

class SynthesisRequest(BaseModel):
    """
    Request model for cross-chapter synthesis
    """
    user_id: str
    course_id: str
    chapters: List[Dict[str, Any]]
    connection_depth: str = "surface"  # surface, deep
    output_format: str = "text"  # text, diagram, comparison

class SynthesisResponse(BaseModel):
    """
    Response model for cross-chapter synthesis
    """
    user_id: UUID
    course_id: UUID
    synthesis_report: Dict[str, Any]
    connections: List[Dict[str, Any]]
    big_picture_insights: List[str]
    synthesis_exercises: List[Dict[str, Any]]
    processing_time_ms: Optional[int] = None

class CostSummaryResponse(BaseModel):
    """
    Response model for cost summary
    """
    user_id: UUID
    total_tokens_used: int
    total_cost: float
    feature_costs: Dict[str, float]
    period_start: datetime
    period_end: datetime
    message: str

class PremiumAccessCheck(BaseModel):
    """
    Response model for premium access verification
    """
    user_id: UUID
    has_premium_access: bool
    is_subscription_active: bool
    subscription_tier: str
    subscription_status: str
    access_granted: bool
    feature_name: Optional[str] = None
    feature_available: Optional[bool] = None
    message: str

class CourseStructure(BaseModel):
    """
    Response model for course structure
    """
    course_id: UUID
    title: str
    total_content_items: int
    content_items: List[Dict[str, Any]]
    structural_patterns: List[Dict[str, Any]]