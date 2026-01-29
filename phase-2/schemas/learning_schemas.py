from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum

class SubscriptionTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class AdaptiveLearningRequest(BaseModel):
    """
    Request model for adaptive learning path generation
    """
    user_id: UUID
    course_id: UUID
    current_progress: Dict[str, Any]
    learning_objectives: List[str]
    content_preferences: Optional[Dict[str, Any]] = None


class AdaptiveLearningResponse(BaseModel):
    """
    Response model for adaptive learning path
    """
    user_id: UUID
    course_id: UUID
    recommended_path: List[Dict[str, Any]]
    alternative_paths: Optional[List[Dict[str, Any]]] = None
    focus_areas: Optional[List[Dict[str, Any]]] = None
    reasoning: str
    estimated_completion_time: Optional[int] = None  # in seconds
    confidence_level: str = "medium"  # high, medium, low


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


class QuizSubmissionRequest(BaseModel):
    """
    Request model for quiz submission
    """
    user_id: UUID
    quiz_id: UUID
    answers: List[Dict[str, Any]]  # List of {question_id, answer_text}
    course_context: Optional[Dict[str, Any]] = None


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
    processing_time_ms: Optional[int] = None


class AssessmentGradeRequest(BaseModel):
    """
    Request model for assessment grading
    """
    user_id: UUID
    assessment_id: UUID
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
    user_id: UUID
    course_id: UUID
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


class TokenCostLogRequest(BaseModel):
    """
    Request model for token cost logging
    """
    user_id: UUID
    feature_type: str
    tokens_input: int
    tokens_output: int
    total_tokens: int
    estimated_cost_usd: float
    model_used: str
    request_metadata: Optional[Dict[str, Any]] = None


class TokenCostLogResponse(BaseModel):
    """
    Response model for token cost logging
    """
    success: bool
    log_id: UUID
    user_id: UUID
    estimated_cost_usd: float
    message: str


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


class UserSubscriptionUpdate(BaseModel):
    """
    Request model for subscription updates
    """
    user_id: UUID
    new_tier: SubscriptionTier
    payment_method_id: Optional[str] = None
    auto_renew: bool = True


class SubscriptionUpdateResponse(BaseModel):
    """
    Response model for subscription updates
    """
    user_id: UUID
    previous_tier: str
    new_tier: str
    status: str
    message: str
    next_billing_date: Optional[datetime] = None


class ProgressTrackingRequest(BaseModel):
    """
    Request model for progress tracking
    """
    user_id: UUID
    content_id: UUID
    status: str  # not_started, in_progress, completed
    completion_percentage: float
    time_spent_seconds: int = 0


class ProgressTrackingResponse(BaseModel):
    """
    Response model for progress tracking
    """
    user_id: UUID
    content_id: UUID
    status: str
    completion_percentage: float
    time_spent_seconds: int
    updated_at: datetime
    message: str