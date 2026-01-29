from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from typing import Dict, Any, List
from database import get_db
from services.search_service import SearchService
from middleware.auth import get_current_user

router = APIRouter()

@router.post("/search")
def search_content(
    query: str,
    course_id: uuid.UUID = None,
    filters: Dict[str, Any] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Search across course materials"""
    search_service = SearchService()

    # Perform search
    results = search_service.search_content(db, query, course_id, filters)

    return {
        "query": query,
        "course_id": course_id,
        "filters": filters,
        "results": [
            {
                "id": content.id,
                "title": content.title,
                "type": content.content_type.value,
                "course_id": content.course_id,
                "metadata": content.content_metadata
            }
            for content in results
        ],
        "total_results": len(results)
    }


@router.post("/search/autocomplete")
def search_autocomplete(
    query: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get search suggestions"""
    search_service = SearchService()
    suggestions = search_service.get_search_suggestions(db, query)

    return {
        "query": query,
        "suggestions": suggestions
    }


@router.post("/search/faceted")
def faceted_search(
    query: str,
    facets: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Perform faceted search with additional filters"""
    search_service = SearchService()
    results = search_service.faceted_search(db, query, facets)

    return {
        "query": query,
        "facets": facets,
        "results": [
            {
                "id": content.id,
                "title": content.title,
                "type": content.content_type.value,
                "course_id": content.course_id,
                "metadata": content.content_metadata
            }
            for content in results
        ],
        "total_results": len(results)
    }