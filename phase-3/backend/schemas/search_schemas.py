from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID

class SearchRequest(BaseModel):
    """
    Request model for content search
    """
    query: str
    course_id: Optional[str] = None  # Course ID as string to be converted to UUID
    filters: Optional[Dict[str, Any]] = None
    limit: Optional[int] = 20
    offset: Optional[int] = 0

class SearchResult(BaseModel):
    """
    Individual search result model
    """
    id: UUID
    title: str
    content_type: str
    course_id: UUID
    relevance_score: float
    snippet: str
    created_at: Any  # Using Any to accommodate datetime

class SearchResponse(BaseModel):
    """
    Response model for search results
    """
    query: str
    course_id: Optional[UUID] = None
    results: List[SearchResult]
    total_results: int
    took_ms: float
    message: str

class AutocompleteRequest(BaseModel):
    """
    Request model for search autocomplete
    """
    query: str
    course_id: Optional[str] = None
    limit: Optional[int] = 10

class AutocompleteResponse(BaseModel):
    """
    Response model for search autocomplete
    """
    query: str
    course_id: Optional[UUID] = None
    suggestions: List[str]
    total_suggestions: int

class FacetedSearchRequest(BaseModel):
    """
    Request model for faceted search
    """
    query: str
    facets: Dict[str, Any]
    course_id: Optional[str] = None
    limit: Optional[int] = 20

class FacetedSearchResponse(BaseModel):
    """
    Response model for faceted search
    """
    query: str
    facets: Dict[str, Any]
    course_id: Optional[UUID] = None
    results: List[SearchResult]
    total_results: int

class PopularSearchesResponse(BaseModel):
    """
    Response model for popular search terms
    """
    popular_searches: List[Dict[str, Any]]
    limit: int
    total_returned: int

class SearchByAuthorResponse(BaseModel):
    """
    Response model for author-based search
    """
    author: str
    course_id: Optional[UUID] = None
    results: List[Dict[str, Any]]
    total_results: int