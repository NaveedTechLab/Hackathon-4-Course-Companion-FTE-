from sqlalchemy.orm import Session
from models.content import Content
from models.course import Course
from typing import List, Dict, Any, Optional
import uuid
import re
from datetime import datetime

class SynthesisService:
    """
    Service for generating cross-chapter connections and big-picture insights
    This is a deterministic service that identifies connections based on content metadata and relationships
    """

    def __init__(self):
        pass

    def generate_cross_chapter_synthesis(
        self,
        db: Session,
        user_id: uuid.UUID,
        course_id: uuid.UUID,
        chapters: List[Dict[str, Any]],
        connection_depth: str = "surface",
        output_format: str = "text"
    ) -> Dict[str, Any]:
        """
        Generate synthesis connecting concepts across different chapters
        """
        # Get course information
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise ValueError("Course not found")

        # Get all content for the course to analyze relationships
        course_content = db.query(Content).filter(
            Content.course_id == course_id
        ).order_by(Content.created_at).all()

        # Identify connections between chapters based on content
        connections = self._identify_connections(course_content, chapters, connection_depth)

        # Generate big picture insights
        big_picture_insights = self._generate_big_picture_insights(course_content, connections)

        # Create synthesis exercises
        synthesis_exercises = self._generate_synthesis_exercises(connections, course_content)

        return {
            "user_id": user_id,
            "course_id": course_id,
            "course_title": course.title,
            "synthesis_report": {
                "connection_count": len(connections),
                "connection_depth": connection_depth,
                "synthesis_quality": self._evaluate_synthesis_quality(connections)
            },
            "connections": connections,
            "big_picture_insights": big_picture_insights,
            "synthesis_exercises": synthesis_exercises,
            "processing_time_ms": 0,  # In a real implementation, measure actual processing time
            "method": "deterministic_pattern_matching"
        }

    def _identify_connections(
        self,
        course_content: List[Content],
        chapters: List[Dict[str, Any]],
        depth: str
    ) -> List[Dict[str, Any]]:
        """
        Identify connections between different chapters/sections using deterministic pattern matching
        """
        connections = []
        content_map = {str(content.id): content for content in course_content}

        # Create combinations of content items to analyze for connections
        for i, content1 in enumerate(course_content):
            for j, content2 in enumerate(course_content[i+1:], i+1):
                # Look for potential connections based on metadata and content
                connection = self._analyze_connection(content1, content2, depth)

                if connection:
                    connections.append(connection)

        return connections

    def _analyze_connection(
        self,
        content1: Content,
        content2: Content,
        depth: str
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze potential connection between two content items
        """
        # Check for common terms, concepts, or themes
        common_elements = self._find_common_elements(content1, content2)

        if not common_elements:
            return None

        # Determine connection type based on common elements
        connection_type = self._classify_connection_type(common_elements)

        # Generate connection description
        description = self._generate_connection_description(content1, content2, common_elements, connection_type)

        return {
            "from_content_id": content1.id,
            "to_content_id": content2.id,
            "from_title": content1.title,
            "to_title": content2.title,
            "connection_type": connection_type,
            "description": description,
            "common_elements": common_elements,
            "relevance_score": len(common_elements) / max(len(content1.title.split()), len(content2.title.split()), 1),
            "depth_level": depth
        }

    def _find_common_elements(self, content1: Content, content2: Content) -> List[str]:
        """
        Find common terms, concepts, or themes between two content items
        """
        # Extract keywords from titles and metadata
        title1_keywords = set(content1.title.lower().split())
        title2_keywords = set(content2.title.lower().split())

        # Find intersection of keywords
        common_keywords = title1_keywords.intersection(title2_keywords)

        # If no direct keyword matches, look for related concepts in metadata
        common_elements = list(common_keywords)

        # Add more sophisticated analysis based on content metadata
        if content1.content_metadata and content2.content_metadata:
            meta1 = content1.content_metadata.lower()
            meta2 = content2.content_metadata.lower()

            # Look for common terms in metadata
            for word in meta1.split():
                if len(word) > 3 and word in meta2 and word not in common_elements:
                    common_elements.append(word)

        return common_elements

    def _classify_connection_type(self, common_elements: List[str]) -> str:
        """
        Classify the type of connection based on common elements
        """
        # Define connection type indicators
        prerequisite_indicators = {
            'depends', 'require', 'prerequisite', 'foundation', 'based on', 'building on',
            'introduces', 'establishes', 'requires', 'needs', 'precedes'
        }

        complementary_indicators = {
            'complements', 'supports', 'enhances', 'adds', 'extends', 'applies',
            'uses', 'implements', 'demonstrates', 'illustrates', 'shows'
        }

        analogous_indicators = {
            'similar', 'like', 'resembles', 'compared to', 'analogy', 'parallel',
            'equivalent', 'corresponds to', 'matches', 'resembles'
        }

        # Check for connection type indicators in common elements
        common_set = {elem.lower() for elem in common_elements}

        if common_set.intersection(prerequisite_indicators):
            return "prerequisite"
        elif common_set.intersection(complementary_indicators):
            return "complementary"
        elif common_set.intersection(analogous_indicators):
            return "analogous"
        else:
            return "related"

    def _generate_connection_description(
        self,
        content1: Content,
        content2: Content,
        common_elements: List[str],
        connection_type: str
    ) -> str:
        """
        Generate a description of the connection between two content items
        """
        if connection_type == "prerequisite":
            return (f"The concepts in '{content1.title}' provide foundational knowledge "
                   f"that is required to understand the material in '{content2.title}'. "
                   f"Key shared concepts include: {', '.join(common_elements[:3])}.")
        elif connection_type == "complementary":
            return (f"The material in '{content2.title}' complements and builds upon "
                   f"the concepts introduced in '{content1.title}'. Together, these sections "
                   f"provide a more complete understanding of the topic. Key connections: {', '.join(common_elements[:3])}.")
        elif connection_type == "analogous":
            return (f"'{content1.title}' and '{content2.title}' contain analogous concepts "
                   f"that demonstrate similar principles in different contexts. "
                   f"Understanding the pattern in one can help with understanding the other. "
                   f"Similar elements: {', '.join(common_elements[:3])}.")
        else:
            return (f"'{content1.title}' and '{content2.title}' are related through "
                   f"shared concepts including: {', '.join(common_elements[:3])}. "
                   f"These connections help form a more cohesive understanding of the course material.")

    def _generate_big_picture_insights(self, course_content: List[Content], connections: List[Dict[str, Any]]) -> List[str]:
        """
        Generate big picture insights about the course structure and concepts
        """
        insights = []

        if not course_content:
            return insights

        # Insight about course structure
        insights.append(
            f"This course contains {len(course_content)} content items that form a connected learning pathway. "
            f"The material is designed to build progressively from foundational concepts to more advanced applications."
        )

        # Insight about connections
        if connections:
            connection_count = len(connections)
            avg_relevance = sum(conn.get('relevance_score', 0) for conn in connections) / len(connections) if connections else 0

            insights.append(
                f"Across the course materials, {connection_count} meaningful connections have been identified, "
                f"with an average relevance score of {avg_relevance:.2f}. This indicates a well-integrated curriculum "
                f"where concepts reinforce and build upon each other."
            )

        # Insight about concept progression
        if len(course_content) > 1:
            first_content = course_content[0]
            last_content = course_content[-1]

            insights.append(
                f"The course begins with foundational material in '{first_content.title}' and progresses to "
                f"more advanced applications in '{last_content.title}', creating a structured learning journey."
            )

        # Insight about thematic connections
        if connections:
            # Find the most common themes/keywords across connections
            all_common_elements = []
            for conn in connections:
                all_common_elements.extend(conn.get('common_elements', []))

            if all_common_elements:
                from collections import Counter
                common_themes = Counter(all_common_elements)
                top_themes = [theme for theme, count in common_themes.most_common(3)]

                if top_themes:
                    insights.append(
                        f"Key recurring themes throughout the course include: {', '.join(top_themes)}. "
                        f"These themes connect different sections and form the conceptual backbone of the material."
                    )

        return insights

    def _generate_synthesis_exercises(
        self,
        connections: List[Dict[str, Any]],
        course_content: List[Content]
    ) -> List[Dict[str, Any]]:
        """
        Generate exercises that require synthesizing concepts across different chapters
        """
        exercises = []

        if not connections:
            return exercises

        # Create exercises based on identified connections
        for i, connection in enumerate(connections[:5]):  # Limit to first 5 connections for brevity
            exercise = {
                "exercise_id": f"synthesis_ex_{i+1}",
                "title": f"Connecting {connection['from_title']} and {connection['to_title']}",
                "description": (
                    f"This exercise asks you to synthesize concepts from two different sections: "
                    f"'{connection['from_title']}' and '{connection['to_title']}'. "
                    f"The connection type is '{connection['connection_type']}', indicating that these concepts "
                    f"are {connection['connection_type']} to each other."
                ),
                "instructions": (
                    f"Review both sections and explain how the concepts from '{connection['from_title']}' "
                    f"relate to or can be applied in the context of '{connection['to_title']}'. "
                    f"Provide specific examples from both sections to support your explanation."
                ),
                "difficulty": "intermediate",
                "estimated_time_minutes": 20,
                "connection_type": connection["connection_type"],
                "related_content": [connection["from_content_id"], connection["to_content_id"]]
            }
            exercises.append(exercise)

        return exercises

    def _evaluate_synthesis_quality(self, connections: List[Dict[str, Any]]) -> str:
        """
        Evaluate the quality of the generated synthesis
        """
        if not connections:
            return "low"

        avg_relevance = sum(conn.get('relevance_score', 0) for conn in connections) / len(connections)

        if avg_relevance >= 0.7:
            return "high"
        elif avg_relevance >= 0.4:
            return "medium"
        else:
            return "low"

    def get_course_structure_synthesis(
        self,
        db: Session,
        course_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Generate synthesis of the entire course structure
        """
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise ValueError("Course not found")

        course_content = db.query(Content).filter(
            Content.course_id == course_id
        ).order_by(Content.created_at).all()

        # Analyze the sequence and relationships
        structure_analysis = {
            "course_id": course_id,
            "course_title": course.title,
            "total_content_items": len(course_content),
            "content_sequence": [
                {
                    "id": content.id,
                    "title": content.title,
                    "type": content.content_type.value if hasattr(content, 'content_type') else 'unknown',
                    "position": idx + 1
                }
                for idx, content in enumerate(course_content)
            ]
        }

        # Identify structural patterns
        patterns = self._identify_structural_patterns(course_content)
        structure_analysis["structural_patterns"] = patterns

        return structure_analysis

    def _identify_structural_patterns(self, course_content: List[Content]) -> List[Dict[str, Any]]:
        """
        Identify structural patterns in the course content sequence
        """
        patterns = []

        if len(course_content) < 2:
            return patterns

        # Pattern: Foundational content at beginning
        if len(course_content) > 0:
            first_content = course_content[0]
            patterns.append({
                "type": "foundational_start",
                "description": f"Course begins with '{first_content.title}' which likely introduces foundational concepts",
                "confidence": "high"
            })

        # Pattern: Progression from simple to complex
        if len(course_content) > 1:
            last_content = course_content[-1]
            patterns.append({
                "type": "advanced_application",
                "description": f"Course concludes with '{last_content.title}' which likely contains advanced applications or synthesis",
                "confidence": "high"
            })

        # Pattern: Content variety
        content_types = [getattr(content, 'content_type', 'unknown') for content in course_content]
        type_diversity = len(set(str(ct) for ct in content_types))

        if type_diversity > 1:
            patterns.append({
                "type": "multimodal_approach",
                "description": f"Course uses {type_diversity} different content types to reinforce learning through varied modalities",
                "confidence": "high"
            })

        return patterns