from functools import wraps
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import jwt
import uuid
from datetime import datetime, timedelta
from database import get_db
from config import settings
from models.user import User
from services.premium_service import PremiumService

security = HTTPBearer()
premium_service = PremiumService()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """
    Get current user from JWT token
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

        user_uuid = uuid.UUID(user_id)
        user = db.query(User).filter(User.id == user_uuid).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID format in token")

def premium_required(feature_name: str):
    """
    Decorator to require premium access for specific features
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract database session and current user from function arguments
            db = None
            current_user = None

            # Find db session in kwargs or args
            for arg in kwargs.values():
                if isinstance(arg, Session):
                    db = arg
                    break

            if db is None:
                for arg in args:
                    if isinstance(arg, Session):
                        db = arg
                        break

            # Find current_user in kwargs or args
            if 'current_user' in kwargs:
                current_user = kwargs['current_user']
            elif 'user' in kwargs:
                current_user = kwargs['user']
            else:
                for arg in args:
                    if hasattr(arg, 'id') and hasattr(arg, 'subscription_tier'):
                        current_user = arg
                        break

            if not db or not current_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database session or user context not available"
                )

            # Check premium access
            access_result = premium_service.check_feature_access(db, current_user.id, feature_name)

            if not access_result["has_access"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=access_result["message"]
                )

            # Check usage limits
            usage_result = premium_service.check_usage_limit(db, current_user.id, feature_name)
            if usage_result["limit_exceeded"]:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=usage_result["message"]
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
            # Extract database session and current user from function arguments
            db = None
            current_user = None

            # Find db session in kwargs or args
            for arg in kwargs.values():
                if isinstance(arg, Session):
                    db = arg
                    break

            if db is None:
                for arg in args:
                    if isinstance(arg, Session):
                        db = arg
                        break

            # Find current_user in kwargs or args
            if 'current_user' in kwargs:
                current_user = kwargs['current_user']
            elif 'user' in kwargs:
                current_user = kwargs['user']
            else:
                for arg in args:
                    if hasattr(arg, 'id') and hasattr(arg, 'subscription_tier'):
                        current_user = arg
                        break

            if db and current_user:
                try:
                    # Track the usage
                    premium_service.track_feature_usage(db, current_user.id, feature_name)
                except Exception as e:
                    # Log the error but don't block the function execution
                    print(f"Error tracking usage for {feature_name}: {e}")

            # Call the original function
            result = func(*args, **kwargs)

            # Track usage after successful execution
            if db and current_user:
                try:
                    premium_service.track_feature_usage(db, current_user.id, feature_name)
                except Exception as e:
                    print(f"Error tracking usage for {feature_name}: {e}")

            return result

        return wrapper
    return decorator

def check_subscription_tier(required_tier: str = "premium"):
    """
    Decorator to check if user has a specific subscription tier or higher
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract database session and current user from function arguments
            db = None
            current_user = None

            # Find db session in kwargs or args
            for arg in kwargs.values():
                if isinstance(arg, Session):
                    db = arg
                    break

            if db is None:
                for arg in args:
                    if isinstance(arg, Session):
                        db = arg
                        break

            # Find current_user in kwargs or args
            if 'current_user' in kwargs:
                current_user = kwargs['current_user']
            elif 'user' in kwargs:
                current_user = kwargs['user']
            else:
                for arg in args:
                    if hasattr(arg, 'id') and hasattr(arg, 'subscription_tier'):
                        current_user = arg
                        break

            if not db or not current_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database session or user context not available"
                )

            # Define tier hierarchy
            tier_hierarchy = {
                "free": 0,
                "premium": 1,
                "enterprise": 2
            }

            current_tier_level = tier_hierarchy.get(current_user.subscription_tier.value, 0)
            required_tier_level = tier_hierarchy.get(required_tier.lower(), 0)

            if current_tier_level < required_tier_level:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Feature requires {required_tier} subscription tier or higher"
                )

            # Call the original function
            return func(*args, **kwargs)

        return wrapper
    return decorator

# Example usage:
#
# @router.get("/premium-feature")
# @premium_required("adaptive_learning")
# @track_usage("adaptive_learning")
# @check_subscription_tier("premium")
# async def get_premium_feature(
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     # Implementation here
#     pass