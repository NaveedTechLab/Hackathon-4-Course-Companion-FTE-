from sqlalchemy.orm import Session
from ..models.progress import Progress, ProgressStatus, Streak
from ..models.content import Content
from ..models.course import Course
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timedelta
from collections import defaultdict

class ProgressService:
    """
    Service for tracking and managing user progress
    This is a deterministic service that tracks progress without LLM integration
    """

    def __init__(self):
        pass

    def update_content_progress(
        self,
        db: Session,
        user_id: uuid.UUID,
        content_id: uuid.UUID,
        status: str,
        completion_percentage: float = 0.0,
        time_spent_seconds: int = 0
    ) -> Progress:
        """
        Update progress for a specific content item
        """
        from ..models.progress import ProgressStatus

        try:
            status_enum = ProgressStatus(status)
        except ValueError:
            raise ValueError(f"Invalid progress status: {status}")

        # Check if progress record already exists
        existing_progress = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.content_id == content_id
        ).first()

        if existing_progress:
            # Update existing progress
            existing_progress.status = status_enum
            existing_progress.completion_percentage = completion_percentage
            existing_progress.time_spent_seconds = time_spent_seconds
            existing_progress.last_accessed = datetime.utcnow()
            existing_progress.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(existing_progress)
            return existing_progress
        else:
            # Create new progress record
            new_progress = Progress(
                user_id=user_id,
                content_id=content_id,
                status=status_enum,
                completion_percentage=completion_percentage,
                time_spent_seconds=time_spent_seconds,
                last_accessed=datetime.utcnow(),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            db.add(new_progress)
            db.commit()
            db.refresh(new_progress)
            return new_progress

    def get_user_progress(self, db: Session, user_id: uuid.UUID) -> Dict[str, Any]:
        """
        Get overall progress summary for a user
        """
        all_progress = db.query(Progress).filter(
            Progress.user_id == user_id
        ).all()

        if not all_progress:
            return {
                "total_content": 0,
                "completed_content": 0,
                "in_progress_content": 0,
                "not_started_content": 0,
                "overall_completion_percentage": 0.0,
                "current_streak_days": 0,
                "last_active": None,
                "progress_distribution": {
                    "completed": 0,
                    "in_progress": 0,
                    "not_started": 0
                }
            }

        # Count progress by status
        status_counts = defaultdict(int)
        for progress in all_progress:
            status_counts[progress.status.value] += 1

        total_content = len(all_progress)
        completed_content = status_counts[ProgressStatus.COMPLETED.value]
        in_progress_content = status_counts[ProgressStatus.IN_PROGRESS.value]
        not_started_content = status_counts[ProgressStatus.NOT_STARTED.value]

        overall_completion_percentage = (completed_content / total_content * 100) if total_content > 0 else 0

        # Calculate current streak
        current_streak = self._calculate_current_streak(db, user_id)

        # Get last active date
        last_active = max((p.updated_at for p in all_progress if p.updated_at), default=None)

        return {
            "total_content": total_content,
            "completed_content": completed_content,
            "in_progress_content": in_progress_content,
            "not_started_content": not_started_content,
            "overall_completion_percentage": round(overall_completion_percentage, 2),
            "current_streak_days": current_streak,
            "last_active": last_active,
            "progress_distribution": {
                "completed": completed_content,
                "in_progress": in_progress_content,
                "not_started": not_started_content
            }
        }

    def get_course_progress(self, db: Session, user_id: uuid.UUID, course_id: uuid.UUID) -> Dict[str, Any]:
        """
        Get progress for a specific course
        """
        # Get all content in the course
        course_content = db.query(Content).filter(
            Content.course_id == course_id
        ).all()

        # Get user's progress for content in this course
        user_progress = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.content_id.in_([c.id for c in course_content])
        ).all()

        # Create progress mapping
        progress_map = {p.content_id: p for p in user_progress}

        # Calculate progress for each content item
        content_progress = []
        completed_items = 0

        for content in course_content:
            progress = progress_map.get(content.id)
            if progress:
                content_progress.append({
                    "content_id": content.id,
                    "title": content.title,
                    "status": progress.status.value,
                    "completion_percentage": float(progress.completion_percentage) if progress.completion_percentage else 0,
                    "time_spent_seconds": progress.time_spent_seconds or 0,
                    "last_accessed": progress.last_accessed
                })

                if progress.status == ProgressStatus.COMPLETED:
                    completed_items += 1
            else:
                content_progress.append({
                    "content_id": content.id,
                    "title": content.title,
                    "status": ProgressStatus.NOT_STARTED.value,
                    "completion_percentage": 0,
                    "time_spent_seconds": 0,
                    "last_accessed": None
                })

        # Calculate completion percentage
        total_items = len(course_content)
        completion_percentage = (completed_items / total_items * 100) if total_items > 0 else 0

        # Calculate milestones
        milestones = self._calculate_course_milestones(completed_items, total_items)

        # Generate recommendations
        recommendations = self._generate_progress_recommendations(content_progress)

        return {
            "total_content_items": total_items,
            "completed_items": completed_items,
            "completion_percentage": round(completion_percentage, 2),
            "content_progress": content_progress,
            "milestones": milestones,
            "recommendations": recommendations
        }

    def _calculate_current_streak(self, db: Session, user_id: uuid.UUID) -> int:
        """
        Calculate current learning streak in days
        """
        # Get the user's streak record
        streak_record = db.query(Streak).filter(Streak.user_id == user_id).first()

        if streak_record:
            return streak_record.current_streak
        else:
            # If no streak record exists, create one with 0 streak
            new_streak = Streak(
                user_id=user_id,
                current_streak=0,
                longest_streak=0
            )
            db.add(new_streak)
            db.commit()
            return 0

    def _calculate_course_milestones(self, completed_items: int, total_items: int) -> List[Dict[str, Any]]:
        """
        Calculate course milestones based on completion
        """
        milestones = []

        # Define milestone thresholds
        thresholds = [
            {"threshold": 0.25, "name": "Quarter Way", "emoji": "🕐"},
            {"threshold": 0.50, "name": "Halfway", "emoji": "🕒"},
            {"threshold": 0.75, "name": "Almost Done", "emoji": "🕔"},
            {"threshold": 1.00, "name": "Course Complete", "emoji": "🎉"}
        ]

        for milestone in thresholds:
            threshold_items = int(milestone["threshold"] * total_items)
            if completed_items >= threshold_items and milestone["threshold"] <= completed_items / total_items if total_items > 0 else 0:
                milestones.append({
                    "name": milestone["name"],
                    "emoji": milestone["emoji"],
                    "threshold_percentage": milestone["threshold"] * 100,
                    "threshold_items": threshold_items,
                    "achieved": completed_items >= threshold_items,
                    "date_achieved": datetime.utcnow() if completed_items >= threshold_items else None
                })

        return milestones

    def _generate_progress_recommendations(self, content_progress: List[Dict[str, Any]]) -> List[str]:
        """
        Generate recommendations based on content progress
        """
        recommendations = []

        if not content_progress:
            return recommendations

        completed_count = len([item for item in content_progress if item["status"] == "completed"])
        total_count = len(content_progress)
        completion_percentage = completed_count / total_count if total_count > 0 else 0

        # Recommendation based on completion rate
        if completion_percentage < 0.3:
            recommendations.append("Focus on building a consistent study routine to establish momentum.")
        elif completion_percentage < 0.7:
            recommendations.append("You're making good progress! Try to maintain your current pace to finish strong.")
        elif completion_percentage < 1.0:
            recommendations.append("Almost there! Maintain your momentum to complete the course.")
        else:
            recommendations.append("Congratulations on completing the course! Consider exploring advanced materials.")

        # Identify difficult content
        incomplete_items = [item for item in content_progress if item["status"] != "completed"]
        if incomplete_items:
            longest_time_items = sorted(incomplete_items, key=lambda x: x["time_spent_seconds"], reverse=True)[:3]
            if longest_time_items:
                titles = [item["title"][:50] + "..." if len(item["title"]) > 50 else item["title"]
                         for item in longest_time_items]
                recommendations.append(f"You seem to be spending more time on: {', '.join(titles)}. "
                                      "Consider reviewing foundational concepts or seeking additional resources.")

        return recommendations

    def get_user_learning_analytics(self, db: Session, user_id: uuid.UUID, course_id: uuid.UUID = None) -> Dict[str, Any]:
        """
        Get detailed learning analytics for a user
        """
        # Get all progress records for the user
        query = db.query(Progress).filter(Progress.user_id == user_id)

        if course_id:
            # Filter by specific course
            content_ids = db.query(Content.id).filter(Content.course_id == course_id).subquery()
            query = query.filter(Progress.content_id.in_(content_ids))

        all_progress = query.all()

        if not all_progress:
            return {
                "user_id": user_id,
                "course_id": course_id,
                "total_content_accessed": 0,
                "total_time_spent_seconds": 0,
                "average_completion_time": 0,
                "learning_patterns": [],
                "performance_insights": []
            }

        # Calculate analytics
        total_time_spent = sum(p.time_spent_seconds or 0 for p in all_progress)
        completed_progress = [p for p in all_progress if p.status == ProgressStatus.COMPLETED]

        # Calculate average time per completed content
        avg_time_per_content = total_time_spent / len(completed_progress) if completed_progress else 0

        # Identify learning patterns
        learning_patterns = self._analyze_learning_patterns(all_progress)

        # Generate performance insights
        performance_insights = self._generate_performance_insights(all_progress)

        return {
            "user_id": user_id,
            "course_id": course_id,
            "total_content_accessed": len(all_progress),
            "total_time_spent_seconds": total_time_spent,
            "completed_content_count": len(completed_progress),
            "average_time_per_content": avg_time_per_content,
            "learning_patterns": learning_patterns,
            "performance_insights": performance_insights,
            "last_active": max((p.updated_at for p in all_progress if p.updated_at), default=None)
        }

    def _analyze_learning_patterns(self, progress_records: List[Progress]) -> List[Dict[str, Any]]:
        """
        Analyze learning patterns from progress data
        """
        patterns = []

        # Time-based patterns
        if progress_records:
            # Calculate time spent distribution
            time_spent_values = [p.time_spent_seconds or 0 for p in progress_records]
            avg_time = sum(time_spent_values) / len(time_spent_values)

            if avg_time < 300:  # Less than 5 minutes average
                patterns.append({
                    "pattern": "quick_review",
                    "description": "You tend to spend relatively little time on each content item",
                    "implication": "You may benefit from deeper engagement with materials"
                })
            elif avg_time > 1800:  # More than 30 minutes average
                patterns.append({
                    "pattern": "deep_focus",
                    "description": "You spend considerable time with each content item",
                    "implication": "You engage deeply with materials, which may lead to better retention"
                })
            else:
                patterns.append({
                    "pattern": "balanced_pacing",
                    "description": "You spend an appropriate amount of time with content items",
                    "implication": "Your pacing appears well-balanced for optimal learning"
                })

        return patterns

    def _generate_performance_insights(self, progress_records: List[Progress]) -> List[Dict[str, Any]]:
        """
        Generate performance insights from progress data
        """
        insights = []

        if not progress_records:
            return insights

        # Calculate completion rates by status
        status_counts = defaultdict(int)
        for p in progress_records:
            status_counts[p.status.value] += 1

        total_records = len(progress_records)
        completion_rate = status_counts[ProgressStatus.COMPLETED.value] / total_records * 100

        if completion_rate >= 80:
            insights.append({
                "type": "high_completion",
                "message": f"Excellent completion rate of {completion_rate:.1f}%",
                "suggestion": "Consider tackling more advanced content to continue growing"
            })
        elif completion_rate >= 60:
            insights.append({
                "type": "good_progress",
                "message": f"Good completion rate of {completion_rate:.1f}%",
                "suggestion": "Keep up the consistent progress"
            })
        else:
            insights.append({
                "type": "improvement_needed",
                "message": f"Completion rate of {completion_rate:.1f}% - room for improvement",
                "suggestion": "Consider setting aside dedicated study time each day"
            })

        # Identify content difficulty patterns
        if progress_records:
            avg_completion_percentage = sum(
                float(p.completion_percentage or 0) for p in progress_records
            ) / len(progress_records)

            if avg_completion_percentage < 50:
                insights.append({
                    "type": "content_difficulty",
                    "message": "Average completion percentage is low",
                    "suggestion": "Consider reviewing foundational concepts before proceeding"
                })

        return insights

    def update_streak(self, db: Session, user_id: uuid.UUID) -> Streak:
        """
        Update user's learning streak based on today's activity
        """
        from datetime import date

        # Get existing streak record
        streak = db.query(Streak).filter(Streak.user_id == user_id).first()

        today = date.today()

        if not streak:
            # Create new streak record
            streak = Streak(
                user_id=user_id,
                current_streak=1,
                longest_streak=1,
                last_learning_date=datetime.utcnow()
            )
            db.add(streak)
        else:
            # Update existing streak
            if streak.last_learning_date:
                last_date = streak.last_learning_date.date()

                if last_date == today:
                    # Same day, no change
                    pass
                elif (today - last_date).days == 1:
                    # Consecutive day, increment streak
                    streak.current_streak += 1
                    if streak.current_streak > streak.longest_streak:
                        streak.longest_streak = streak.current_streak
                else:
                    # Break in streak, reset to 1
                    streak.current_streak = 1

            streak.last_learning_date = datetime.utcnow()

        db.commit()
        db.refresh(streak)
        return streak