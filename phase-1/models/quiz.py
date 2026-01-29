from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
import uuid
from enum import Enum

class QuestionType(Enum):
    MCQ = "mcq"  # Multiple Choice Question
    TF = "tf"    # True/False
    FILL_BLANK = "fill_blank"
    ESSAY = "essay"

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id"))  # Foreign key to Content
    title = Column(String, nullable=False)
    instructions = Column(Text)
    time_limit_minutes = Column(Integer)
    max_attempts = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    content = relationship("Content")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))  # Foreign key to Quiz
    question_text = Column(Text, nullable=False)
    question_type = Column(SQLEnum(QuestionType), nullable=False)
    question_order = Column(Integer, default=0)
    points = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    quiz = relationship("Quiz")


class QuizAnswer(Base):
    __tablename__ = "quiz_answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("quiz_questions.id"))  # Foreign key to QuizQuestion
    answer_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    points_awarded = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    question = relationship("QuizQuestion")


class QuizSubmission(Base):
    __tablename__ = "quiz_submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    score = Column(Integer, default=0)
    max_score = Column(Integer, default=0)
    attempt_number = Column(Integer, default=1)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    quiz = relationship("Quiz")
