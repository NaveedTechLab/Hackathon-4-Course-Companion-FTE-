from sqlalchemy.orm import Session
from models.content import Content
from models.course import Course
from typing import List, Dict, Any
import uuid
import re
from datetime import datetime

class SearchService:
    def __init__(self):
        pass

    def search_content(self, db: Session, query: str, course_id: uuid.UUID = None, filters: Dict[str, Any] = None) -> List[Content]:
        """Perform keyword-based search across course materials"""
        # Build the query
        search_query = db.query(Content)

        # Apply course filter if provided
        if course_id:
            search_query = search_query.filter(Content.course_id == course_id)

        # Apply additional filters if provided
        if filters:
            if 'content_type' in filters:
                from models.content import ContentType
                search_query = search_query.filter(Content.content_type == ContentType(filters['content_type']))
            if 'created_after' in filters:
                search_query = search_query.filter(Content.created_at >= filters['created_after'])
            if 'created_before' in filters:
                search_query = search_query.filter(Content.created_at <= filters['created_before'])

        # Perform full-text search on title and metadata
        search_terms = self._extract_search_terms(query)
        if search_terms:
            # Build OR condition for search terms
            search_conditions = []
            for term in search_terms:
                term_pattern = f"%{term}%"
                search_conditions.append(Content.title.ilike(term_pattern))
                if Content.content_metadata:
                    search_conditions.append(Content.content_metadata.ilike(term_pattern))

            if search_conditions:
                from sqlalchemy import or_
                search_query = search_query.filter(or_(*search_conditions))

        # Execute query and return results
        results = search_query.all()

        # Sort by relevance (simple implementation - prioritize title matches)
        sorted_results = sorted(results, key=lambda x: self._calculate_relevance(x, search_terms), reverse=True)

        return sorted_results

    def _extract_search_terms(self, query: str) -> List[str]:
        """Extract search terms from query string"""
        # Remove special characters and split into terms
        terms = re.findall(r'\b\w+\b', query.lower())
        # Filter out common stop words (basic implementation)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        return [term for term in terms if len(term) > 2 and term not in stop_words]

    def _calculate_relevance(self, content: Content, search_terms: List[str]) -> float:
        """Calculate relevance score for content based on search terms"""
        score = 0.0

        # Boost score for title matches
        title_lower = content.title.lower()
        for term in search_terms:
            if term in title_lower:
                # Give higher weight to title matches
                score += 2.0

        # Boost score for metadata matches
        if content.content_metadata:
            metadata_lower = content.content_metadata.lower()
            for term in search_terms:
                if term in metadata_lower:
                    score += 1.0

        return score

    def get_search_suggestions(self, db: Session, query: str) -> List[str]:
        """Get search suggestions based on partial query"""
        if len(query) < 2:
            return []

        # Find content with titles that start with or contain the query
        suggestions = db.query(Content.title).filter(
            Content.title.ilike(f"%{query}%")
        ).distinct().limit(10).all()

        return [s[0] for s in suggestions if s[0]]

    def faceted_search(self, db: Session, query: str, facets: Dict[str, Any]) -> List[Content]:
        """Perform faceted search with additional filters"""
        search_query = db.query(Content)

        # Apply facet filters
        if 'content_type' in facets:
            from models.content import ContentType
            search_query = search_query.filter(Content.content_type == ContentType(facets['content_type']))

        if 'course_id' in facets:
            search_query = search_query.filter(Content.course_id == uuid.UUID(facets['course_id']))

        if 'date_range' in facets:
            start_date = facets['date_range'].get('start')
            end_date = facets['date_range'].get('end')
            if start_date:
                search_query = search_query.filter(Content.created_at >= start_date)
            if end_date:
                search_query = search_query.filter(Content.created_at <= end_date)

        # Apply keyword search
        search_terms = self._extract_search_terms(query)
        if search_terms:
            search_conditions = []
            for term in search_terms:
                term_pattern = f"%{term}%"
                search_conditions.append(Content.title.ilike(term_pattern))
                if Content.content_metadata:
                    search_conditions.append(Content.content_metadata.ilike(term_pattern))

            if search_conditions:
                from sqlalchemy import or_
                search_query = search_query.filter(or_(*search_conditions))

        return search_query.all()

    def search_by_author(self, db: Session, author: str, course_id: uuid.UUID = None) -> List[Content]:
        """Search content by author"""
        search_query = db.query(Content)

        if course_id:
            search_query = search_query.filter(Content.course_id == course_id)

        # Look for author in metadata
        author_pattern = f"%{author}%"
        search_query = search_query.filter(Content.content_metadata.ilike(author_pattern))

        return search_query.all()

    def get_popular_searches(self, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Get popular search terms (would require search logs in a real implementation)"""
        # This is a simplified implementation
        # In a real system, this would analyze search logs to find popular terms
        return [
            {"term": "introduction", "count": 150},
            {"term": "tutorial", "count": 120},
            {"term": "exercise", "count": 98},
            {"term": "quiz", "count": 87},
            {"term": "assignment", "count": 76}
        ][:limit]