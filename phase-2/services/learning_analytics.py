from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
from uuid import UUID
from datetime import datetime, timedelta
from models.progress import Progress, ProgressStatus
from models.content import Content
from models.user import User
from models.course import Course
import logging

logger = logging.getLogger(__name__)

class LearningAnalyticsService:
    """
    Service for analyzing learning patterns and performance to generate insights
    """

    def __init__(self):
        pass

    def analyze_user_performance(self, db: Session, user_id: UUID, course_id: UUID = None) -> Dict[str, Any]:
        """
        Analyze user's performance data to identify patterns and insights
        """
        try:
            # Get all progress records for the user
            query = db.query(Progress).filter(Progress.user_id == user_id)

            if course_id:
                query = query.join(Content).filter(Content.course_id == course_id)

            progress_records = query.all()

            if not progress_records:
                return {
                    "user_id": user_id,
                    "course_id": course_id,
                    "total_content": 0,
                    "completed_content": 0,
                    "completion_rate": 0.0,
                    "avg_completion_time": None,
                    "performance_trends": [],
                    "knowledge_gaps": [],
                    "strengths": [],
                    "learning_velocity": "unknown"
                }

            total_content = len(progress_records)
            completed_content = len([p for p in progress_records if p.status == ProgressStatus.COMPLETED])
            completion_rate = (completed_content / total_content) * 100 if total_content > 0 else 0

            # Calculate average completion time
            completion_times = []
            for record in progress_records:
                if record.status == ProgressStatus.COMPLETED and record.time_spent_seconds:
                    completion_times.append(record.time_spent_seconds)

            avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else None

            # Identify performance trends
            recent_progress = self._get_recent_progress(db, user_id, days=30, course_id=course_id)
            performance_trends = self._analyze_trends(recent_progress)

            # Identify knowledge gaps based on low completion percentages
            knowledge_gaps = self._identify_knowledge_gaps(progress_records)

            # Identify strengths based on high performance
            strengths = self._identify_strengths(progress_records)

            # Calculate learning velocity
            learning_velocity = self._calculate_learning_velocity(progress_records)

            return {
                "user_id": user_id,
                "course_id": course_id,
                "total_content": total_content,
                "completed_content": completed_content,
                "completion_rate": round(completion_rate, 2),
                "avg_completion_time": avg_completion_time,
                "performance_trends": performance_trends,
                "knowledge_gaps": knowledge_gaps,
                "strengths": strengths,
                "learning_velocity": learning_velocity,
                "last_active": max((p.last_accessed for p in progress_records if p.last_accessed), default=None)
            }

        except Exception as e:
            logger.error(f"Error analyzing user performance: {e}")
            raise

    def _get_recent_progress(self, db: Session, user_id: UUID, days: int = 30, course_id: UUID = None) -> List[Progress]:
        """
        Get user's progress from the last N days
        """
        from sqlalchemy import and_, or_
        from datetime import datetime

        cutoff_date = datetime.utcnow() - timedelta(days=days)

        query = db.query(Progress).filter(
            and_(
                Progress.user_id == user_id,
                Progress.created_at >= cutoff_date
            )
        )

        if course_id:
            query = query.join(Content).filter(Content.course_id == course_id)

        return query.all()

    def _analyze_trends(self, progress_records: List[Progress]) -> List[Dict[str, Any]]:
        """
        Analyze trends in user's learning progress
        """
        if not progress_records:
            return []

        # Calculate weekly progress
        weekly_completion = {}
        for record in progress_records:
            week = record.created_at.strftime("%Y-W%U")
            if week not in weekly_completion:
                weekly_completion[week] = {"completed": 0, "in_progress": 0}

            if record.status == ProgressStatus.COMPLETED:
                weekly_completion[week]["completed"] += 1
            elif record.status == ProgressStatus.IN_PROGRESS:
                weekly_completion[week]["in_progress"] += 1

        trends = []
        weeks = sorted(weekly_completion.keys())

        for i in range(1, len(weeks)):
            prev_week = weekly_completion[weeks[i-1]]
            curr_week = weekly_completion[weeks[i]]

            prev_total = prev_week["completed"] + prev_week["in_progress"]
            curr_total = curr_week["completed"] + curr_week["in_progress"]

            if prev_total > 0 and curr_total > 0:
                change = ((curr_total - prev_total) / prev_total) * 100
                trends.append({
                    "period": f"{weeks[i-1]} to {weeks[i]}",
                    "change_percent": round(change, 2),
                    "direction": "increasing" if change > 0 else "decreasing"
                })

        return trends

    def _identify_knowledge_gaps(self, progress_records: List[Progress]) -> List[Dict[str, Any]]:
        """
        Identify potential knowledge gaps based on low completion rates
        """
        gaps = []

        # Group progress by content type or topic if available in metadata
        content_groups = {}
        for record in progress_records:
            # This would need to be adapted based on how content is categorized
            # For now, we'll use basic heuristics
            if record.completion_percentage and record.completion_percentage < 50:
                content = record.content  # Assuming relationship exists
                if content:
                    gaps.append({
                        "content_id": content.id,
                        "title": content.title,
                        "completion_percentage": record.completion_percentage,
                        "time_spent": record.time_spent_seconds
                    })

        # Sort by completion percentage (lowest first)
        gaps.sort(key=lambda x: x["completion_percentage"])
        return gaps[:5]  # Return top 5 knowledge gaps

    def _identify_strengths(self, progress_records: List[Progress]) -> List[Dict[str, Any]]:
        """
        Identify user's strengths based on high performance
        """
        strengths = []

        high_performers = [
            record for record in progress_records
            if record.completion_percentage and record.completion_percentage >= 80
        ]

        # Group by content characteristics to find strong areas
        for record in high_performers[:5]:  # Top 5 high performers
            content = record.content
            if content:
                strengths.append({
                    "content_id": content.id,
                    "title": content.title,
                    "completion_percentage": record.completion_percentage,
                    "time_spent": record.time_spent_seconds
                })

        return strengths

    def _calculate_learning_velocity(self, progress_records: List[Progress]) -> str:
        """
        Calculate user's learning velocity (speed of progress)
        """
        if not progress_records:
            return "unknown"

        # Calculate average days between content completions
        completed_records = [r for r in progress_records if r.status == ProgressStatus.COMPLETED]
        if len(completed_records) < 2:
            return "insufficient_data"

        # Sort by completion date
        completed_records.sort(key=lambda x: x.updated_at or x.created_at)

        # Calculate time between completions
        total_days = 0
        intervals = 0

        for i in range(1, len(completed_records)):
            time_diff = (completed_records[i].updated_at or completed_records[i].created_at) - \
                       (completed_records[i-1].updated_at or completed_records[i-1].created_at)
            days_diff = time_diff.days
            if days_diff > 0:  # Only count if there was a gap
                total_days += days_diff
                intervals += 1

        if intervals > 0:
            avg_days_between = total_days / intervals
            if avg_days_between <= 1:
                return "fast"
            elif avg_days_between <= 3:
                return "moderate"
            else:
                return "slow"
        else:
            return "unknown"

    def get_content_engagement_metrics(self, db: Session, content_id: UUID) -> Dict[str, Any]:
        """
        Get engagement metrics for a specific content item
        """
        try:
            progress_records = db.query(Progress).filter(
                Progress.content_id == content_id
            ).all()

            if not progress_records:
                return {
                    "content_id": content_id,
                    "total_attempts": 0,
                    "completion_rate": 0.0,
                    "avg_completion_time": None,
                    "engagement_score": 0.0
                }

            total_attempts = len(progress_records)
            completed_attempts = len([p for p in progress_records if p.status == ProgressStatus.COMPLETED])
            completion_rate = (completed_attempts / total_attempts) * 100 if total_attempts > 0 else 0

            # Calculate average completion time
            completion_times = [p.time_spent_seconds for p in progress_records
                              if p.status == ProgressStatus.COMPLETED and p.time_spent_seconds]
            avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else None

            # Engagement score based on completion rate and time spent
            engagement_score = completion_rate * 0.7  # Weight completion rate heavily
            if avg_completion_time:
                # Higher time spent could indicate more engagement (up to a point)
                time_engagement = min(avg_completion_time / 3600, 30)  # Cap at 30 (for 30+ hours)
                engagement_score += time_engagement * 0.3

            return {
                "content_id": content_id,
                "total_attempts": total_attempts,
                "completed_attempts": completed_attempts,
                "completion_rate": round(completion_rate, 2),
                "avg_completion_time": avg_completion_time,
                "engagement_score": round(min(engagement_score, 100), 2)
            }

        except Exception as e:
            logger.error(f"Error getting content engagement metrics: {e}")
            raise

    def get_course_completion_insights(self, db: Session, user_id: UUID, course_id: UUID) -> Dict[str, Any]:
        """
        Get detailed insights about user's progress in a specific course
        """
        try:
            # Get all content in the course
            course_content = db.query(Content).filter(
                Content.course_id == course_id
            ).all()

            # Get user's progress for this course
            user_progress = db.query(Progress).filter(
                Progress.user_id == user_id,
                Progress.content_id.in_([c.id for c in course_content])
            ).all()

            # Create a mapping of content_id to progress
            progress_map = {p.content_id: p for p in user_progress}

            # Calculate course-level metrics
            completed_content = [c for c in course_content if
                               c.id in progress_map and
                               progress_map[c.id].status == ProgressStatus.COMPLETED]

            in_progress_content = [c for c in course_content if
                                  c.id in progress_map and
                                  progress_map[c.id].status == ProgressStatus.IN_PROGRESS]

            course_completion_rate = (len(completed_content) / len(course_content)) * 100 if course_content else 0

            # Identify content that hasn't been started
            not_started_content = [c for c in course_content if c.id not in progress_map]

            # Calculate time estimates
            completed_times = [p.time_spent_seconds for p in user_progress
                             if p.status == ProgressStatus.COMPLETED and p.time_spent_seconds]
            avg_completion_time = sum(completed_times) / len(completed_times) if completed_times else None

            estimated_remaining_time = None
            if avg_completion_time and not_started_content:
                estimated_remaining_time = avg_completion_time * len(not_started_content)

            return {
                "user_id": user_id,
                "course_id": course_id,
                "total_content": len(course_content),
                "completed_content": len(completed_content),
                "in_progress_content": len(in_progress_content),
                "not_started_content": len(not_started_content),
                "course_completion_rate": round(course_completion_rate, 2),
                "estimated_completion_time_remaining": estimated_remaining_time,
                "content_breakdown": {
                    "completed": [{"id": c.id, "title": c.title} for c in completed_content],
                    "in_progress": [{"id": c.id, "title": c.title} for c in in_progress_content],
                    "not_started": [{"id": c.id, "title": c.title} for c in not_started_content]
                }
            }

        except Exception as e:
            logger.error(f"Error getting course completion insights: {e}")
            raise