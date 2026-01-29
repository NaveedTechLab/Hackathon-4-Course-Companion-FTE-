from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import uuid
from database import get_db
from middleware.premium_check import require_premium_access
from schemas.premium_schemas import (
    SynthesisRequest,
    SynthesisResponse,
    OverviewRequest,
    ExerciseRequest,
    ExerciseResponse
)
from services.synthesis_service import SynthesisService
from models.subscription import SubscriptionFeature

router = APIRouter()

@router.post("/synthesize", response_model=SynthesisResponse)
async def generate_cross_chapter_synthesis(
    request: SynthesisRequest,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(require_premium_access(SubscriptionFeature.CROSS_CHAPTER_SYNTHESIS))
) -> SynthesisResponse:
    """
    Generate synthesis connecting concepts across different chapters
    """
    try:
        synthesis_service = SynthesisService()

        result = synthesis_service.generate_cross_chapter_synthesis(
            db=db,
            user_id=user_id,
            course_id=request.course_id,
            chapters=request.chapters,
            focus_areas=request.focus_areas
        )

        return SynthesisResponse(
            synthesis_id=uuid.UUID(result["synthesis_id"]),
            user_id=user_id,
            course_id=request.course_id,
            chapters_synthesized=result["chapters_synthesized"],
            focus_areas=result["focus_areas"],
            synthesis_content=result["synthesis_content"],
            key_connections=result["key_connections"],
            generated_at=result["generated_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/overview", response_model=Dict[str, Any])
async def generate_course_overview(
    request: OverviewRequest,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(require_premium_access(SubscriptionFeature.CROSS_CHAPTER_SYNTHESIS))
) -> Dict[str, Any]:
    """
    Generate an overview summary connecting all concepts in a course
    """
    try:
        synthesis_service = SynthesisService()

        result = synthesis_service.generate_overview_summary(
            db=db,
            user_id=user_id,
            course_id=request.course_id,
            include_progress=request.include_progress
        )

        return {
            "overview_id": result["overview_id"],
            "user_id": result["user_id"],
            "course_id": result["course_id"],
            "include_progress": result["include_progress"],
            "overview_content": result["overview_content"],
            "key_themes": result["key_themes"],
            "learning_pathway": result["learning_pathway"],
            "generated_at": result["generated_at"],
            "token_usage": result["claude_metadata"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/exercise", response_model=ExerciseResponse)
async def generate_synthesis_exercise(
    request: ExerciseRequest,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(require_premium_access(SubscriptionFeature.CROSS_CHAPTER_SYNTHESIS))
) -> ExerciseResponse:
    """
    Generate a synthesis exercise that combines multiple concepts
    """
    try:
        synthesis_service = SynthesisService()

        result = synthesis_service.generate_synthesis_exercise(
            db=db,
            user_id=user_id,
            course_id=request.course_id,
            concept_pairs=request.concept_pairs,
            difficulty=request.difficulty
        )

        return ExerciseResponse(
            exercise_id=uuid.UUID(result["exercise_id"]),
            user_id=user_id,
            course_id=request.course_id,
            concept_pairs=request.concept_pairs,
            difficulty=request.difficulty,
            exercise_content=result["exercise_content"],
            sample_solution=result["sample_solution"],
            learning_objectives=result["learning_objectives"],
            created_at=result["created_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/recommendations/{course_id}", response_model=Dict[str, Any])
async def get_synthesis_recommendations(
    course_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(require_premium_access(SubscriptionFeature.CROSS_CHAPTER_SYNTHESIS))
) -> Dict[str, Any]:
    """
    Get recommendations for synthesis opportunities within a course
    """
    try:
        # This would analyze the course content to identify natural synthesis opportunities
        # For now, return placeholder data

        # Get course content to analyze for synthesis opportunities
        from models.content import Content
        contents = db.query(Content).filter(Content.course_id == course_id).all()

        # Identify potential concept pairs for synthesis
        concept_pairs = []
        for i in range(len(contents)):
            for j in range(i+1, min(i+3, len(contents))):  # Pair with next 2 contents
                concept_pairs.append((
                    contents[i].title.split()[0] if contents[i].title.split() else "Concept",
                    contents[j].title.split()[0] if contents[j].title.split() else "Concept"
                ))

        # Limit to 5 pairs to avoid overwhelming the user
        concept_pairs = concept_pairs[:5]

        return {
            "course_id": course_id,
            "total_contents": len(contents),
            "recommended_synthesis_pairs": concept_pairs,
            "total_recommendations": len(concept_pairs),
            "last_updated": str(uuid.datetime.datetime.utcnow())
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_ERROR,
            detail=f"Internal server error: {str(e)}"
        )