from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from . import Base
from datetime import datetime
import uuid
from enum import Enum

class SubscriptionTier(Enum):
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class User(Base):
    """
    Database model for user information
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    subscription_tier = Column(SQLEnum(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False)
    subscription_status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime)

    def is_active(self) -> bool:
        """Check if user subscription is active"""
        return self.subscription_status == SubscriptionStatus.ACTIVE

    def has_premium_access(self) -> bool:
        """Check if user has premium access (not just free tier)"""
        return self.subscription_tier in [SubscriptionTier.PREMIUM, SubscriptionTier.ENTERPRISE]

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, tier={self.subscription_tier.value})>"