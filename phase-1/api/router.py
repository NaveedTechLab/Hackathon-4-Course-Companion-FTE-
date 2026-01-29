from fastapi import APIRouter
from .endpoints import content, navigation, search, quiz, progress, auth

# Create the main API router
api_router = APIRouter()

# Include all API routes
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(navigation.router, prefix="/navigation", tags=["navigation"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

@api_router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "phase": "1", "service": "course-companion-api"}

@api_router.get("/ready")
def readiness_check():
    """Readiness check endpoint"""
    # In a real implementation, you would check database connectivity,
    # external service availability, etc.
    return {"status": "ready", "phase": "1", "service": "course-companion-api"}