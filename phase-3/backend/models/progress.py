from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Enum as SQLEnum

class ProgressStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Progress(Base):
    """
    Database model for tracking user progress on content
    """
    __tablename__ = "progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Foreign key to User
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id"), nullable=False)  # Foreign key to Content
    status = Column(SQLEnum(ProgressStatus), default=ProgressStatus.NOT_STARTED, nullable=False)
    completion_percentage = Column(DECIMAL(5, 2))  # Decimal between 0.00 and 100.00
    time_spent_seconds = Column(Integer, default=0)
    last_accessed = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="progress_records")
    content = relationship("Content", back_populates="progress_records")

    def __repr__(self):
        return f"<Progress(user_id={self.user_id}, content_id={self.content_id}, status={self.status.value}, completion={self.completion_percentage}%)>"

class Streak(Base):
    """
    Database model for tracking user learning streaks
    """
    __tablename__ = "streaks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    current_streak = Column(Integer, default=0)  # Number of consecutive days of learning
    longest_streak = Column(Integer, default=0)  # Longest streak ever achieved
    last_learning_date = Column(DateTime)  # Date of last learning activity
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="streak")

    def __repr__(self):
        return f"<Streak(user_id={self.user_id}, current_streak={self.current_streak}, longest_streak={self.longest_streak})>"

# Add relationships to User model if they don't exist in the user model file:
"""
progress_records = relationship("Progress", back_populates="user", foreign_keys=[Progress.user_id])
streak = relationship("Streak", uselist=False, back_populates="user", foreign_keys=[Streak.user_id])
"""