from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
from uuid import UUID
import logging
from models.content import Content
from models.progress import Progress, ProgressStatus
from models.course import Course
from services.learning_analytics import LearningAnalyticsService

logger = logging.getLogger(__name__)

class LearningPathService:
    """
    Service for generating and managing adaptive learning paths
    """

    def __init__(self):
        self.analytics_service = LearningAnalyticsService()

    def generate_adaptive_path(
        self,
        db: Session,
        user_id: UUID,
        course_id: UUID,
        current_progress: Dict[str, Any],
        learning_objectives: List[str],
        content_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate an adaptive learning path based on user data
        """
        try:
            # Analyze user's current performance and patterns
            user_insights = self.analytics_service.analyze_user_performance(db, user_id, course_id)

            # Get all content in the course
            course_content = db.query(Content).filter(
                Content.course_id == course_id
            ).order_by(Content.created_at).all()

            # Get user's progress for each content item
            user_progress = db.query(Progress).filter(
                Progress.user_id == user_id,
                Progress.content_id.in_([c.id for c in course_content])
            ).all()

            # Create progress mapping
            progress_map = {p.content_id: p for p in user_progress}

            # Identify knowledge gaps and strengths
            knowledge_gaps = user_insights.get("knowledge_gaps", [])
            strengths = user_insights.get("strengths", [])

            gap_content_ids = {gap["content_id"] for gap in knowledge_gaps}

            # Generate personalized path based on gaps and objectives
            recommended_path = self._generate_path_based_on_gaps(
                course_content,
                progress_map,
                gap_content_ids,
                learning_objectives,
                content_preferences
            )

            # Generate alternative paths
            alternative_paths = self._generate_alternative_paths(
                course_content,
                progress_map,
                user_insights,
                learning_objectives
            )

            # Identify focus areas
            focus_areas = self._identify_focus_areas(
                knowledge_gaps,
                learning_objectives
            )

            return {
                "user_id": user_id,
                "course_id": course_id,
                "recommended_path": recommended_path,
                "alternative_paths": alternative_paths,
                "focus_areas": focus_areas,
                "reasoning": self._generate_reasoning(
                    user_insights,
                    learning_objectives,
                    len(recommended_path)
                ),
                "estimated_completion_time": self._estimate_completion_time(recommended_path),
                "confidence_level": self._calculate_path_confidence(user_insights)
            }

        except Exception as e:
            logger.error(f"Error generating adaptive learning path: {e}")
            raise

    def _generate_path_based_on_gaps(
        self,
        course_content: List[Content],
        progress_map: Dict[UUID, Progress],
        gap_content_ids: set,
        learning_objectives: List[str],
        content_preferences: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate learning path prioritizing content that addresses knowledge gaps
        """
        path = []

        # Sort content based on priority: gaps first, then objectives, then chronological
        prioritized_content = []

        # Add gap content first
        for content in course_content:
            if content.id in gap_content_ids:
                prioritized_content.append(("high", content))

        # Add content related to learning objectives
        for content in course_content:
            if content.id not in gap_content_ids and self._matches_objectives(content, learning_objectives):
                prioritized_content.append(("medium", content))

        # Add remaining content
        for content in course_content:
            if content.id not in gap_content_ids and not self._matches_objectives(content, learning_objectives):
                prioritized_content.append(("low", content))

        # Create path with priority information
        for priority, content in prioritized_content:
            progress = progress_map.get(content.id)

            path_item = {
                "content_id": content.id,
                "title": content.title,
                "content_type": content.content_type.value if hasattr(content.content_type, 'value') else str(content.content_type),
                "priority": priority,
                "estimated_time_minutes": content.metadata.get("estimated_duration_minutes", 30) if content.metadata else 30,
                "difficulty": content.metadata.get("difficulty", "intermediate") if content.metadata else "intermediate",
                "is_completed": progress.status == ProgressStatus.COMPLETED if progress else False,
                "completion_percentage": progress.completion_percentage if progress else 0,
                "position": len(path) + 1
            }

            path.append(path_item)

        return path

    def _matches_objectives(self, content: Content, objectives: List[str]) -> bool:
        """
        Check if content matches any of the learning objectives
        """
        content_text = f"{content.title} {content.description}".lower()
        for objective in objectives:
            if objective.lower() in content_text:
                return True
        return False

    def _generate_alternative_paths(
        self,
        course_content: List[Content],
        progress_map: Dict[UUID, Progress],
        user_insights: Dict[str, Any],
        learning_objectives: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate alternative learning paths based on different approaches
        """
        alternative_paths = []

        # Alternative 1: Speed-focused path (easier content first to build confidence)
        speed_path = self._create_speed_focused_path(course_content, progress_map)
        if speed_path:
            alternative_paths.append({
                "path_id": "speed_focused",
                "path_name": "Speed-focused Path",
                "description": "Focus on completing easier content quickly to build momentum",
                "contents": speed_path
            })

        # Alternative 2: Mastery-focused path (difficult content first to tackle challenges early)
        mastery_path = self._create_mastery_focused_path(course_content, progress_map)
        if mastery_path:
            alternative_paths.append({
                "path_id": "mastery_focused",
                "path_name": "Mastery-focused Path",
                "description": "Tackle challenging content first to address difficulties early",
                "contents": mastery_path
            })

        # Alternative 3: Objective-aligned path (strictly follows learning objectives order)
        objective_path = self._create_objective_aligned_path(course_content, progress_map, learning_objectives)
        if objective_path:
            alternative_paths.append({
                "path_id": "objective_aligned",
                "path_name": "Objective-aligned Path",
                "description": "Sequenced strictly according to your learning objectives",
                "contents": objective_path
            })

        return alternative_paths

    def _create_speed_focused_path(
        self,
        course_content: List[Content],
        progress_map: Dict[UUID, Progress]
    ) -> List[Dict[str, Any]]:
        """
        Create a path focusing on easier content to build momentum
        """
        # Sort by difficulty ascending (assuming easier content first)
        sorted_content = sorted(course_content, key=lambda c: self._get_content_difficulty_score(c))

        path = []
        for content in sorted_content:
            progress = progress_map.get(content.id)
            if not progress or progress.status != ProgressStatus.COMPLETED:
                path.append({
                    "content_id": content.id,
                    "title": content.title,
                    "difficulty_score": self._get_content_difficulty_score(content),
                    "position": len(path) + 1
                })

        return path

    def _create_mastery_focused_path(
        self,
        course_content: List[Content],
        progress_map: Dict[UUID, Progress]
    ) -> List[Dict[str, Any]]:
        """
        Create a path focusing on difficult content first
        """
        # Sort by difficulty descending (more difficult content first)
        sorted_content = sorted(course_content, key=lambda c: self._get_content_difficulty_score(c), reverse=True)

        path = []
        for content in sorted_content:
            progress = progress_map.get(content.id)
            if not progress or progress.status != ProgressStatus.COMPLETED:
                path.append({
                    "content_id": content.id,
                    "title": content.title,
                    "difficulty_score": self._get_content_difficulty_score(content),
                    "position": len(path) + 1
                })

        return path

    def _create_objective_aligned_path(
        self,
        course_content: List[Content],
        progress_map: Dict[UUID, Progress],
        learning_objectives: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Create a path aligned with learning objectives
        """
        path = []
        for objective in learning_objectives:
            # Find content that best matches this objective
            matching_content = self._find_content_for_objective(course_content, objective)
            for content in matching_content:
                progress = progress_map.get(content.id)
                if not progress or progress.status != ProgressStatus.COMPLETED:
                    path.append({
                        "content_id": content.id,
                        "title": content.title,
                        "related_objective": objective,
                        "position": len(path) + 1
                    })

        return path

    def _find_content_for_objective(self, course_content: List[Content], objective: str) -> List[Content]:
        """
        Find content that relates to a specific learning objective
        """
        matching_content = []
        objective_lower = objective.lower()

        for content in course_content:
            content_text = f"{content.title} {content.description}".lower()
            if objective_lower in content_text:
                matching_content.append(content)

        return matching_content

    def _get_content_difficulty_score(self, content: Content) -> int:
        """
        Get a numeric difficulty score for content (higher = more difficult)
        """
        if content.metadata and "difficulty" in content.metadata:
            difficulty_map = {
                "beginner": 1,
                "elementary": 2,
                "intermediate": 3,
                "advanced": 4,
                "expert": 5
            }
            difficulty = content.metadata["difficulty"].lower()
            return difficulty_map.get(difficulty, 3)  # Default to intermediate

        return 3  # Default to intermediate

    def _identify_focus_areas(
        self,
        knowledge_gaps: List[Dict[str, Any]],
        learning_objectives: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Identify key focus areas based on knowledge gaps and objectives
        """
        focus_areas = []

        # Add knowledge gaps as focus areas
        for gap in knowledge_gaps:
            focus_areas.append({
                "area": gap.get("title", "Unknown Area"),
                "reason": "Identified as knowledge gap based on performance",
                "recommended_resources": [gap.get("content_id")]
            })

        # Add objective-based focus areas
        for objective in learning_objectives:
            if not any(gap.get("title", "").lower() in objective.lower() for gap in knowledge_gaps):
                focus_areas.append({
                    "area": objective,
                    "reason": "Part of learning objectives",
                    "recommended_resources": []
                })

        return focus_areas

    def _generate_reasoning(
        self,
        user_insights: Dict[str, Any],
        learning_objectives: List[str],
        path_length: int
    ) -> str:
        """
        Generate explanation for why this path was recommended
        """
        completion_rate = user_insights.get("completion_rate", 0)
        velocity = user_insights.get("learning_velocity", "unknown")

        reasoning_parts = [
            f"This path is tailored to your current {completion_rate}% completion rate and {velocity} learning pace.",
            f"It prioritizes addressing the knowledge gaps identified in your performance."
        ]

        if learning_objectives:
            reasoning_parts.append(f"The path aligns with your stated learning objectives: {', '.join(learning_objectives[:3])}.")

        if path_length > 0:
            reasoning_parts.append(f"The recommended path includes {path_length} content items sequenced for optimal learning.")

        return " ".join(reasoning_parts)

    def _estimate_completion_time(self, path: List[Dict[str, Any]]) -> int:
        """
        Estimate total time to complete the path in minutes
        """
        total_minutes = 0
        for item in path:
            estimated_time = item.get("estimated_time_minutes", 30)
            total_minutes += estimated_time

        return total_minutes

    def _calculate_path_confidence(self, user_insights: Dict[str, Any]) -> str:
        """
        Calculate confidence level in the path recommendation
        """
        data_points = 0

        if user_insights.get("total_content", 0) > 0:
            data_points += 1
        if user_insights.get("knowledge_gaps"):
            data_points += 1
        if user_insights.get("performance_trends"):
            data_points += 1

        if data_points >= 3:
            return "high"
        elif data_points >= 2:
            return "medium"
        else:
            return "low"

    def adjust_learning_path(
        self,
        db: Session,
        user_id: UUID,
        course_id: UUID,
        current_progress: Dict[str, Any],
        learning_objectives: List[str]
    ) -> Dict[str, Any]:
        """
        Adjust an existing learning path based on new information
        """
        # Get current path and update based on new progress
        return self.generate_adaptive_path(
            db, user_id, course_id, current_progress, learning_objectives
        )

    def get_user_recommendations(
        self,
        db: Session,
        user_id: UUID
    ) -> List[Dict[str, Any]]:
        """
        Get general learning recommendations for a user
        """
        try:
            # Get user's recent activity and performance
            recent_progress = self.analytics_service._get_recent_progress(db, user_id, days=30)

            # Find courses with incomplete content
            incomplete_content = []
            for progress in recent_progress:
                if progress.status != ProgressStatus.COMPLETED:
                    content = db.query(Content).filter(Content.id == progress.content_id).first()
                    if content:
                        incomplete_content.append({
                            "content_id": content.id,
                            "title": content.title,
                            "course_id": content.course_id,
                            "completion_percentage": progress.completion_percentage or 0
                        })

            # Get user's most active courses
            active_courses = self._get_active_courses(db, user_id)

            recommendations = []
            for course in active_courses:
                course_content = db.query(Content).filter(
                    Content.course_id == course.id
                ).all()

                incomplete_in_course = [
                    content for content in course_content
                    if content.id in [ic["content_id"] for ic in incomplete_content]
                ]

                if incomplete_in_course:
                    recommendations.append({
                        "type": "continue_learning",
                        "course_id": course.id,
                        "course_title": course.title,
                        "content_to_continue": incomplete_in_course[:3],
                        "reason": "You have started this course but not finished"
                    })

            # Add new course recommendations based on user's interests
            new_course_recs = self._get_new_course_recommendations(db, user_id)
            recommendations.extend(new_course_recs)

            return recommendations

        except Exception as e:
            logger.error(f"Error getting user recommendations: {e}")
            raise

    def _get_active_courses(self, db: Session, user_id: UUID) -> List[Course]:
        """
        Get courses where user has recent activity
        """
        from models.progress import Progress
        from models.content import Content

        # Get content IDs the user has interacted with recently
        recent_content_ids = db.query(Progress.content_id).filter(
            Progress.user_id == user_id
        ).distinct().limit(20).subquery()

        # Get the courses those contents belong to
        course_ids = db.query(Content.course_id).filter(
            Content.id.in_(recent_content_ids)
        ).distinct().all()

        # Get course objects
        course_uuids = [cid[0] for cid in course_ids]
        courses = db.query(Course).filter(Course.id.in_(course_uuids)).all()

        return courses

    def _get_new_course_recommendations(self, db: Session, user_id: UUID) -> List[Dict[str, Any]]:
        """
        Get recommendations for new courses based on user's activity
        """
        # This would implement a recommendation algorithm based on user's activity
        # For now, returning placeholder
        return []