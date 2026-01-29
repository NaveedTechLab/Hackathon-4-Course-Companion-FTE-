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

class SubscriptionInfo(BaseModel):
    """
    Response model for subscription information
    """
    user_id: UUID
    has_subscription: bool
    tier: SubscriptionTier
    status: SubscriptionStatus
    is_active: bool
    has_premium_access: bool
    end_date: Optional[datetime] = None
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

class FeatureAccess(BaseModel):
    """
    Response model for feature access information
    """
    user_id: UUID
    can_access_premium_features: bool
    available_features: List[str]
    tier: str
    status: str
    message: str

class UsageLimitCheck(BaseModel):
    """
    Response model for usage limit checks
    """
    user_id: UUID
    feature_name: str
    usage_count: int
    usage_limit: int
    remaining_uses: int
    limit_exceeded: bool
    message: str

class PremiumFeatureRequest(BaseModel):
    """
    Request model for premium feature access
    """
    user_id: UUID
    feature_name: str
    context: Optional[Dict[str, Any]] = None

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

class RubricItem(BaseModel):
    """
    Model for individual rubric criteria
    """
    criterion: str
    points: int
    description: str
    weight: float = 1.0  # Relative importance of this criterion


class Rubric(BaseModel):
    """
    Model for assessment rubric
    """
    criteria: List[RubricItem]
    max_score: int
    grading_scale: str = "percentage"  # percentage, letter, points
    detailed_feedback_required: bool = True


class AssessmentGradeRequest(BaseModel):
    """
    Request model for assessment grading
    """
    user_id: UUID
    assessment_id: Optional[UUID] = None
    question: str
    correct_answer: Optional[str] = None
    student_response: str
    rubric: Optional[Rubric] = None
    context: Optional[Dict[str, Any]] = None
    course_context: Optional[str] = None


class AssessmentGradeResponse(BaseModel):
    """
    Response model for assessment grading
    """
    assessment_id: UUID
    user_id: UUID
    question: str
    student_response: str
    score: float
    max_score: int
    feedback: str
    strengths: List[str]
    areas_for_improvement: List[str]
    misconceptions_identified: List[str]
    next_learning_recommendations: List[str]
    graded_at: str


class SynthesisRequest(BaseModel):
    """
    Request model for cross-chapter synthesis
    """
    user_id: UUID
    course_id: UUID
    chapters: List[str]
    focus_areas: Optional[List[str]] = None
    connection_depth: str = "moderate"  # shallow, moderate, deep
    output_format: str = "text"  # text, outline, comparison


class SynthesisResponse(BaseModel):
    """
    Response model for cross-chapter synthesis
    """
    synthesis_id: UUID
    user_id: UUID
    course_id: UUID
    chapters_synthesized: List[str]
    focus_areas: List[str]
    synthesis_content: str
    key_connections: List[str]
    generated_at: str


class OverviewRequest(BaseModel):
    """
    Request model for course overview
    """
    user_id: UUID
    course_id: UUID
    include_progress: bool = False


class ExerciseRequest(BaseModel):
    """
    Request model for synthesis exercise
    """
    user_id: UUID
    course_id: UUID
    concept_pairs: List[tuple]
    difficulty: str = "intermediate"  # beginner, intermediate, advanced


class ExerciseResponse(BaseModel):
    """
    Response model for synthesis exercise
    """
    exercise_id: UUID
    user_id: UUID
    course_id: UUID
    concept_pairs: List[tuple]
    difficulty: str
    exercise_content: str
    sample_solution: str
    learning_objectives: List[str]
    created_at: str

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
    total_estimated_cost: float
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