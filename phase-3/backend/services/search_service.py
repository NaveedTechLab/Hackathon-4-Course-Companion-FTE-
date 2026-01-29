from sqlalchemy.orm import Session
from ..models.content import Content
from ..models.course import Course
from typing import List, Dict, Any
import uuid
import re
from datetime import datetime, timedelta
import time

class SearchService:
    """
    Service for searching course content using deterministic keyword-based search
    This service does not use any LLM functionality, relying solely on keyword matching and metadata analysis
    """

    def __init__(self):
        pass

    def search_content(
        self,
        db: Session,
        query: str,
        course_id: uuid.UUID = None,
        filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Perform keyword-based search across course content
        """
        start_time = time.time()

        # Prepare search query - extract keywords and normalize
        search_keywords = self._extract_search_keywords(query)

        # Build query
        search_query = db.query(Content)

        # Apply course filter if provided
        if course_id:
            search_query = search_query.filter(Content.course_id == course_id)

        # Apply additional filters if provided
        if filters:
            if 'content_type' in filters:
                from ..models.content import ContentType
                search_query = search_query.filter(Content.content_type == ContentType(filters['content_type']))
            if 'created_after' in filters:
                search_query = search_query.filter(Content.created_at >= filters['created_after'])
            if 'created_before' in filters:
                search_query = search_query.filter(Content.created_at <= filters['created_before'])

        # Execute search - match keywords in title and metadata
        all_content = search_query.all()

        # Filter results based on keyword matching
        results = []
        for content in all_content:
            relevance_score = self._calculate_keyword_relevance(content, search_keywords)

            if relevance_score > 0:  # Only include if there's some relevance
                results.append({
                    "id": content.id,
                    "title": content.title,
                    "content_type": content.content_type.value,
                    "course_id": content.course_id,
                    "relevance_score": relevance_score,
                    "snippet": self._get_content_snippet(content, query),
                    "created_at": content.created_at
                })

        # Sort by relevance score (descending)
        results.sort(key=lambda x: x["relevance_score"], reverse=True)

        # Calculate execution time
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        return {
            "results": results,
            "total_results": len(results),
            "query": query,
            "course_id": course_id,
            "took_ms": execution_time,
            "message": f"Found {len(results)} results in {execution_time:.2f}ms"
        }

    def _extract_search_keywords(self, query: str) -> List[str]:
        """
        Extract search keywords from query string
        """
        # Remove special characters and convert to lowercase
        clean_query = re.sub(r'[^\w\s]', ' ', query.lower())

        # Split into words
        words = clean_query.split()

        # Filter out common stop words (basic implementation)
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }

        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        return keywords

    def _calculate_keyword_relevance(self, content: Content, keywords: List[str]) -> float:
        """
        Calculate relevance score based on keyword matching
        """
        if not keywords:
            return 0.0

        # Score based on matches in title and metadata
        title_lower = content.title.lower()
        metadata_lower = (content.content_metadata or "").lower()

        title_matches = sum(1 for keyword in keywords if keyword in title_lower)
        metadata_matches = sum(1 for keyword in keywords if keyword in metadata_lower)

        # Weight title matches more heavily than metadata matches
        relevance_score = (title_matches * 2) + metadata_matches

        # Normalize based on content length and keyword count
        total_matches = title_matches + metadata_matches
        if total_matches == 0:
            return 0.0

        # Calculate normalized score (0-1 scale)
        max_possible_matches = len(keywords) * 3  # 2 for title, 1 for metadata
        normalized_score = min(1.0, relevance_score / max_possible_matches)

        return normalized_score

    def _get_content_snippet(self, content: Content, query: str, max_length: int = 150) -> str:
        """
        Get a snippet of content that highlights the query terms
        """
        # For now, we'll use the title and a portion of the metadata
        # In a real implementation, this might extract from the actual content
        full_text = f"{content.title} {(content.content_metadata or '')[:500]}"

        # Find positions of query terms in the text
        query_words = self._extract_search_keywords(query)
        positions = []

        for word in query_words:
            pos = full_text.lower().find(word.lower())
            if pos != -1:
                positions.append(pos)

        if positions:
            # Center the snippet around the first match
            start_pos = max(0, min(positions) - 50)
            end_pos = min(len(full_text), start_pos + max_length)
            snippet = full_text[start_pos:end_pos]

            if start_pos > 0:
                snippet = "..." + snippet
            if end_pos < len(full_text):
                snippet += "..."

            return snippet
        else:
            # Return beginning of content if no matches found
            return full_text[:max_length] + ("..." if len(full_text) > max_length else "")

    def get_search_suggestions(self, db: Session, query: str, course_id: uuid.UUID = None) -> List[str]:
        """
        Get search suggestions for autocomplete
        """
        # Find content titles that contain the query as a substring
        search_query = db.query(Content.title)

        if course_id:
            search_query = search_query.filter(Content.course_id == course_id)

        # Filter for titles containing the query
        suggestions = search_query.filter(
            Content.title.ilike(f"%{query}%")
        ).distinct().limit(10).all()

        # Extract just the title strings
        suggestion_list = [item[0] for item in suggestions if item[0]]

        # Remove duplicates while preserving order
        seen = set()
        unique_suggestions = []
        for suggestion in suggestion_list:
            if suggestion.lower() not in seen:
                seen.add(suggestion.lower())
                unique_suggestions.append(suggestion)

        return unique_suggestions

    def faceted_search(
        self,
        db: Session,
        query: str,
        facets: Dict[str, Any],
        course_id: uuid.UUID = None
    ) -> List[Dict[str, Any]]:
        """
        Perform faceted search with additional filters
        """
        # Build base query
        search_query = db.query(Content)

        if course_id:
            search_query = search_query.filter(Content.course_id == course_id)

        # Apply facet filters
        if 'content_type' in facets:
            from ..models.content import ContentType
            search_query = search_query.filter(Content.content_type == ContentType(facets['content_type']))

        if 'created_after' in facets:
            search_query = search_query.filter(Content.created_at >= facets['created_after'])

        if 'created_before' in facets:
            search_query = search_query.filter(Content.created_at <= facets['created_before'])

        # Get content that matches filters
        filtered_content = search_query.all()

        # Apply keyword search to filtered results
        search_keywords = self._extract_search_keywords(query)
        results = []

        for content in filtered_content:
            relevance_score = self._calculate_keyword_relevance(content, search_keywords)
            if relevance_score > 0:
                results.append({
                    "id": content.id,
                    "title": content.title,
                    "content_type": content.content_type.value,
                    "course_id": content.course_id,
                    "relevance_score": relevance_score,
                    "snippet": self._get_content_snippet(content, query),
                    "created_at": content.created_at
                })

        # Sort by relevance
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results

    def search_by_author(
        self,
        db: Session,
        author_name: str,
        course_id: uuid.UUID = None
    ) -> List[Dict[str, Any]]:
        """
        Search content by author name in metadata
        """
        search_query = db.query(Content)

        if course_id:
            search_query = search_query.filter(Content.course_id == course_id)

        # Look for author name in content metadata
        author_pattern = f"%{author_name}%"
        search_query = search_query.filter(Content.content_metadata.ilike(author_pattern))

        content_items = search_query.all()

        results = []
        for content in content_items:
            results.append({
                "id": content.id,
                "title": content.title,
                "content_type": content.content_type.value,
                "course_id": content.course_id,
                "author": author_name,  # Extracted from metadata
                "created_at": content.created_at
            })

        return results

    def get_popular_searches(self, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get popular search terms (simulated - in a real system this would use search logs)
        """
        # This is a simulated implementation
        # In a real system, this would analyze search logs to find popular terms
        popular_terms = [
            {"term": "introduction", "count": 150},
            {"term": "tutorial", "count": 120},
            {"term": "exercise", "count": 98},
            {"term": "quiz", "count": 87},
            {"term": "assignment", "count": 76},
            {"term": "practice", "count": 65},
            {"term": "example", "count": 60},
            {"term": "solution", "count": 55},
            {"term": "review", "count": 50},
            {"term": "concept", "count": 45}
        ]

        return popular_terms[:limit]

    def get_content_by_tags(
        self,
        db: Session,
        tags: List[str],
        course_id: uuid.UUID = None
    ) -> List[Dict[str, Any]]:
        """
        Search content by tags in metadata
        """
        search_query = db.query(Content)

        if course_id:
            search_query = search_query.filter(Content.course_id == course_id)

        # Look for content that has tags in its metadata
        for tag in tags:
            tag_pattern = f"%{tag}%"
            search_query = search_query.filter(Content.content_metadata.ilike(tag_pattern))

        content_items = search_query.all()

        results = []
        for content in content_items:
            # Extract matching tags from content
            content_tags = []
            metadata_lower = (content.content_metadata or "").lower()
            for tag in tags:
                if tag.lower() in metadata_lower:
                    content_tags.append(tag)

            results.append({
                "id": content.id,
                "title": content.title,
                "content_type": content.content_type.value,
                "course_id": content.course_id,
                "matching_tags": content_tags,
                "created_at": content.created_at
            })

        return results

    def search_by_content_type(
        self,
        db: Session,
        content_type: str,
        course_id: uuid.UUID = None
    ) -> List[Dict[str, Any]]:
        """
        Search content by type
        """
        from ..models.content import ContentType

        search_query = db.query(Content)

        if course_id:
            search_query = search_query.filter(Content.course_id == course_id)

        try:
            search_query = search_query.filter(Content.content_type == ContentType(content_type))
        except ValueError:
            # Invalid content type
            return []

        content_items = search_query.all()

        results = []
        for content in content_items:
            results.append({
                "id": content.id,
                "title": content.title,
                "content_type": content.content_type.value,
                "course_id": content.course_id,
                "file_size": content.file_size,
                "created_at": content.created_at
            })

        return results

    def get_related_content(
        self,
        db: Session,
        content_id: uuid.UUID,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get content related to a specific content item based on metadata similarity
        """
        # Get the original content
        original_content = db.query(Content).filter(Content.id == content_id).first()
        if not original_content:
            return []

        # Extract keywords from the original content
        original_keywords = self._extract_search_keywords(original_content.title + " " + (original_content.content_metadata or ""))

        # Find other content with similar keywords
        all_content = db.query(Content).filter(Content.id != content_id).all()

        related_content = []
        for content in all_content:
            content_keywords = self._extract_search_keywords(content.title + " " + (content.content_metadata or ""))
            similarity = len(set(original_keywords) & set(content_keywords))

            if similarity > 0:
                related_content.append({
                    "id": content.id,
                    "title": content.title,
                    "content_type": content.content_type.value,
                    "course_id": content.course_id,
                    "similarity_score": similarity,
                    "created_at": content.created_at
                })

        # Sort by similarity and return top results
        related_content.sort(key=lambda x: x["similarity_score"], reverse=True)
        return related_content[:limit]