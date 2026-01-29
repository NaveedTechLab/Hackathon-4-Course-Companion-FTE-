from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.consolidated_router import api_router
from .config import settings

app = FastAPI(
    title="Course Companion FTE - Phase 3 API",
    description="Consolidated API serving deterministic and hybrid features",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1", tags=["course-companion"])

@app.get("/")
def read_root():
    return {
        "message": "Course Companion FTE - Phase 3 API",
        "phase": "3",
        "status": "operational",
        "features": {
            "deterministic": True,
            "hybrid": True,
            "premium_gated": True
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "phase": "3",
        "service": "course-companion-api",
        "timestamp": "2026-01-27T00:00:00Z"
    }