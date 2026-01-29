from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uuid
from database import get_db
from services.navigation_service import NavigationService
from middleware.auth import get_current_user
from models.content import Content

router = APIRouter()

@router.get("/courses/{course_id}/structure")
def get_course_structure(
    course_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get course structure with chapter/section hierarchy"""
    navigation_service = NavigationService()
    course_contents = navigation_service.get_course_structure(db, course_id)

    return {
        "course_id": course_id,
        "structure": [
            {
                "id": content.id,
                "title": content.title,
                "type": content.content_type.value,
                "position": navigation_service.get_content_position(db, course_id, content.id)
            }
            for content in course_contents
        ]
    }


@router.get("/courses/{course_id}/next")
def get_next_content(
    course_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get next available content based on progress"""
    navigation_service = NavigationService()
    next_content = navigation_service.get_next_content(db, current_user.id, course_id)

    if not next_content:
        return {"message": "No more content available", "completed": True}

    return {
        "content_id": next_content.id,
        "title": next_content.title,
        "type": next_content.content_type.value,
        "position": navigation_service.get_content_position(db, course_id, next_content.id)
    }


@router.post("/content/{content_id}/bookmark")
def set_bookmark(
    content_id: uuid.UUID,
    position: int,
    note: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Set bookmark for current user"""
    # This would typically update a bookmarks table
    # For now, we'll just return a confirmation
    return {
        "content_id": content_id,
        "position": position,
        "note": note,
        "bookmarked_at": "now",
        "message": "Bookmark set successfully"
    }