from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from models.subscription import Subscription, SubscriptionTier, SubscriptionStatus
from models.user import User  # Assuming User model from Phase 1
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PremiumService:
    """
    Service for handling premium access verification and subscription management
    """

    def __init__(self):
        pass

    def check_user_subscription_status(self, db: Session, user_id: UUID) -> dict:
        """
        Check the subscription status of a user
        """
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()

        if not subscription:
            return {
                "user_id": user_id,
                "has_subscription": False,
                "tier": SubscriptionTier.FREE.value,
                "status": SubscriptionStatus.INACTIVE.value,
                "is_active": False,
                "has_premium_access": False,
                "message": "No subscription found for user"
            }

        is_active = subscription.is_active()
        has_premium_access = subscription.has_premium_access()

        return {
            "user_id": user_id,
            "has_subscription": True,
            "tier": subscription.tier.value,
            "status": subscription.status.value,
            "is_active": is_active,
            "has_premium_access": has_premium_access,
            "end_date": subscription.end_date,
            "message": f"Subscription {subscription.status.value} ({subscription.tier.value} tier)"
        }

    def has_access_to_feature(self, db: Session, user_id: UUID, feature_name: str) -> bool:
        """
        Check if user has access to a specific premium feature
        """
        subscription_info = self.check_user_subscription_status(db, user_id)

        # All premium features require at least PREMIUM tier and active status
        return (
            subscription_info["is_active"] and
            subscription_info["has_premium_access"]
        )

    def get_premium_feature_access(self, db: Session, user_id: UUID) -> dict:
        """
        Get detailed information about what premium features a user can access
        """
        subscription_info = self.check_user_subscription_status(db, user_id)

        if not subscription_info["has_premium_access"]:
            return {
                "user_id": user_id,
                "can_access_premium_features": False,
                "available_features": [],
                "tier": subscription_info["tier"],
                "status": subscription_info["status"],
                "message": "User does not have premium access"
            }

        # Determine available features based on tier
        available_features = ["adaptive_learning", "llm_assessment_grading", "cross_chapter_synthesis"]

        if subscription_info["tier"] == SubscriptionTier.ENTERPRISE.value:
            available_features.extend(["advanced_analytics", "custom_content", "priority_support"])

        return {
            "user_id": user_id,
            "can_access_premium_features": True,
            "available_features": available_features,
            "tier": subscription_info["tier"],
            "status": subscription_info["status"],
            "message": f"User has access to {len(available_features)} premium features"
        }

    def verify_premium_access(self, db: Session, user_id: UUID, feature_name: str = None) -> dict:
        """
        Verify premium access for a user with detailed information
        """
        subscription_info = self.check_user_subscription_status(db, user_id)

        result = {
            "user_id": user_id,
            "has_premium_access": subscription_info["has_premium_access"],
            "is_subscription_active": subscription_info["is_active"],
            "subscription_tier": subscription_info["tier"],
            "subscription_status": subscription_info["status"],
            "access_granted": False,
            "feature_name": feature_name
        }

        # Check if user has active premium subscription
        if subscription_info["is_active"] and subscription_info["has_premium_access"]:
            result["access_granted"] = True
            result["message"] = f"Access granted to {feature_name or 'premium features'}"

            # If feature name specified, check if it's available for this tier
            if feature_name:
                available_features = self._get_features_for_tier(subscription_info["tier"])
                if feature_name in available_features:
                    result["feature_available"] = True
                    result["message"] = f"Access granted to {feature_name}"
                else:
                    result["feature_available"] = False
                    result["access_granted"] = False
                    result["message"] = f"Feature '{feature_name}' not available for {subscription_info['tier']} tier"
        else:
            result["message"] = f"Access denied: {subscription_info['message']}"

        # Log access attempt for analytics
        self._log_access_attempt(db, user_id, feature_name, result["access_granted"])

        return result

    def _get_features_for_tier(self, tier: str) -> list:
        """
        Get list of features available for a specific subscription tier
        """
        base_features = [
            "adaptive_learning",
            "llm_assessment_grading",
            "cross_chapter_synthesis"
        ]

        if tier == SubscriptionTier.ENTERPRISE.value:
            return base_features + [
                "advanced_analytics",
                "custom_content",
                "priority_support",
                "admin_dashboard",
                "api_access"
            ]
        elif tier == SubscriptionTier.PREMIUM.value:
            return base_features + [
                "basic_analytics",
                "custom_content"
            ]
        else:  # FREE tier
            return []

    def _log_access_attempt(self, db: Session, user_id: UUID, feature_name: str, access_granted: bool):
        """
        Log access attempt for analytics and monitoring
        """
        from models.usage_tracking import UsageTracking
        from datetime import date

        # Check if we already have a record for this user, feature, and date
        today = date.today()
        existing_record = db.query(UsageTracking).filter(
            UsageTracking.user_id == user_id,
            UsageTracking.feature_name == feature_name,
            UsageTracking.date_recorded == today
        ).first()

        if existing_record:
            # Update existing record
            existing_record.usage_count += 1
            existing_record.updated_at = datetime.utcnow()
        else:
            # Create new record
            usage_record = UsageTracking(
                user_id=user_id,
                feature_name=feature_name,
                usage_count=1
            )
            db.add(usage_record)

        try:
            db.commit()
        except Exception as e:
            logger.error(f"Failed to log access attempt: {e}")
            db.rollback()

    def upgrade_subscription(self, db: Session, user_id: UUID, new_tier: SubscriptionTier) -> dict:
        """
        Upgrade user's subscription to a new tier
        """
        # Get current subscription
        current_subscription = db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()

        if not current_subscription:
            # Create new subscription
            new_subscription = Subscription(
                user_id=user_id,
                tier=new_tier,
                status=SubscriptionStatus.ACTIVE
            )
            db.add(new_subscription)
        else:
            # Update existing subscription
            current_subscription.tier = new_tier
            current_subscription.status = SubscriptionStatus.ACTIVE
            current_subscription.updated_at = datetime.utcnow()

        try:
            db.commit()
            return {
                "user_id": user_id,
                "previous_tier": current_subscription.tier.value if current_subscription else "none",
                "new_tier": new_tier.value,
                "status": "subscription_upgraded",
                "message": f"Subscription upgraded to {new_tier.value}"
            }
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to upgrade subscription: {e}")
            return {
                "user_id": user_id,
                "status": "upgrade_failed",
                "error": str(e),
                "message": "Failed to upgrade subscription"
            }

    def check_usage_limit(self, db: Session, user_id: UUID, feature_name: str) -> dict:
        """
        Check if user has exceeded usage limits for a feature
        """
        from models.usage_tracking import UsageTracking
        from datetime import date

        today = date.today()

        # Get today's usage for this feature
        today_usage = db.query(UsageTracking).filter(
            UsageTracking.user_id == user_id,
            UsageTracking.feature_name == feature_name,
            UsageTracking.date_recorded == today
        ).first()

        usage_count = today_usage.usage_count if today_usage else 0

        # Get subscription info to determine limits
        subscription_info = self.check_user_subscription_status(db, user_id)
        tier = subscription_info["tier"]

        # Define usage limits by tier
        usage_limits = {
            "free": 2,      # 2 uses per day for free tier
            "premium": 20,  # 20 uses per day for premium
            "enterprise": 100  # 100 uses per day for enterprise
        }

        limit = usage_limits.get(tier, 2)

        return {
            "user_id": user_id,
            "feature_name": feature_name,
            "usage_count": usage_count,
            "usage_limit": limit,
            "remaining_uses": max(0, limit - usage_count),
            "limit_exceeded": usage_count >= limit,
            "message": f"Used {usage_count}/{limit} daily allocations"
        }

    def is_within_usage_limit(self, db: Session, user_id: UUID, feature_name: str) -> bool:
        """
        Check if user is within usage limits for a feature
        """
        usage_info = self.check_usage_limit(db, user_id, feature_name)
        return not usage_info["limit_exceeded"]