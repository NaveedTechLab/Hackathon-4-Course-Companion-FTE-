from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
import uuid
from enum import Enum

class ProgressStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Progress(Base):
    __tablename__ = "progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))  # Foreign key to User
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id"))  # Foreign key to Content
    status = Column(SQLEnum(ProgressStatus), default=ProgressStatus.NOT_STARTED)
    completion_percentage = Column(DECIMAL(5, 2))  # Decimal between 0.00 and 100.00
    time_spent_seconds = Column(Integer, default=0)
    last_accessed = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User")
    content = relationship("Content")