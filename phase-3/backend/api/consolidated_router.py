from fastapi import APIRouter
from . import (
    content_routes,
    navigation_routes,
    search_routes,
    quiz_routes,
    progress_routes,
    auth_routes
)

api_router = APIRouter()

# Include all Phase 1 and Phase 2 routes in a single consolidated router
api_router.include_router(content_routes.router, prefix="/content", tags=["content"])
api_router.include_router(navigation_routes.router, prefix="/navigation", tags=["navigation"])
api_router.include_router(search_routes.router, prefix="/search", tags=["search"])
api_router.include_router(quiz_routes.router, prefix="/quiz", tags=["quiz"])
api_router.include_router(progress_routes.router, prefix="/progress", tags=["progress"])
api_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])

@api_router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "phase": "3",
        "service": "consolidated-api",
        "features": {
            "deterministic": True,
            "premium_gated": True,
            "zero_backend_llm": True
        }
    }