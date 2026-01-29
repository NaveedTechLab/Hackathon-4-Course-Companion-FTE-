from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

class QuestionType(str, Enum):
    MCQ = "mcq"
    TF = "tf"
    FILL_BLANK = "fill_blank"
    ESSAY = "essay"

class QuizSubmissionRequest(BaseModel):
    """
    Request model for submitting quiz answers
    """
    user_id: str
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

class QuizCreationRequest(BaseModel):
    """
    Request model for creating a quiz
    """
    course_id: str
    title: str
    instructions: Optional[str] = None
    time_limit_minutes: Optional[int] = None
    max_attempts: Optional[int] = 1

class QuizQuestionRequest(BaseModel):
    """
    Request model for creating a quiz question
    """
    quiz_id: str
    question_text: str
    question_type: QuestionType
    points: Optional[int] = 1
    question_order: Optional[int] = 0

class QuizAnswerRequest(BaseModel):
    """
    Request model for creating a quiz answer option
    """
    question_id: str
    answer_text: str
    is_correct: bool
    points_awarded: Optional[int] = 0

class QuizResponse(BaseModel):
    """
    Response model for quiz details
    """
    quiz_id: UUID
    title: str
    instructions: Optional[str]
    time_limit_minutes: Optional[int]
    questions: List[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime] = None

class QuizResultResponse(BaseModel):
    """
    Response model for quiz results
    """
    quiz_id: UUID
    user_id: UUID
    score: float
    max_score: float
    percentage: float
    submitted_at: datetime
    attempts_count: int
    breakdown: List[Dict[str, Any]]