from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from ..database import get_db
from ..services.navigation_service import NavigationService
from ..middleware.auth import get_current_user
from ..schemas.navigation_schemas import CourseStructureResponse, NextContentResponse

router = APIRouter()
navigation_service = NavigationService()

@router.get("/courses/{course_id}/structure", response_model=CourseStructureResponse)
def get_course_structure(
    course_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get the hierarchical structure of a course
    """
    try:
        course_uuid = uuid.UUID(course_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )

    course_structure = navigation_service.get_course_structure(db, course_uuid)

    if not course_structure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return CourseStructureResponse(
        course_id=course_uuid,
        title=course_structure["title"],
        chapters=course_structure["chapters"],
        total_chapters=course_structure["total_chapters"]
    )


@router.get("/courses/{course_id}/next", response_model=NextContentResponse)
def get_next_content(
    course_id: str,
    user_id: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get the next content item based on user's progress in the course
    """
    try:
        course_uuid = uuid.UUID(course_id)
        user_uuid = uuid.UUID(user_id) if user_id else current_user.id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course or user ID format"
        )

    next_content = navigation_service.get_next_content(db, user_uuid, course_uuid)

    if not next_content:
        return NextContentResponse(
            course_id=course_uuid,
            user_id=user_uuid,
            has_next_content=False,
            message="No more content available - course completed or no content found"
        )

    return NextContentResponse(
        course_id=course_uuid,
        user_id=user_uuid,
        has_next_content=True,
        next_content_id=next_content["id"],
        next_content_title=next_content["title"],
        next_content_type=next_content["content_type"],
        message="Next content available"
    )


@router.get("/courses/{course_id}/prev")
def get_prev_content(
    course_id: str,
    content_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get the previous content item in the course sequence
    """
    try:
        course_uuid = uuid.UUID(course_id)
        content_uuid = uuid.UUID(content_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course or content ID format"
        )

    prev_content = navigation_service.get_prev_content(db, course_uuid, content_uuid)

    if not prev_content:
        return {
            "course_id": course_uuid,
            "current_content_id": content_uuid,
            "has_prev_content": False,
            "message": "No previous content available"
        }

    return {
        "course_id": course_uuid,
        "current_content_id": content_uuid,
        "has_prev_content": True,
        "prev_content_id": prev_content["id"],
        "prev_content_title": prev_content["title"],
        "message": "Previous content available"
    }


@router.post("/content/{content_id}/bookmark")
def set_bookmark(
    content_id: str,
    position: int,
    note: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Set bookmark for current content position
    """
    try:
        content_uuid = uuid.UUID(content_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid content ID format"
        )

    bookmark_result = navigation_service.set_bookmark(
        db, current_user.id, content_uuid, position, note
    )

    return {
        "user_id": current_user.id,
        "content_id": content_uuid,
        "position": position,
        "note": note,
        "bookmarked_at": bookmark_result["bookmarked_at"],
        "message": "Bookmark set successfully"
    }


@router.get("/users/{user_id}/bookmarks")
def get_user_bookmarks(
    user_id: str,
    course_id: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get user's bookmarks, optionally filtered by course
    """
    try:
        user_uuid = uuid.UUID(user_id)
        course_uuid = uuid.UUID(course_id) if course_id else None
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user or course ID format"
        )

    # Only allow users to access their own bookmarks
    if user_uuid != current_user.id and not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to other user's bookmarks"
        )

    bookmarks = navigation_service.get_user_bookmarks(db, user_uuid, course_uuid)

    return {
        "user_id": user_uuid,
        "course_id": course_uuid,
        "bookmarks": bookmarks,
        "total_bookmarks": len(bookmarks)
    }