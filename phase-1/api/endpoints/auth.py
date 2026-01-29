from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import uuid
from typing import Dict, Any
from database import get_db
from services.subscription_service import SubscriptionService
from middleware.auth import get_current_user, create_access_token
from models.user import User

router = APIRouter()

@router.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """User login endpoint"""
    # In a real implementation, you'd verify credentials against a database
    # For now, we'll simulate authentication
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # In a real system, you'd verify the password hash here
    # For now, we'll assume the password is correct
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "subscription_tier": user.subscription_tier.value if user.subscription_tier else "free"
    }


@router.get("/auth/me")
def get_current_user_info(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    subscription_service = SubscriptionService()
    feature_access = subscription_service.get_user_feature_access(db, current_user.id)

    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "subscription_tier": current_user.subscription_tier.value if current_user.subscription_tier else "free",
        "subscription_status": current_user.subscription_status.value if current_user.subscription_status else "inactive",
        "feature_access": feature_access["features"],
        "last_active": current_user.last_active
    }


@router.get("/auth/access/{content_id}")
def check_content_access(
    content_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Check if user has access to specific content"""
    subscription_service = SubscriptionService()
    access_result = subscription_service.check_content_access(db, current_user.id, content_id)

    return access_result


@router.get("/auth/access")
def get_user_access(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get user's overall access information"""
    subscription_service = SubscriptionService()

    # Get subscription verification
    subscription_info = subscription_service.verify_user_subscription(db, current_user.id)

    # Get feature access
    feature_access = subscription_service.get_user_feature_access(db, current_user.id)

    # Get usage limits
    usage_limits = subscription_service.get_usage_limits(db, current_user.id)

    return {
        "user_id": current_user.id,
        "subscription_info": subscription_info,
        "feature_access": feature_access.get("features", {}),
        "usage_limits": usage_limits,
        "access_granted": subscription_info["subscription_valid"]
    }