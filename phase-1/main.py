# Load environment variables first
from dotenv import load_dotenv
import os

# Load .env from parent directory if exists, otherwise current directory
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import content, navigation, search, quiz, progress, auth

app = FastAPI(
    title="Course Companion FTE - Phase 1",
    description="Digital educational tutor operating 168 hours/week with deterministic backend",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, configure this properly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(content.router, prefix="/api/v1", tags=["content"])
app.include_router(navigation.router, prefix="/api/v1", tags=["navigation"])
app.include_router(search.router, prefix="/api/v1", tags=["search"])
app.include_router(quiz.router, prefix="/api/v1", tags=["quiz"])
app.include_router(progress.router, prefix="/api/v1", tags=["progress"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Course Companion FTE - Phase 1 API", "phase": "1", "status": "operational"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "phase": "1", "service": "course-companion-api"}