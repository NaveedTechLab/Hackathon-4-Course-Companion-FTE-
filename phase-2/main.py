# Load environment variables first
from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.premium_router import premium_router
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Course Companion FTE - Phase 2 API",
    description="Premium AI-Enhanced Features for the Course Companion FTE",
    version="2.0.0",
    openapi_url="/api/v2/premium/openapi.json",
    docs_url="/api/v2/premium/docs",
    redoc_url="/api/v2/premium/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Uncomment the following line if you need to expose headers
    # expose_headers=["Access-Control-Allow-Origin"]
)

# Include premium feature routes
app.include_router(premium_router)

@app.get("/api/v2/premium/health")
async def health_check():
    """
    Health check endpoint for the premium API
    """
    return {
        "status": "healthy",
        "version": "2.0.0",
        "features": [
            "Adaptive Learning Paths",
            "LLM-Graded Assessments",
            "Cross-Chapter Synthesis"
        ],
        "openai_integration": True,
        "claude_integration": False
    }

@app.get("/api/v2/premium/info")
async def api_info():
    """
    Information about the premium API capabilities
    """
    return {
        "api": "Course Companion FTE - Phase 2",
        "version": "2.0.0",
        "description": "Premium AI-enhanced educational features",
        "features": {
            "adaptive_learning": {
                "description": "Personalized learning path recommendations",
                "endpoint": "/api/v2/premium/adaptive-learning",
                "authentication": "Premium subscription required"
            },
            "assessment_grading": {
                "description": "LLM-powered assessment grading for free-form responses",
                "endpoint": "/api/v2/premium/assessments",
                "authentication": "Premium subscription required"
            },
            "cross_chapter_synthesis": {
                "description": "Big-picture connections across different chapters and concepts",
                "endpoint": "/api/v2/premium/synthesis",
                "authentication": "Premium subscription required"
            }
        },
        "openai_sdk": True,
        "claude_sdk": False,
        "premium_only": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.API_PORT,
        reload=settings.DEBUG_MODE
    )