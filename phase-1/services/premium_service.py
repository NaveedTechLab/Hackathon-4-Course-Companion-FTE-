from sqlalchemy.orm import Session
from models.user import User, SubscriptionTier
from models.subscription import Subscription
from typing import Dict, Any, Optional, List
import uuid
from datetime import datetime, date
from enum import Enum

class Feature(Enum):
    CONTENT_ACCESS = "content_access"
    COURSE_NAVIGATION = "course_navigation"
    QUIZ_SUBMISSION = "quiz_submission"
    ASSESSMENT_GRADING = "assessment_grading"
    CROSS_CHAPTER_SYNTHESIS = "cross_chapter_synthesis"
    ADAPTIVE_LEARNING = "adaptive_learning"
    PROGRESS_TRACKING = "progress_tracking"
    CHAT_INTERFACE = "chat_interface"

class FeatureTier(Enum):
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

# Define feature access by tier
FEATURE_ACCESS_MATRIX = {
    Feature.CONTENT_ACCESS: {
        FeatureTier.FREE: True,
        FeatureTier.PREMIUM: True,
        FeatureTier.ENTERPRISE: True
    },
    Feature.COURSE_NAVIGATION: {
        FeatureTier.FREE: True,
        FeatureTier.PREMIUM: True,
        FeatureTier.ENTERPRISE: True
    },
    Feature.QUIZ_SUBMISSION: {
        FeatureTier.FREE: True,
        FeatureTier.PREMIUM: True,
        FeatureTier.ENTERPRISE: True
    },
    Feature.ASSESSMENT_GRADING: {
        FeatureTier.FREE: False,
        FeatureTier.PREMIUM: True,
        FeatureTier.ENTERPRISE: True
    },
    Feature.CROSS_CHAPTER_SYNTHESIS: {
        FeatureTier.FREE: False,
        FeatureTier.PREMIUM: True,
        FeatureTier.ENTERPRISE: True
    },
    Feature.ADAPTIVE_LEARNING: {
        FeatureTier.FREE: False,
        FeatureTier.PREMIUM: True,
        FeatureTier.ENTERPRISE: True
    },
    Feature.PROGRESS_TRACKING: {
        FeatureTier.FREE: True,
        FeatureTier.PREMIUM: True,
        FeatureTier.ENTERPRISE: True
    },
    Feature.CHAT_INTERFACE: {
        FeatureTier.FREE: False,
        FeatureTier.PREMIUM: True,
        FeatureTier.ENTERPRISE: True
    }
}

# Define usage limits by tier (per day)
USAGE_LIMITS = {
    FeatureTier.FREE: {
        Feature.ASSESSMENT_GRADING: 2,
        Feature.CROSS_CHAPTER_SYNTHESIS: 1,
        Feature.ADAPTIVE_LEARNING: 2,
        Feature.CHAT_INTERFACE: 5
    },
    FeatureTier.PREMIUM: {
        Feature.ASSESSMENT_GRADING: 20,
        Feature.CROSS_CHAPTER_SYNTHESIS: 10,
        Feature.ADAPTIVE_LEARNING: 20,
        Feature.CHAT_INTERFACE: 100
    },
    FeatureTier.ENTERPRISE: {
        Feature.ASSESSMENT_GRADING: 100,
        Feature.CROSS_CHAPTER_SYNTHESIS: 50,
        Feature.ADAPTIVE_LEARNING: 100,
        Feature.CHAT_INTERFACE: 500
    }
}

class PremiumService:
    """
    Service for managing premium feature access and usage tracking
    """

    def __init__(self):
        pass

    def check_feature_access(self, db: Session, user_id: uuid.UUID, feature_name: str) -> Dict[str, Any]:
        """
        Check if user has access to a specific feature
        """
        try:
            feature = Feature(feature_name)
        except ValueError:
            return {
                "has_access": False,
                "feature_name": feature_name,
                "message": f"Unknown feature: {feature_name}",
                "required_tier": "unknown"
            }

        # Get user's subscription
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {
                "has_access": False,
                "feature_name": feature_name,
                "message": "User not found",
                "required_tier": "unknown"
            }

        # Determine user's tier
        user_tier = user.subscription_tier
        tier_enum = FeatureTier(user_tier.value)

        # Check if feature is available for this tier
        is_available = FEATURE_ACCESS_MATRIX.get(feature, {}).get(tier_enum, False)

        if is_available:
            return {
                "has_access": True,
                "feature_name": feature_name,
                "user_tier": user_tier.value,
                "message": f"Access granted to {feature_name}",
                "required_tier": self._get_required_tier(feature).value
            }
        else:
            required_tier = self._get_required_tier(feature)
            return {
                "has_access": False,
                "feature_name": feature_name,
                "user_tier": user_tier.value,
                "message": f"Feature {feature_name} requires {required_tier.value} tier or higher",
                "required_tier": required_tier.value
            }

    def _get_required_tier(self, feature: Feature) -> FeatureTier:
        """
        Get the minimum required tier for a feature
        """
        for tier in [FeatureTier.ENTERPRISE, FeatureTier.PREMIUM, FeatureTier.FREE]:
            if FEATURE_ACCESS_MATRIX[feature].get(tier, False):
                return tier

        # If feature is not available in any tier, return highest tier
        return FeatureTier.ENTERPRISE

    def check_usage_limit(self, db: Session, user_id: uuid.UUID, feature_name: str) -> Dict[str, Any]:
        """
        Check if user has exceeded usage limits for a feature
        """
        try:
            feature = Feature(feature_name)
        except ValueError:
            return {
                "limit_exceeded": True,
                "feature_name": feature_name,
                "message": f"Unknown feature: {feature_name}",
                "usage_count": 0,
                "limit": 0
            }

        # Get user's subscription tier
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {
                "limit_exceeded": True,
                "feature_name": feature_name,
                "message": "User not found",
                "usage_count": 0,
                "limit": 0
            }

        user_tier = FeatureTier(user.subscription_tier.value)

        # Get the usage limit for this tier and feature
        tier_limits = USAGE_LIMITS.get(user_tier, {})
        daily_limit = tier_limits.get(feature, 0)

        if daily_limit == 0:
            # Feature not available for this tier
            return {
                "limit_exceeded": True,
                "feature_name": feature_name,
                "message": f"Feature {feature_name} not available for {user_tier.value} tier",
                "usage_count": 0,
                "limit": 0
            }

        # Get today's usage count
        from models.usage_tracking import UsageTracking
        today = date.today()

        usage_count = db.query(UsageTracking).filter(
            UsageTracking.user_id == user_id,
            UsageTracking.feature_name == feature_name,
            UsageTracking.date_recorded == today
        ).count()

        return {
            "limit_exceeded": usage_count >= daily_limit,
            "feature_name": feature_name,
            "usage_count": usage_count,
            "limit": daily_limit,
            "remaining": daily_limit - usage_count,
            "message": f"Used {usage_count}/{daily_limit} daily allocations for {feature_name}"
        }

    def track_feature_usage(self, db: Session, user_id: uuid.UUID, feature_name: str) -> bool:
        """
        Track usage of a premium feature
        """
        from models.usage_tracking import UsageTracking

        today = date.today()

        # Check if usage record already exists for today
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
                usage_count=1,
                date_recorded=today
            )
            db.add(usage_record)

        try:
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error tracking usage: {e}")
            return False

    def get_user_feature_access(self, db: Session, user_id: uuid.UUID) -> Dict[str, Any]:
        """
        Get all features available to a user based on their subscription tier
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {
                "user_id": user_id,
                "error": "User not found",
                "available_features": [],
                "tier": "unknown"
            }

        user_tier = FeatureTier(user.subscription_tier.value)
        available_features = []

        for feature, tier_access in FEATURE_ACCESS_MATRIX.items():
            if tier_access.get(user_tier, False):
                available_features.append(feature.value)

        # Get usage information for premium features
        usage_info = {}
        premium_features = [f.value for f in Feature if not FEATURE_ACCESS_MATRIX[f][FeatureTier.FREE]]

        for feature_name in premium_features:
            usage_data = self.check_usage_limit(db, user_id, feature_name)
            usage_info[feature_name] = {
                "available": usage_data["limit_exceeded"] is False,
                "usage_count": usage_data["usage_count"],
                "daily_limit": usage_data["limit"],
                "remaining": usage_data["remaining"]
            }

        return {
            "user_id": user_id,
            "tier": user_tier.value,
            "available_features": available_features,
            "feature_usage": usage_info,
            "total_features_available": len(available_features)
        }

    def get_premium_features_for_tier(self, tier: SubscriptionTier) -> List[str]:
        """
        Get list of premium features available for a specific tier
        """
        tier_enum = FeatureTier(tier.value)
        premium_features = []

        for feature, tier_access in FEATURE_ACCESS_MATRIX.items():
            if tier_access.get(tier_enum, False) and not tier_access.get(FeatureTier.FREE, False):
                premium_features.append(feature.value)

        return premium_features

    def check_zero_llm_compliance(self, codebase_path: str) -> Dict[str, Any]:
        """
        Check that the codebase complies with Zero-Backend-LLM principle
        """
        import os
        import re

        llm_indicators = [
            r'openai\.',
            r'anthropic\.',
            r'cohere\.',
            r'transformers\.',
            r'huggingface\.',
            r'langchain\.',
            r'llama_index\.',
            r'gpt',
            r'chatgpt',
            r'claude',
            r'gemini',
            r'embedding',
            r'embeddings',
            r'rag',
            r'vector',
            r'pinecone',
            r'weaviate',
            r'chromadb'
        ]

        violations = []
        total_files_scanned = 0

        for root, dirs, files in os.walk(codebase_path):
            # Skip common directories that shouldn't be scanned
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv']]

            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        total_files_scanned += 1

                        for pattern in llm_indicators:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            if matches:
                                violations.append({
                                    "file": file_path,
                                    "pattern": pattern,
                                    "matches": len(matches),
                                    "line_numbers": self._find_line_numbers(content, pattern)
                                })
                    except Exception as e:
                        print(f"Error scanning file {file_path}: {e}")

        return {
            "compliant": len(violations) == 0,
            "total_files_scanned": total_files_scanned,
            "violations_count": len(violations),
            "violations": violations,
            "message": f"Codebase has {'no' if len(violations) == 0 else 'some'} LLM API violations" if total_files_scanned > 0 else "No Python files found to scan"
        }

    def _find_line_numbers(self, content: str, pattern: str) -> list:
        """
        Find line numbers where a pattern occurs in content
        """
        lines = content.split('\n')
        line_numbers = []

        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                line_numbers.append(i)

        return line_numbers[:5]  # Return first 5 line numbers to avoid too much output

    def upgrade_user_subscription(self, db: Session, user_id: uuid.UUID, new_tier: SubscriptionTier) -> Dict[str, Any]:
        """
        Upgrade user subscription to a new tier
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {
                "success": False,
                "message": "User not found",
                "user_id": user_id
            }

        old_tier = user.subscription_tier

        # Update subscription
        user.subscription_tier = new_tier
        user.updated_at = datetime.utcnow()

        try:
            db.commit()
            return {
                "success": True,
                "user_id": user_id,
                "old_tier": old_tier.value,
                "new_tier": new_tier.value,
                "message": f"Subscription upgraded from {old_tier.value} to {new_tier.value}"
            }
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "message": f"Error upgrading subscription: {str(e)}",
                "user_id": user_id
            }

    def get_usage_statistics(self, db: Session, feature_name: str = None) -> Dict[str, Any]:
        """
        Get usage statistics for premium features
        """
        from models.usage_tracking import UsageTracking

        query = db.query(UsageTracking)

        if feature_name:
            query = query.filter(UsageTracking.feature_name == feature_name)

        usage_records = query.all()

        stats = {
            "total_records": len(usage_records),
            "by_feature": {},
            "by_user": {},
            "by_date": {}
        }

        for record in usage_records:
            # Count by feature
            feature = record.feature_name
            if feature not in stats["by_feature"]:
                stats["by_feature"][feature] = 0
            stats["by_feature"][feature] += record.usage_count

            # Count by user
            user_id = str(record.user_id)
            if user_id not in stats["by_user"]:
                stats["by_user"][user_id] = 0
            stats["by_user"][user_id] += record.usage_count

            # Count by date
            date_str = record.date_recorded.isoformat()
            if date_str not in stats["by_date"]:
                stats["by_date"][date_str] = 0
            stats["by_date"][date_str] += record.usage_count

        return stats