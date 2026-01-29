from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
import uuid
import logging
from models.content import Content
from models.course import Course
from models.progress import Progress
from .openai_agent_service import OpenAIAgentService

logger = logging.getLogger(__name__)

class SynthesisService:
    """
    Service for generating cross-chapter synthesis and big-picture connections
    """

    def __init__(self):
        self.openai_service = OpenAIAgentService()

    def generate_cross_chapter_synthesis(
        self,
        db: Session,
        user_id: uuid.UUID,
        course_id: uuid.UUID,
        chapters: List[str],
        focus_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate synthesis connecting concepts across different chapters
        """
        try:
            # Get course information
            course = db.query(Course).filter(Course.id == course_id).first()
            if not course:
                raise ValueError("Course not found")

            # Get content from specified chapters
            contents = db.query(Content).filter(
                Content.course_id == course_id,
                Content.chapter_title.in_(chapters) if chapters else Content.course_id == course_id
            ).all()

            # Build context from course content
            content_context = []
            for content in contents:
                content_context.append({
                    "title": content.title,
                    "summary": content.summary,
                    "key_concepts": content.metadata.get("key_concepts", []) if content.metadata else [],
                    "chapter": content.chapter_title
                })

            # Create synthesis request to Claude
            synthesis_request = {
                "course_title": course.title,
                "course_description": course.description,
                "content_context": content_context,
                "chapters_referenced": chapters,
                "focus_areas": focus_areas or [],
                "request_type": "cross_chapter_synthesis"
            }

            system_prompt = """
            You are an expert educational synthesizer. Your role is to identify and articulate
            connections between concepts taught in different chapters, helping students see
            the bigger picture and understand how different topics interrelate.
            Focus on meaningful connections that enhance understanding.
            """

            user_content = f"""
            Course: {synthesis_request['course_title']}
            Course Description: {synthesis_request['course_description']}

            Content Context: {str(synthesis_request['content_context'][:5])}  # Limit to first 5 items

            Focus Areas: {', '.join(synthesis_request['focus_areas']) if synthesis_request['focus_areas'] else 'None specified'}

            Please generate a synthesis that connects concepts across these chapters, highlighting:
            1. Key interconnections between topics
            2. How concepts build upon each other
            3. Common themes or principles
            4. Practical applications that combine multiple concepts
            5. Recommendations for deeper understanding of the connections

            Format your response as a detailed explanation with specific examples.
            """

            messages = [{"role": "user", "content": user_content}]

            openai_response = self.openai_service.create_completion(
                messages=messages,
                system_prompt=system_prompt,
                max_tokens=2500,
                temperature=0.4,
                user_id=str(user_id),
                feature_type="cross_chapter_synthesis"
            )

            # Create synthesis result
            synthesis_result = {
                "synthesis_id": str(uuid.uuid4()),
                "user_id": str(user_id),
                "course_id": str(course_id),
                "chapters_synthesized": chapters,
                "focus_areas": focus_areas or [],
                "synthesis_content": openai_response.get("content", ""),
                "key_connections": self._extract_key_connections(openai_response.get("content", "")),
                "generated_at": str(uuid.datetime.datetime.utcnow()),
                "openai_metadata": {
                    "model_used": openai_response.get("model"),
                    "input_tokens": openai_response.get("usage", {}).get("input_tokens", 0),
                    "output_tokens": openai_response.get("usage", {}).get("output_tokens", 0),
                    "estimated_cost": openai_response.get("cost_estimate", 0.0)
                }
            }

            return synthesis_result

        except Exception as e:
            logger.error(f"Error generating cross-chapter synthesis: {e}")
            raise

    def generate_overview_summary(
        self,
        db: Session,
        user_id: uuid.UUID,
        course_id: uuid.UUID,
        include_progress: bool = False
    ) -> Dict[str, Any]:
        """
        Generate an overview summary connecting all concepts in a course
        """
        try:
            # Get course information
            course = db.query(Course).filter(Course.id == course_id).first()
            if not course:
                raise ValueError("Course not found")

            # Get all content in the course
            all_contents = db.query(Content).filter(
                Content.course_id == course_id
            ).order_by(Content.chapter_title, Content.created_at).all()

            # Optionally get user's progress
            user_progress = None
            if include_progress:
                user_progress = db.query(Progress).filter(
                    Progress.user_id == user_id,
                    Progress.content_id.in_([c.id for c in all_contents])
                ).all()

            # Build comprehensive context
            content_context = []
            for content in all_contents:
                context_item = {
                    "title": content.title,
                    "chapter": content.chapter_title,
                    "content_type": str(content.content_type),
                    "key_points": content.metadata.get("key_points", []) if content.metadata else [],
                    "prerequisites": content.metadata.get("prerequisites", []) if content.metadata else []
                }

                # Add progress information if requested
                if include_progress:
                    progress_for_content = next((p for p in user_progress if p.content_id == content.id), None)
                    if progress_for_content:
                        context_item["progress_status"] = progress_for_content.status.value
                        context_item["completion_percentage"] = progress_for_content.completion_percentage

                content_context.append(context_item)

            # Create overview summary request to Claude
            system_prompt = """
            You are an expert educational synthesizer. Create a comprehensive overview that
            connects all concepts in the course, showing how they fit together in a coherent
            learning journey. Highlight the progression of ideas and how each concept builds
            on previous ones.
            """

            user_content = f"""
            Course: {course.title}
            Course Description: {course.description}

            Content Structure: {str(content_context[:10])}  # Limit to first 10 items to manage context

            Please generate a comprehensive overview summary that:
            1. Shows how all concepts connect in a cohesive narrative
            2. Highlights the learning progression
            3. Identifies prerequisite relationships
            4. Points out synthesis opportunities
            5. Suggests how to approach the course for maximum understanding

            If progress information is provided, also include personalized recommendations.
            """

            messages = [{"role": "user", "content": user_content}]

            openai_response = self.openai_service.create_completion(
                messages=messages,
                system_prompt=system_prompt,
                max_tokens=3000,
                temperature=0.5,
                user_id=str(user_id),
                feature_type="overview_synthesis"
            )

            overview_result = {
                "overview_id": str(uuid.uuid4()),
                "user_id": str(user_id),
                "course_id": str(course_id),
                "include_progress": include_progress,
                "overview_content": openai_response.get("content", ""),
                "key_themes": self._extract_key_themes(openai_response.get("content", "")),
                "learning_pathway": self._extract_learning_pathway(openai_response.get("content", "")),
                "generated_at": str(uuid.datetime.datetime.utcnow()),
                "openai_metadata": {
                    "model_used": openai_response.get("model"),
                    "input_tokens": openai_response.get("usage", {}).get("input_tokens", 0),
                    "output_tokens": openai_response.get("usage", {}).get("output_tokens", 0),
                    "estimated_cost": openai_response.get("cost_estimate", 0.0)
                }
            }

            return overview_result

        except Exception as e:
            logger.error(f"Error generating overview summary: {e}")
            raise

    def generate_synthesis_exercise(
        self,
        db: Session,
        user_id: uuid.UUID,
        course_id: uuid.UUID,
        concept_pairs: List[tuple],
        difficulty: str = "intermediate"
    ) -> Dict[str, Any]:
        """
        Generate a synthesis exercise that combines multiple concepts
        """
        try:
            course = db.query(Course).filter(Course.id == course_id).first()
            if not course:
                raise ValueError("Course not found")

            # Get content for the specified concept pairs
            concept_details = []
            for concept_a, concept_b in concept_pairs:
                contents = db.query(Content).filter(
                    Content.course_id == course_id,
                    (Content.title.contains(concept_a)) | (Content.title.contains(concept_b))
                ).limit(2).all()

                for content in contents:
                    concept_details.append({
                        "title": content.title,
                        "summary": content.summary,
                        "key_concepts": content.metadata.get("key_concepts", []) if content.metadata else [],
                        "relationships": [concept_a, concept_b]
                    })

            # Create synthesis exercise request to Claude
            system_prompt = """
            You are an expert educational designer. Create a synthesis exercise that
            requires students to connect and apply multiple concepts. The exercise should
            challenge students to think critically about how concepts relate to each other
            and can be combined in practical applications.
            """

            user_content = f"""
            Course: {course.title}

            Concept Pairs to Synthesize: {str(concept_pairs)}

            Concept Details: {str(concept_details[:5])}  # Limit to first 5 items

            Difficulty Level: {difficulty}

            Please create a synthesis exercise that:
            1. Requires application of both concepts
            2. Shows their interconnection
            3. Challenges higher-order thinking
            4. Includes clear instructions
            5. Provides a framework for response

            Also provide a sample solution that demonstrates the synthesis.
            """

            messages = [{"role": "user", "content": user_content}]

            openai_response = self.openai_service.create_completion(
                messages=messages,
                system_prompt=system_prompt,
                max_tokens=2000,
                temperature=0.6,
                user_id=str(user_id),
                feature_type="synthesis_exercise"
            )

            exercise_result = {
                "exercise_id": str(uuid.uuid4()),
                "user_id": str(user_id),
                "course_id": str(course_id),
                "concept_pairs": concept_pairs,
                "difficulty": difficulty,
                "exercise_content": openai_response.get("content", ""),
                "sample_solution": self._extract_sample_solution(openai_response.get("content", "")),
                "learning_objectives": self._extract_learning_objectives(openai_response.get("content", "")),
                "created_at": str(uuid.datetime.datetime.utcnow()),
                "openai_metadata": {
                    "model_used": openai_response.get("model"),
                    "input_tokens": openai_response.get("usage", {}).get("input_tokens", 0),
                    "output_tokens": openai_response.get("usage", {}).get("output_tokens", 0),
                    "estimated_cost": openai_response.get("cost_estimate", 0.0)
                }
            }

            return exercise_result

        except Exception as e:
            logger.error(f"Error generating synthesis exercise: {e}")
            raise

    def _extract_key_connections(self, synthesis_content: str) -> List[str]:
        """
        Extract key connections from synthesis content (placeholder implementation)
        """
        # In a real implementation, this would use NLP techniques to extract connections
        # For now, return placeholder data
        return [
            "Connection between fundamental concepts",
            "Progression of ideas across chapters",
            "Integration of different methodologies"
        ]

    def _extract_key_themes(self, overview_content: str) -> List[str]:
        """
        Extract key themes from overview content (placeholder implementation)
        """
        return [
            "Fundamental principles",
            "Progressive complexity",
            "Practical applications",
            "Interdisciplinary connections"
        ]

    def _extract_learning_pathway(self, overview_content: str) -> List[str]:
        """
        Extract suggested learning pathway from overview content (placeholder implementation)
        """
        return [
            "Start with foundational concepts",
            "Progress to advanced applications",
            "Synthesize across domains",
            "Apply in practical contexts"
        ]

    def _extract_sample_solution(self, exercise_content: str) -> str:
        """
        Extract sample solution from exercise content (placeholder implementation)
        """
        return "Sample solution demonstrating concept synthesis would be provided here."

    def _extract_learning_objectives(self, exercise_content: str) -> List[str]:
        """
        Extract learning objectives from exercise content (placeholder implementation)
        """
        return [
            "Connect multiple concepts",
            "Apply knowledge in novel contexts",
            "Demonstrate critical thinking",
            "Synthesize interdisciplinary knowledge"
        ]