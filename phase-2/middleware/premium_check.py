from functools import wraps
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import jwt
from services.premium_service import PremiumService
from database import get_db
from config import settings
from models.subscription import SubscriptionFeature
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer()

def require_premium_access(feature: SubscriptionFeature):
    """
    Dependency that checks if user has premium access to a specific feature
    Returns user_id if access is granted
    """
    def dependency(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
    ) -> UUID:
        try:
            token = credentials.credentials
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            user_id_str: str = payload.get("sub")
            if user_id_str is None:
                raise HTTPException(status_code=401, detail="Could not validate credentials")

            user_id = UUID(user_id_str)

            # Check premium access
            premium_service = PremiumService()
            access_result = premium_service.verify_premium_access(db, user_id, feature.value)

            if not access_result.get("access_granted", False):
                raise HTTPException(
                    status_code=403,
                    detail=f"Premium access required for feature: {feature.value}"
                )

            return user_id

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid user ID format")

    return dependency

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UUID:
    """
    Extract user ID from JWT token
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return UUID(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def premium_required(feature_name: Optional[str] = None):
    """
    Decorator to require premium access for specific features
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract database session and user ID from the function arguments
            db = None
            user_id = None

            # Look for db session in kwargs or args
            for arg in kwargs.values():
                if isinstance(arg, Session):
                    db = arg
                    break

            if db is None:
                for arg in args:
                    if isinstance(arg, Session):
                        db = arg
                        break

            # Look for user_id in kwargs or args
            if 'user_id' in kwargs:
                user_id = kwargs['user_id']
            elif 'current_user_id' in kwargs:
                user_id = kwargs['current_user_id']
            else:
                # Look for user_id in args
                for arg in args:
                    if isinstance(arg, UUID):
                        user_id = arg
                        break

            if not db or not user_id:
                raise HTTPException(
                    status_code=500,
                    detail="Database session or user ID not available in function context"
                )

            # Check premium access
            premium_service = PremiumService()

            # If a specific feature name is provided, check access to that feature
            if feature_name:
                access_result = premium_service.verify_premium_access(db, user_id, feature_name)

                if not access_result["access_granted"]:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Premium access required for feature: {feature_name}. {access_result['message']}"
                    )
            else:
                # Just check general premium access
                subscription_info = premium_service.check_user_subscription_status(db, user_id)

                if not subscription_info["has_premium_access"]:
                    raise HTTPException(
                        status_code=403,
                        detail="Premium subscription required for this feature"
                    )

            # Call the original function
            return func(*args, **kwargs)

        return wrapper
    return decorator

def subscription_required(min_tier: str = "premium"):
    """
    Decorator to require a specific subscription tier
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract database session and user ID from the function arguments
            db = None
            user_id = None

            # Look for db session in kwargs or args
            for arg in kwargs.values():
                if isinstance(arg, Session):
                    db = arg
                    break

            if db is None:
                for arg in args:
                    if isinstance(arg, Session):
                        db = arg
                        break

            # Look for user_id in kwargs or args
            if 'user_id' in kwargs:
                user_id = kwargs['user_id']
            elif 'current_user_id' in kwargs:
                user_id = kwargs['current_user_id']
            else:
                # Look for user_id in args
                for arg in args:
                    if isinstance(arg, UUID):
                        user_id = arg
                        break

            if not db or not user_id:
                raise HTTPException(
                    status_code=500,
                    detail="Database session or user ID not available in function context"
                )

            # Check subscription tier
            premium_service = PremiumService()
            subscription_info = premium_service.check_user_subscription_status(db, user_id)

            tier_levels = {
                "free": 0,
                "premium": 1,
                "enterprise": 2
            }

            current_tier_level = tier_levels.get(subscription_info["tier"], 0)
            required_tier_level = tier_levels.get(min_tier, 1)

            if current_tier_level < required_tier_level:
                raise HTTPException(
                    status_code=403,
                    detail=f"Subscription tier '{min_tier}' or higher required for this feature"
                )

            # Call the original function
            return func(*args, **kwargs)

        return wrapper
    return decorator

def track_usage(feature_name: str):
    """
    Decorator to track usage of premium features
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract database session and user ID from the function arguments
            db = None
            user_id = None

            # Look for db session in kwargs or args
            for arg in kwargs.values():
                if isinstance(arg, Session):
                    db = arg
                    break

            if db is None:
                for arg in args:
                    if isinstance(arg, Session):
                        db = arg
                        break

            # Look for user_id in kwargs or args
            if 'user_id' in kwargs:
                user_id = kwargs['user_id']
            elif 'current_user_id' in kwargs:
                user_id = kwargs['current_user_id']
            else:
                # Look for user_id in args
                for arg in args:
                    if isinstance(arg, UUID):
                        user_id = arg
                        break

            if db and user_id:
                # Track usage before calling the function
                premium_service = PremiumService()
                usage_info = premium_service.check_usage_limit(db, user_id, feature_name)

                if usage_info["limit_exceeded"]:
                    raise HTTPException(
                        status_code=429,
                        detail=f"Usage limit exceeded for {feature_name}. Limit: {usage_info['usage_limit']} per day"
                    )

            # Call the original function
            result = func(*args, **kwargs)

            # Track usage after successful execution
            if db and user_id:
                try:
                    premium_service = PremiumService()
                    premium_service._log_access_attempt(db, user_id, feature_name, True)
                except Exception as e:
                    logger.error(f"Failed to log usage for feature {feature_name}: {e}")

            return result

        return wrapper
    return decorator

# Example usage:
#
# @router.get("/premium-feature")
# @premium_required("adaptive_learning")
# @track_usage("adaptive_learning")
# async def get_adaptive_learning_path(
#     user_id: UUID = Depends(get_current_user_id),
#     db: Session = Depends(get_db)
# ):
#     # Implementation here
#     pass