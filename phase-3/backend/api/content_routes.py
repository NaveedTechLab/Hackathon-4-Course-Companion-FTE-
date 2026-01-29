from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import uuid
from ..database import get_db
from ..services.content_service import ContentService
from ..middleware.auth import get_current_user
from ..schemas.content_schemas import ContentResponse

router = APIRouter()
content_service = ContentService()

@router.get("/content/{content_id}", response_model=ContentResponse)
def get_content(
    content_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieve content metadata and download URL
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

    # Check if user has access to this content
    # For now, assume all enrolled users can access content
    # In a real implementation, this would check enrollment and access permissions

    # Generate presigned URL for content access
    download_url = content_service.get_presigned_url(content.r2_key)

    return ContentResponse(
        id=content.id,
        title=content.title,
        content_type=content.content_type.value,
        file_size=content.file_size,
        download_url=download_url,
        content_metadata=content.content_metadata,
        created_at=content.created_at
    )


@router.get("/content/{content_id}/stream")
def stream_content(
    content_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Stream content directly from R2
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

    # Check access permissions
    # In a real implementation, this would verify user has access to this content

    # Get content from R2
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


@router.get("/courses/{course_id}/content")
def get_course_content(
    course_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all content for a specific course
    """
    try:
        course_uuid = uuid.UUID(course_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )

    course_content = content_service.get_course_content(db, course_uuid)

    return {
        "course_id": course_uuid,
        "content_items": [
            {
                "id": content.id,
                "title": content.title,
                "content_type": content.content_type.value,
                "position": content.position,
                "created_at": content.created_at
            }
            for content in course_content
        ],
        "total_items": len(course_content)
    }