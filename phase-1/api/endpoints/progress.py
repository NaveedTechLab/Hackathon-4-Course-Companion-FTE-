from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from uuid import UUID
import uuid
from database import get_db
from services.progress_service import ProgressService
from services.premium_service import PremiumService
from middleware.premium_check import premium_required, track_usage
from schemas.learning_schemas import (
    ProgressTrackingRequest,
    ProgressTrackingResponse,
    CostSummaryResponse
)

router = APIRouter()
progress_service = ProgressService()
premium_service = PremiumService()

@router.put("/progress")
@premium_required("progress_tracking")
@track_usage("progress_tracking")
async def update_progress(
    request: ProgressTrackingRequest,
    db: Session = Depends(get_db)
):
    """
    Update progress for a specific content item
    """
    try:
        user_uuid = uuid.UUID(request.user_id)
        content_uuid = uuid.UUID(request.content_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user or content ID format"
        )

    # Verify user has access to update progress
    access_check = premium_service.verify_premium_access(db, user_uuid, "progress_tracking")
    if not access_check["access_granted"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=access_check["message"]
        )

    try:
        # Update progress with validation
        result = progress_service.update_progress_with_validation(
            db,
            user_uuid,
            content_uuid,
            request.status,
            request.completion_percentage,
            request.time_spent_seconds
        )

        return ProgressTrackingResponse(
            user_id=user_uuid,
            content_id=content_uuid,
            status=request.status,
            completion_percentage=request.completion_percentage,
            time_spent_seconds=request.time_spent_seconds,
            updated_at=datetime.utcnow(),
            message=result["message"]
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating progress: {str(e)}"
        )


@router.get("/progress/{user_id}")
@premium_required("progress_viewing")
@track_usage("progress_viewing")
async def get_user_progress(
    user_id: str,
    course_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Get user's overall progress summary
    """
    try:
        user_uuid = uuid.UUID(user_id)
        course_uuid = uuid.UUID(course_id) if course_id else None
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user or course ID format"
        )

    try:
        progress_summary = progress_service.get_user_progress(db, user_uuid, course_uuid)

        return {
            "user_id": user_uuid,
            "course_id": course_uuid,
            "progress_summary": progress_summary
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving progress: {str(e)}"
        )


@router.get("/progress/{user_id}/course/{course_id}")
@premium_required("course_progress_viewing")
@track_usage("course_progress_viewing")
async def get_course_progress(
    user_id: str,
    course_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed progress for a specific course
    """
    try:
        user_uuid = uuid.UUID(user_id)
        course_uuid = uuid.UUID(course_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user or course ID format"
        )

    try:
        course_progress = progress_service.get_course_progress_summary(db, user_uuid, course_uuid)

        return {
            "user_id": user_uuid,
            "course_id": course_uuid,
            "course_progress": course_progress
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving course progress: {str(e)}"
        )


@router.get("/progress/{user_id}/insights")
@premium_required("learning_insights")
@track_usage("learning_insights")
async def get_learning_insights(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive learning insights for a user
    """
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    try:
        insights = progress_service.get_user_learning_insights(db, user_uuid)

        return {
            "user_id": user_uuid,
            "learning_insights": insights
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving learning insights: {str(e)}"
        )


@router.get("/progress/{user_id}/streak")
@premium_required("streak_tracking")
@track_usage("streak_tracking")
async def get_learning_streak(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get user's current learning streak
    """
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    try:
        # Calculate streak using the same method as in progress service
        streak = progress_service._calculate_current_streak(db, user_uuid)

        return {
            "user_id": user_uuid,
            "current_streak_days": streak,
            "message": f"Current learning streak: {streak} days"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating learning streak: {str(e)}"
        )


@router.get("/progress/{user_id}/cost-summary")
@premium_required("cost_tracking")
@track_usage("cost_tracking")
async def get_cost_summary(
    user_id: str,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """
    Get cost summary for a user's progress tracking usage
    """
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # This would typically integrate with the token tracking system
    # For now, return a mock implementation showing the structure

    from datetime import datetime, timedelta
    import random

    # Mock cost calculation based on feature usage
    total_tokens = random.randint(10000, 50000)  # Random token usage for demo
    cost_per_token = 0.000002  # $0.002 per 1K tokens (mock value)
    total_cost = total_tokens * cost_per_token

    return CostSummaryResponse(
        user_id=user_uuid,
        total_tokens_used=total_tokens,
        total_cost=round(total_cost, 6),
        feature_costs={
            "progress_tracking": round(total_cost * 0.3, 6),  # 30% of costs
            "course_navigation": round(total_cost * 0.2, 6),  # 20% of costs
            "adaptive_learning": round(total_cost * 0.5, 6)   # 50% of costs
        },
        period_start=datetime.utcnow() - timedelta(days=30) if not start_date else datetime.fromisoformat(start_date),
        period_end=datetime.utcnow(),
        message=f"Cost summary for progress tracking features"
    )


@router.get("/progress/feature-info")
async def get_progress_feature_info(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get information about progress tracking feature access
    """
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    access_info = premium_service.verify_premium_access(db, user_uuid, "progress_tracking")

    return {
        "user_id": user_uuid,
        "feature_name": "progress_tracking",
        "has_access": access_info["access_granted"],
        "subscription_tier": access_info["subscription_tier"],
        "available_features": [
            "basic_progress_tracking",
            "course_completion_stats",
            "learning_streaks",
            "time_spent_tracking",
            "completion_percentages"
        ] if access_info["has_premium_access"] else ["basic_progress_tracking"],
        "message": access_info["message"]
    }

from datetime import datetime