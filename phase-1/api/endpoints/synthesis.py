from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from uuid import UUID
import uuid
from database import get_db
from services.synthesis_service import SynthesisService
from services.premium_service import PremiumService
from middleware.premium_check import premium_required, track_usage
from schemas.learning_schemas import (
    SynthesisRequest,
    SynthesisResponse,
    PremiumAccessCheck
)

router = APIRouter()
synthesis_service = SynthesisService()
premium_service = PremiumService()

@router.post("/synthesis/connect-concepts", response_model=SynthesisResponse)
@premium_required("cross_chapter_synthesis")
@track_usage("cross_chapter_synthesis")
async def connect_concepts(
    request: SynthesisRequest,
    db: Session = Depends(get_db)
):
    """
    Generate connections across different chapters and concepts
    """
    try:
        user_uuid = uuid.UUID(request.user_id)
        course_uuid = uuid.UUID(request.course_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user or course ID format"
        )

    # Check if user has access to this premium feature
    access_check = premium_service.verify_premium_access(db, user_uuid, "cross_chapter_synthesis")
    if not access_check["access_granted"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=access_check["message"]
        )

    # Check usage limits
    usage_check = premium_service.check_usage_limit(db, user_uuid, "cross_chapter_synthesis")
    if usage_check["limit_exceeded"]:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Usage limit exceeded for cross-chapter synthesis feature"
        )

    try:
        # Generate cross-chapter synthesis
        synthesis_result = synthesis_service.generate_cross_chapter_synthesis(
            db,
            user_uuid,
            course_uuid,
            request.chapters,
            request.connection_depth,
            request.output_format
        )

        return SynthesisResponse(
            user_id=user_uuid,
            course_id=course_uuid,
            synthesis_report=synthesis_result["synthesis_report"],
            connections=synthesis_result["connections"],
            big_picture_insights=synthesis_result["big_picture_insights"],
            synthesis_exercises=synthesis_result["synthesis_exercises"],
            processing_time_ms=synthesis_result["processing_time_ms"]
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating synthesis: {str(e)}"
        )


@router.get("/synthesis/{course_id}/course-structure")
@premium_required("course_structure_synthesis")
@track_usage("course_structure_synthesis")
async def get_course_structure_synthesis(
    course_id: str,
    db: Session = Depends(get_db)
):
    """
    Get synthesis of the entire course structure and patterns
    """
    try:
        course_uuid = uuid.UUID(course_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )

    try:
        structure_synthesis = synthesis_service.get_course_structure_synthesis(db, course_uuid)

        return {
            "course_id": course_uuid,
            "structure_analysis": structure_synthesis["course_title"],
            "total_content_items": structure_synthesis["total_content_items"],
            "content_sequence": structure_synthesis["content_sequence"],
            "structural_patterns": structure_synthesis["structural_patterns"],
            "message": f"Course '{structure_synthesis['course_title']}' structure analysis complete"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing course structure: {str(e)}"
        )


@router.get("/synthesis/{course_id}/big-picture-insights")
@premium_required("big_picture_insights")
@track_usage("big_picture_insights")
async def get_big_picture_insights(
    course_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get big picture insights about the course and concept connections
    """
    try:
        course_uuid = uuid.UUID(course_id)
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course or user ID format"
        )

    # Get all content for the course
    from models.content import Content
    course_content = db.query(Content).filter(
        Content.course_id == course_uuid
    ).order_by(Content.created_at).all()

    # Get all connections in the course
    connections = synthesis_service._identify_connections(course_content, [], "deep")

    # Generate big picture insights
    big_picture_insights = synthesis_service._generate_big_picture_insights(course_content, connections)

    return {
        "user_id": user_uuid,
        "course_id": course_uuid,
        "insights_count": len(big_picture_insights),
        "big_picture_insights": big_picture_insights,
        "connection_count": len(connections),
        "thematic_connections": synthesis_service._get_thematic_connections(connections)
    }


@router.get("/synthesis/feature-info", response_model=PremiumAccessCheck)
async def get_synthesis_feature_info(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get information about synthesis feature access
    """
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    access_info = premium_service.verify_premium_access(db, user_uuid, "cross_chapter_synthesis")

    return PremiumAccessCheck(
        user_id=user_uuid,
        has_premium_access=access_info["has_premium_access"],
        is_subscription_active=access_info["is_subscription_active"],
        subscription_tier=access_info["subscription_tier"],
        subscription_status=access_info["subscription_status"],
        access_granted=access_info["access_granted"],
        feature_name="cross_chapter_synthesis",
        feature_available=access_info.get("feature_available", False),
        message=access_info["message"]
    )


@router.post("/synthesis/generate-exercises")
@premium_required("synthesis_exercises")
@track_usage("synthesis_exercises")
async def generate_synthesis_exercises(
    course_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Generate synthesis exercises that connect multiple concepts
    """
    try:
        course_uuid = uuid.UUID(course_id)
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course or user ID format"
        )

    # Get all content for the course
    from models.content import Content
    course_content = db.query(Content).filter(
        Content.course_id == course_uuid
    ).order_by(Content.created_at).all()

    # Get all connections in the course
    connections = synthesis_service._identify_connections(course_content, [], "deep")

    # Generate synthesis exercises based on connections
    exercises = synthesis_service._generate_synthesis_exercises(connections, course_content)

    return {
        "user_id": user_uuid,
        "course_id": course_uuid,
        "exercise_count": len(exercises),
        "exercises": exercises,
        "message": f"Generated {len(exercises)} synthesis exercises connecting course concepts"
    }


def _get_thematic_connections(self, connections: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Helper function to get thematic connections from synthesis service
    """
    # Find the most common themes/keywords across connections
    all_common_elements = []
    for conn in connections:
        all_common_elements.extend(conn.get('common_elements', []))

    if not all_common_elements:
        return {}

    from collections import Counter
    common_themes = Counter(all_common_elements)
    top_themes = {theme: count for theme, count in common_themes.most_common(5)}

    return {
        "top_themes": top_themes,
        "total_thematic_connections": len(top_themes),
        "most_common_theme": max(top_themes, key=top_themes.get) if top_themes else None
    }