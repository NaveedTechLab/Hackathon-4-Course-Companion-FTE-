from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from database import get_db
from models.content import Content, ContentType
from services.content_service import ContentService
from middleware.auth import get_current_user
from schemas.content_schemas import ContentResponse

router = APIRouter()

@router.get("/content/{content_id}", response_model=ContentResponse)
def get_content(
    content_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Retrieve content metadata and download URL"""
    content_service = ContentService()
    content = content_service.get_content_by_id(db, content_id)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    # Check if user has access to this content
    # For now, we assume all authenticated users can access all content
    # In a real system, you'd check subscription and access permissions

    return {
        "id": content.id,
        "title": content.title,
        "content_type": content.content_type.value,
        "file_size": content.file_size,
        "created_at": content.created_at,
        "updated_at": content.updated_at,
        "download_url": content_service.get_presigned_url(content.r2_key)
    }


@router.get("/content/{content_id}/stream")
def stream_content(
    content_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Stream content directly from R2"""
    content_service = ContentService()
    content = content_service.get_content_by_id(db, content_id)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    # Check if user has access to this content
    # For now, we assume all authenticated users can access all content
    # In a real system, you'd check subscription and access permissions

    # Return presigned URL for direct download
    presigned_url = content_service.get_presigned_url(content.r2_key)
    return {"stream_url": presigned_url}


@router.post("/content/upload")
def upload_content(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Upload content to R2 storage"""
    content_service = ContentService()

    # Read file content
    file_content = file.file.read()

    # Generate a unique key for R2 storage
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'bin'
    r2_key = f"content/{uuid.uuid4()}.{file_extension}"

    # Upload to R2
    try:
        download_url = content_service.upload_content_to_r2(
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
        course_id=uuid.uuid4(),  # This would come from the request in a real implementation
        title=file.filename,
        content_type=file.content_type or "application/octet-stream",
        r2_key=r2_key,
        file_size=len(file_content)
    )

    return {
        "content_id": content.id,
        "title": content.title,
        "download_url": download_url,
        "message": "Content uploaded successfully"
    }