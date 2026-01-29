from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from database import get_db
from services.content_service import ContentService
from services.premium_service import PremiumService
from middleware.premium_check import premium_required, track_usage
from schemas.learning_schemas import (
    AdaptiveLearningRequest,
    AdaptiveLearningResponse,
    PremiumAccessCheck
)

router = APIRouter()
content_service = ContentService()
premium_service = PremiumService()

@router.get("/content/{content_id}")
@premium_required("content_access")
@track_usage("content_access")
async def get_content(
    content_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve content by ID with access control
    """
    try:
        content_uuid = uuid.UUID(content_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid content ID format"
        )

    # Verify user has access to this content
    content = content_service.get_content_by_id(db, content_uuid)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    # Check if content exists in R2
    if not content_service.check_content_exists_in_r2(content.r2_key):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content file not found in storage"
        )

    # Generate presigned URL for content access
    presigned_url = content_service.get_presigned_url(content.r2_key)

    return {
        "id": content.id,
        "title": content.title,
        "content_type": content.content_type.value,
        "file_size": content.file_size,
        "download_url": presigned_url,
        "metadata": content.content_metadata,
        "created_at": content.created_at
    }


@router.get("/content/{content_id}/stream")
@premium_required("content_streaming")
@track_usage("content_streaming")
async def stream_content(
    content_id: str,
    db: Session = Depends(get_db)
):
    """
    Stream content directly from R2 storage
    """
    try:
        content_uuid = uuid.UUID(content_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid content ID format"
        )

    content = content_service.get_content_by_id(db, content_uuid)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    # Check access and stream content
    content_bytes = content_service.get_content_from_r2(content.r2_key)
    if not content_bytes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content file not found in storage"
        )

    # Return content for streaming
    return {
        "content_id": content.id,
        "title": content.title,
        "content_type": content.content_type.value,
        "size": len(content_bytes),
        "content": content_bytes.decode('utf-8') if isinstance(content_bytes, bytes) else content_bytes
    }


@router.get("/courses/{course_id}/chapters")
@premium_required("course_navigation")
@track_usage("course_navigation")
async def get_course_chapters(
    course_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all chapters/sections in a course
    """
    try:
        course_uuid = uuid.UUID(course_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )

    # Get all content for the course (chapters/sections)
    course_content = content_service.get_course_content(db, course_uuid)

    return {
        "course_id": course_uuid,
        "chapters": [
            {
                "id": content.id,
                "title": content.title,
                "content_type": content.content_type.value,
                "position": content.position if hasattr(content, 'position') else idx,
                "created_at": content.created_at
            }
            for idx, content in enumerate(course_content)
        ],
        "total_chapters": len(course_content)
    }


@router.get("/courses/{course_id}/next")
@premium_required("course_navigation")
@track_usage("course_navigation")
async def get_next_chapter(
    course_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the next chapter/section based on user's progress in the course
    """
    try:
        course_uuid = uuid.UUID(course_id)
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course or user ID format"
        )

    from services.navigation_service import NavigationService
    nav_service = NavigationService()

    next_content = nav_service.get_next_content(db, user_uuid, course_uuid)

    if not next_content:
        return {
            "message": "No more content available - course completed!",
            "completed": True
        }

    return {
        "next_content": {
            "id": next_content.id,
            "title": next_content.title,
            "content_type": next_content.content_type.value,
            "position": nav_service.get_content_position(db, course_uuid, next_content.id)
        },
        "completed": False
    }


@router.post("/content/upload")
@premium_required("content_upload")
@track_usage("content_upload")
async def upload_content(
    file: UploadFile = File(...),
    course_id: str = Form(...),
    title: str = Form(...),
    content_type: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Upload new content to R2 storage
    """
    try:
        course_uuid = uuid.UUID(course_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )

    # Read file content
    file_content = await file.read()
    file_size = len(file_content)

    # Generate unique key for R2
    import hashlib
    content_hash = hashlib.md5(file_content).hexdigest()
    r2_key = f"course-{course_uuid}/content-{content_hash}.{file.filename.split('.')[-1]}"

    # Upload to R2
    try:
        content_service.upload_content_to_r2(
            file_content,
            r2_key,
            file.content_type or "application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload content: {str(e)}"
        )

    # Create content record in database
    content = content_service.create_content(
        db=db,
        course_id=course_uuid,
        title=title,
        content_type=content_type,
        r2_key=r2_key,
        file_size=file_size
    )

    return {
        "content_id": content.id,
        "title": content.title,
        "content_type": content.content_type.value,
        "file_size": content.file_size,
        "message": "Content uploaded successfully"
    }