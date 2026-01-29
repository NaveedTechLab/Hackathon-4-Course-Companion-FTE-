from sqlalchemy.orm import Session
from models.user import User, SubscriptionTier, SubscriptionStatus
from models.content import Content
from models.course import Course
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime

class SubscriptionService:
    def __init__(self):
        pass

    def verify_user_subscription(self, db: Session, user_id: uuid.UUID) -> Dict[str, Any]:
        """Verify user subscription status"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {
                "user_id": user_id,
                "subscription_valid": False,
                "subscription_tier": None,
                "subscription_status": None,
                "message": "User not found"
            }

        is_active = user.subscription_status == SubscriptionStatus.ACTIVE
        return {
            "user_id": user_id,
            "subscription_valid": is_active,
            "subscription_tier": user.subscription_tier.value if user.subscription_tier else None,
            "subscription_status": user.subscription_status.value if user.subscription_status else None,
            "message": "Subscription is valid" if is_active else f"Subscription is {user.subscription_status.value}"
        }

    def get_user_feature_access(self, db: Session, user_id: uuid.UUID) -> Dict[str, Any]:
        """Get feature access based on subscription tier"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "User not found"}

        # Define feature access by subscription tier
        feature_access = {
            SubscriptionTier.FREE: {
                "content_access": "limited",
                "course_enrollment": "limited",
                "progress_tracking": True,
                "basic_quizzes": True,
                "advanced_quizzes": False,
                "personalized_learning": False,
                "premium_content": False,
                "ai_features": False,
                "support_level": "community"
            },
            SubscriptionTier.PREMIUM: {
                "content_access": "unlimited",
                "course_enrollment": "unlimited",
                "progress_tracking": True,
                "basic_quizzes": True,
                "advanced_quizzes": True,
                "personalized_learning": True,
                "premium_content": True,
                "ai_features": False,  # No AI features in Phase 1
                "support_level": "priority"
            },
            SubscriptionTier.ENTERPRISE: {
                "content_access": "unlimited",
                "course_enrollment": "unlimited",
                "progress_tracking": True,
                "basic_quizzes": True,
                "advanced_quizzes": True,
                "personalized_learning": True,
                "premium_content": True,
                "ai_features": False,  # No AI features in Phase 1
                "support_level": "dedicated"
            }
        }

        tier = user.subscription_tier or SubscriptionTier.FREE
        return {
            "user_id": user_id,
            "subscription_tier": tier.value,
            "features": feature_access[tier]
        }

    def check_content_access(self, db: Session, user_id: uuid.UUID, content_id: uuid.UUID) -> Dict[str, Any]:
        """Check if user has access to specific content"""
        user = db.query(User).filter(User.id == user_id).first()
        content = db.query(Content).filter(Content.id == content_id).first()

        if not user or not content:
            return {
                "accessible": False,
                "reason": "User or content not found",
                "required_tier": "unknown"
            }

        # Get course to which content belongs
        course = db.query(Course).filter(Course.id == content.course_id).first()

        # Determine if content is premium
        # For now, assume any content with 'premium' in metadata is premium
        is_premium_content = (
            content.content_metadata and
            'premium' in content.content_metadata.lower()
        ) if content.content_metadata else False

        # Check if user has appropriate access
        user_tier = user.subscription_tier or SubscriptionTier.FREE

        if is_premium_content and user_tier == SubscriptionTier.FREE:
            return {
                "accessible": False,
                "reason": "Premium content requires paid subscription",
                "required_tier": SubscriptionTier.PREMIUM.value
            }

        # Check if user's subscription is active
        if user.subscription_status != SubscriptionStatus.ACTIVE:
            return {
                "accessible": False,
                "reason": f"Subscription is {user.subscription_status.value}",
                "required_status": "active"
            }

        return {
            "accessible": True,
            "reason": "Access granted",
            "user_tier": user_tier.value,
            "content_type": content.content_type.value
        }

    def check_course_access(self, db: Session, user_id: uuid.UUID, course_id: uuid.UUID) -> Dict[str, Any]:
        """Check if user has access to specific course"""
        user = db.query(User).filter(User.id == user_id).first()
        course = db.query(Course).filter(Course.id == course_id).first()

        if not user or not course:
            return {
                "accessible": False,
                "reason": "User or course not found"
            }

        # Check if user's subscription is active
        if user.subscription_status != SubscriptionStatus.ACTIVE:
            return {
                "accessible": False,
                "reason": f"Subscription is {user.subscription_status.value}"
            }

        return {
            "accessible": True,
            "reason": "Access granted",
            "user_tier": user.subscription_tier.value if user.subscription_tier else SubscriptionTier.FREE.value
        }

    def get_promotional_access(self, db: Session, user_id: uuid.UUID, promotion_code: str) -> Dict[str, Any]:
        """Check for promotional access periods"""
        # This is a simplified implementation
        # In a real system, you'd check against a promotions table
        return {
            "promotion_code": promotion_code,
            "eligible": False,
            "access_tier": None,
            "expiry_date": None,
            "message": "No active promotions found for this code"
        }

    def get_usage_limits(self, db: Session, user_id: uuid.UUID) -> Dict[str, Any]:
        """Get usage limits based on subscription tier"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "User not found"}

        # Define usage limits by subscription tier
        usage_limits = {
            SubscriptionTier.FREE: {
                "monthly_content_views": 50,
                "simultaneous_courses": 2,
                "download_limit_gb": 1,
                "support_tickets_per_month": 1
            },
            SubscriptionTier.PREMIUM: {
                "monthly_content_views": 500,
                "simultaneous_courses": 10,
                "download_limit_gb": 10,
                "support_tickets_per_month": 5
            },
            SubscriptionTier.ENTERPRISE: {
                "monthly_content_views": 10000,
                "simultaneous_courses": 50,
                "download_limit_gb": 100,
                "support_tickets_per_month": 20
            }
        }

        tier = user.subscription_tier or SubscriptionTier.FREE
        return {
            "user_id": user_id,
            "subscription_tier": tier.value,
            "limits": usage_limits[tier]
        }

    def check_usage_limit(self, db: Session, user_id: uuid.UUID, usage_type: str) -> Dict[str, Any]:
        """Check if user has exceeded usage limits"""
        # Get usage limits for user
        limits = self.get_usage_limits(db, user_id)
        if "error" in limits:
            return limits

        # Get current usage (simplified - in reality this would query usage logs)
        # For now, return that limits are not exceeded
        current_usage = 0

        # This is a simplified check - in a real system you'd query usage logs
        limit_map = {
            "content_views": limits["limits"]["monthly_content_views"],
            "courses": limits["limits"]["simultaneous_courses"],
            "downloads": limits["limits"]["download_limit_gb"]
        }

        if usage_type in limit_map:
            limit = limit_map[usage_type]
            return {
                "usage_type": usage_type,
                "current_usage": current_usage,
                "limit": limit,
                "exceeded": current_usage >= limit,
                "remaining": max(0, limit - current_usage)
            }

        return {
            "usage_type": usage_type,
            "error": "Unknown usage type"
        }

    def update_subscription_tier(self, db: Session, user_id: uuid.UUID, new_tier: SubscriptionTier) -> Optional[User]:
        """Update user's subscription tier"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.subscription_tier = new_tier
            if new_tier == SubscriptionTier.FREE:
                user.subscription_status = SubscriptionStatus.ACTIVE  # Free tier is always active
            db.commit()
            db.refresh(user)
        return user

    def update_subscription_status(self, db: Session, user_id: uuid.UUID, new_status: SubscriptionStatus) -> Optional[User]:
        """Update user's subscription status"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.subscription_status = new_status
            db.commit()
            db.refresh(user)
        return user