from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from ..database import get_db
from ..services.progress_service import ProgressService
from ..middleware.auth import get_current_user
from ..schemas.progress_schemas import (
    UpdateProgressRequest,
    UpdateProgressResponse,
    GetUserProgressResponse,
    GetUserCourseProgressResponse
)

router = APIRouter()
progress_service = ProgressService()

@router.put("/content/{content_id}/progress", response_model=UpdateProgressResponse)
def update_content_progress(
    content_id: str,
    request: UpdateProgressRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update progress for a specific content item
    """
    try:
        content_uuid = uuid.UUID(content_id)
        user_uuid = current_user.id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid content ID format"
        )

    try:
        progress = progress_service.update_content_progress(
            db,
            user_uuid,
            content_uuid,
            request.status,
            request.completion_percentage,
            request.time_spent_seconds
        )

        return UpdateProgressResponse(
            user_id=user_uuid,
            content_id=content_uuid,
            status=progress.status.value,
            completion_percentage=float(progress.completion_percentage) if progress.completion_percentage else 0,
            time_spent_seconds=progress.time_spent_seconds or 0,
            updated_at=progress.updated_at,
            message="Progress updated successfully"
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


@router.get("/users/{user_id}/progress", response_model=GetUserProgressResponse)
def get_user_progress(
    user_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get overall progress for a user
    """
    try:
        requested_user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Only allow users to access their own progress or admins to access others
    if requested_user_uuid != current_user.id and not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to other user's progress"
        )

    progress_data = progress_service.get_user_progress(db, requested_user_uuid)

    return GetUserProgressResponse(
        user_id=requested_user_uuid,
        total_content=progress_data["total_content"],
        completed_content=progress_data["completed_content"],
        in_progress_content=progress_data["in_progress_content"],
        not_started_content=progress_data["not_started_content"],
        overall_completion_percentage=progress_data["overall_completion_percentage"],
        current_streak_days=progress_data["current_streak_days"],
        last_active=progress_data["last_active"],
        progress_distribution=progress_data["progress_distribution"]
    )


@router.get("/courses/{course_id}/progress", response_model=GetUserCourseProgressResponse)
def get_course_progress(
    course_id: str,
    user_id: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get progress for a specific course
    """
    try:
        course_uuid = uuid.UUID(course_id)
        user_uuid = uuid.UUID(user_id) if user_id else current_user.id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course or user ID format"
        )

    # Only allow users to access their own progress or admins to access others
    if user_uuid != current_user.id and not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to other user's progress"
        )

    course_progress = progress_service.get_course_progress(db, user_uuid, course_uuid)

    return GetUserCourseProgressResponse(
        user_id=user_uuid,
        course_id=course_uuid,
        total_content_items=course_progress["total_content_items"],
        completed_items=course_progress["completed_items"],
        completion_percentage=course_progress["completion_percentage"],
        content_progress=course_progress["content_progress"],
        milestones=course_progress["milestones"],
        recommendations=course_progress["recommendations"]
    )


@router.get("/users/{user_id}/streak")
def get_user_streak(
    user_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get user's learning streak
    """
    try:
        requested_user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Only allow users to access their own streak or admins to access others
    if requested_user_uuid != current_user.id and not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to other user's streak"
        )

    streak_data = progress_service.get_user_streak(db, requested_user_uuid)

    return {
        "user_id": requested_user_uuid,
        "current_streak_days": streak_data["current_streak"],
        "longest_streak_days": streak_data["longest_streak"],
        "last_learning_date": streak_data["last_learning_date"],
        "message": f"Current streak: {streak_data['current_streak']} days"
    }


@router.get("/users/{user_id}/analytics")
def get_user_analytics(
    user_id: str,
    course_id: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get detailed learning analytics for a user
    """
    try:
        requested_user_uuid = uuid.UUID(user_id)
        course_uuid = uuid.UUID(course_id) if course_id else None
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user or course ID format"
        )

    # Only allow users to access their own analytics or admins to access others
    if requested_user_uuid != current_user.id and not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to other user's analytics"
        )

    analytics = progress_service.get_user_learning_analytics(
        db, requested_user_uuid, course_uuid
    )

    return analytics