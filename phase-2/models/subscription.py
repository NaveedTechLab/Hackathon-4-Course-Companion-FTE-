from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
import uuid
from enum import Enum

class SubscriptionTier(Enum):
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class SubscriptionFeature(Enum):
    ADAPTIVE_LEARNING = "adaptive_learning"
    ASSESSMENT_GRADING = "assessment_grading"
    CROSS_CHAPTER_SYNTHESIS = "cross_chapter_synthesis"
    PREMIUM_CONTENT = "premium_content"

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class Subscription(Base):
    """
    Database model for user subscription information
    """
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Links to User table from Phase 1
    tier = Column(SQLEnum(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False)
    status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)  # Null for lifetime subscriptions or free tier
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cancellation_reason = Column(String)  # If cancelled, why

    # Relationship
    user = relationship("User", back_populates="subscription")

    def is_active(self) -> bool:
        """Check if subscription is currently active"""
        return (
            self.status == SubscriptionStatus.ACTIVE and
            (self.end_date is None or self.end_date > datetime.utcnow())
        )

    def has_premium_access(self) -> bool:
        """Check if user has premium access (not just free tier)"""
        return self.tier in [SubscriptionTier.PREMIUM, SubscriptionTier.ENTERPRISE]

    def days_remaining(self) -> int:
        """Calculate days remaining in subscription (returns -1 for expired, None for lifetime)"""
        if self.end_date is None:
            return None  # Lifetime subscription
        if self.end_date < datetime.utcnow():
            return -1  # Expired
        return (self.end_date - datetime.utcnow()).days

    def __repr__(self):
        return f"<Subscription(user_id={self.user_id}, tier={self.tier.value}, status={self.status.value})>"


class UsageTracking(Base):
    """
    Database model for tracking premium feature usage per user
    """
    __tablename__ = "usage_tracking"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Links to User table from Phase 1
    feature_name = Column(String, nullable=False)  # e.g., "adaptive_learning", "assessment_grading"
    usage_count = Column(Integer, default=1)  # Number of times feature was used
    date_recorded = Column(DateTime, default=datetime.utcnow, index=True)  # Date of usage
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="usage_tracking")

    def __repr__(self):
        return f"<UsageTracking(user_id={self.user_id}, feature={self.feature_name}, count={self.usage_count})>"