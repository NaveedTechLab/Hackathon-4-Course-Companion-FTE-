from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Enum as SQLEnum

class QuestionType(Enum):
    MCQ = "mcq"  # Multiple Choice Question
    TF = "tf"    # True/False
    FILL_BLANK = "fill_blank"
    ESSAY = "essay"

class Quiz(Base):
    """
    Database model for quizzes
    """
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id"), nullable=False)  # Foreign key to Content
    title = Column(String, nullable=False)
    instructions = Column(Text)
    time_limit_minutes = Column(Integer)  # Optional time limit
    max_attempts = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content = relationship("Content", back_populates="quiz")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Quiz(id={self.id}, title={self.title}, content_id={self.content_id})>"


class QuizQuestion(Base):
    """
    Database model for quiz questions
    """
    __tablename__ = "quiz_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"), nullable=False)  # Foreign key to Quiz
    question_text = Column(Text, nullable=False)
    question_type = Column(SQLEnum(QuestionType), nullable=False)
    question_order = Column(Integer, default=0)
    points = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("QuizAnswer", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<QuizQuestion(id={self.id}, quiz_id={self.quiz_id}, type={self.question_type.value})>"


class QuizAnswer(Base):
    """
    Database model for quiz answer options
    """
    __tablename__ = "quiz_answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("quiz_questions.id"), nullable=False)  # Foreign key to QuizQuestion
    answer_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    points_awarded = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    question = relationship("QuizQuestion", back_populates="answers")

    def __repr__(self):
        return f"<QuizAnswer(id={self.id}, question_id={self.question_id}, is_correct={self.is_correct})>"


class QuizSubmission(Base):
    """
    Database model for quiz submissions
    """
    __tablename__ = "quiz_submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Foreign key to User
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"), nullable=False)  # Foreign key to Quiz
    score = Column(DECIMAL(5, 2))  # Score as percentage (0.00 to 100.00)
    max_score = Column(Integer)  # Maximum possible score
    submitted_at = Column(DateTime, default=datetime.utcnow)
    attempt_number = Column(Integer, default=1)

    # Relationships
    user = relationship("User")
    quiz = relationship("Quiz")

    def __repr__(self):
        return f"<QuizSubmission(user_id={self.user_id}, quiz_id={self.quiz_id}, score={self.score}, attempt={self.attempt_number})>"

# Add relationships to Content model if they don't exist in the content model file:
"""
quiz = relationship("Quiz", uselist=False, back_populates="content", cascade="all, delete-orphan")
"""

# Add relationship to User model if it doesn't exist in the user model file:
"""
quiz_submissions = relationship("QuizSubmission", back_populates="user")
"""