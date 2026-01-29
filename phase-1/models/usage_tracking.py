from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from . import Base
from datetime import datetime
import uuid

class UsageTracking(Base):
    """
    Database model for tracking feature usage per user
    """
    __tablename__ = "usage_tracking"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Foreign key to User
    feature_name = Column(String, nullable=False)  # Name of the feature being used
    usage_count = Column(Integer, default=1)  # Number of times feature was used (default 1, can be incremented)
    date_recorded = Column(DateTime, nullable=False)  # Date of usage
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UsageTracking(user_id={self.user_id}, feature={self.feature_name}, date={self.date_recorded})>"