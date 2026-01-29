from fastapi import APIRouter
from api.endpoints import (
    adaptive_learning,
    assessment_grading,
    synthesis
)

# Main router for all premium features
premium_router = APIRouter(prefix="/api/v2/premium", tags=["Premium Features"])

# Include all premium feature routers
premium_router.include_router(adaptive_learning.router, prefix="/adaptive-learning", tags=["Adaptive Learning"])
premium_router.include_router(assessment_grading.router, prefix="/assessments", tags=["Assessment Grading"])
premium_router.include_router(synthesis.router, prefix="/synthesis", tags=["Cross-Chapter Synthesis"])

__all__ = ["premium_router"]