from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from database import get_db
from services.premium_service import PremiumService
from services.learning_path_service import LearningPathService
from middleware.premium_check import premium_required, track_usage
from schemas.premium_schemas import (
    AdaptiveLearningRequest,
    AdaptiveLearningResponse,
    PremiumAccessCheck
)

router = APIRouter()

@router.post("/adaptive-learning/generate", response_model=AdaptiveLearningResponse)
@premium_required("adaptive_learning")
@track_usage("adaptive_learning")
async def generate_adaptive_learning_path(
    request: AdaptiveLearningRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a personalized learning path based on user data and performance
    """
    try:
        # Check if user has access to this premium feature
        premium_service = PremiumService()
        access_check = premium_service.verify_premium_access(
            db, request.user_id, "adaptive_learning"
        )

        if not access_check["access_granted"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=access_check["message"]
            )

        # Check usage limits
        if not premium_service.is_within_usage_limit(db, request.user_id, "adaptive_learning"):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Usage limit exceeded for adaptive learning feature"
            )

        # Generate adaptive learning path
        learning_path_service = LearningPathService()
        result = learning_path_service.generate_adaptive_path(
            db,
            request.user_id,
            request.course_id,
            request.current_progress,
            request.learning_objectives,
            request.content_preferences
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating adaptive learning path: {str(e)}"
        )


@router.get("/adaptive-learning/{user_id}/recommendations", response_model=List[AdaptiveLearningResponse])
@premium_required("adaptive_learning")
@track_usage("adaptive_learning")
async def get_user_learning_recommendations(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get learning recommendations for a user
    """
    try:
        # Check if user has access to this premium feature
        premium_service = PremiumService()
        access_check = premium_service.verify_premium_access(
            db, user_id, "adaptive_learning"
        )

        if not access_check["access_granted"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=access_check["message"]
            )

        # Get learning recommendations
        learning_path_service = LearningPathService()
        recommendations = learning_path_service.get_user_recommendations(db, user_id)

        return recommendations

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving learning recommendations: {str(e)}"
        )


@router.post("/adaptive-learning/{user_id}/adjust-path", response_model=AdaptiveLearningResponse)
@premium_required("adaptive_learning")
@track_usage("adaptive_learning")
async def adjust_learning_path(
    user_id: UUID,
    request: AdaptiveLearningRequest,
    db: Session = Depends(get_db)
):
    """
    Adjust an existing learning path based on new information
    """
    try:
        # Check if user has access to this premium feature
        premium_service = PremiumService()
        access_check = premium_service.verify_premium_access(
            db, user_id, "adaptive_learning"
        )

        if not access_check["access_granted"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=access_check["message"]
            )

        # Check usage limits
        if not premium_service.is_within_usage_limit(db, user_id, "adaptive_learning"):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Usage limit exceeded for adaptive learning feature"
            )

        # Adjust learning path
        learning_path_service = LearningPathService()
        result = learning_path_service.adjust_learning_path(
            db,
            user_id,
            request.course_id,
            request.current_progress,
            request.learning_objectives
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adjusting learning path: {str(e)}"
        )


@router.get("/adaptive-learning/{user_id}/progress-insights")
@premium_required("adaptive_learning")
@track_usage("adaptive_learning")
async def get_progress_insights(
    user_id: UUID,
    course_id: UUID = None,
    db: Session = Depends(get_db)
):
    """
    Get insights about user's learning progress and patterns
    """
    try:
        # Check if user has access to this premium feature
        premium_service = PremiumService()
        access_check = premium_service.verify_premium_access(
            db, user_id, "adaptive_learning"
        )

        if not access_check["access_granted"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=access_check["message"]
            )

        # Get progress insights
        learning_path_service = LearningPathService()
        insights = learning_path_service.get_progress_insights(
            db,
            user_id,
            course_id
        )

        return insights

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving progress insights: {str(e)}"
        )


@router.get("/adaptive-learning/feature-info", response_model=PremiumAccessCheck)
async def get_adaptive_learning_feature_info(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get information about adaptive learning feature access
    """
    try:
        premium_service = PremiumService()
        access_info = premium_service.verify_premium_access(
            db, user_id, "adaptive_learning"
        )

        return PremiumAccessCheck(
            user_id=user_id,
            has_premium_access=access_info["has_premium_access"],
            is_subscription_active=access_info["is_subscription_active"],
            subscription_tier=access_info["subscription_tier"],
            subscription_status=access_info["subscription_status"],
            access_granted=access_info["access_granted"],
            feature_name="adaptive_learning",
            feature_available=access_info.get("feature_available", False),
            message=access_info["message"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving feature info: {str(e)}"
        )