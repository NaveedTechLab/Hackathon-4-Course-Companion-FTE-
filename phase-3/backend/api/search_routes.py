from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from uuid import UUID
import uuid
from ..database import get_db
from ..services.search_service import SearchService
from ..middleware.auth import get_current_user
from ..schemas.search_schemas import SearchRequest, SearchResponse

router = APIRouter()
search_service = SearchService()

@router.post("/search", response_model=SearchResponse)
def search_content(
    request: SearchRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Search across course materials using keyword-based search
    """
    try:
        course_uuid = uuid.UUID(request.course_id) if request.course_id else None
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )

    try:
        search_results = search_service.search_content(
            db,
            request.query,
            course_uuid,
            request.filters or {}
        )

        return SearchResponse(
            query=request.query,
            course_id=course_uuid,
            results=search_results["results"],
            total_results=search_results["total_results"],
            took_ms=search_results["took_ms"],
            message=search_results["message"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing search: {str(e)}"
        )


@router.post("/search/autocomplete")
def search_autocomplete(
    query: str,
    course_id: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get search suggestions for autocomplete
    """
    try:
        course_uuid = uuid.UUID(course_id) if course_id else None
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )

    try:
        suggestions = search_service.get_search_suggestions(db, query, course_uuid)
        return {
            "query": query,
            "course_id": course_uuid,
            "suggestions": suggestions,
            "total_suggestions": len(suggestions)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting search suggestions: {str(e)}"
        )


@router.post("/search/faceted")
def faceted_search(
    query: str,
    facets: Dict[str, Any],
    course_id: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Perform faceted search with additional filters
    """
    try:
        course_uuid = uuid.UUID(course_id) if course_id else None
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )

    try:
        results = search_service.faceted_search(db, query, facets, course_uuid)
        return {
            "query": query,
            "facets": facets,
            "course_id": course_uuid,
            "results": results,
            "total_results": len(results)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing faceted search: {str(e)}"
        )


@router.get("/search/popular-terms")
def get_popular_search_terms(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get popular search terms in the system
    """
    try:
        popular_terms = search_service.get_popular_searches(db, limit)
        return {
            "popular_searches": popular_terms,
            "limit": limit,
            "total_returned": len(popular_terms)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting popular searches: {str(e)}"
        )


@router.get("/search/authors/{author_name}")
def search_by_author(
    author_name: str,
    course_id: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Search content by author name
    """
    try:
        course_uuid = uuid.UUID(course_id) if course_id else None
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )

    try:
        results = search_service.search_by_author(db, author_name, course_uuid)
        return {
            "author": author_name,
            "course_id": course_uuid,
            "results": results,
            "total_results": len(results)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching by author: {str(e)}"
        )