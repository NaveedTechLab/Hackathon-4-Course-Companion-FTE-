from sqlalchemy.orm import Session
from models.progress import Progress, ProgressStatus
from models.user import User
from models.content import Content
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from decimal import Decimal

class ProgressService:
    """
    Service for tracking and managing user progress through courses
    """

    def __init__(self):
        pass

    def get_user_progress(self, db: Session, user_id: uuid.UUID, course_id: uuid.UUID = None) -> Dict[str, Any]:
        """
        Get user's overall progress summary
        """
        query = db.query(Progress).filter(Progress.user_id == user_id)

        if course_id:
            # Get progress for specific course
            from models.content import Content
            query = query.join(Content).filter(Content.course_id == course_id)

        progress_records = query.all()

        if not progress_records:
            return {
                "user_id": user_id,
                "course_id": course_id,
                "total_content": 0,
                "completed_content": 0,
                "in_progress_content": 0,
                "not_started_content": 0,
                "completion_percentage": 0.0,
                "total_time_spent_seconds": 0,
                "current_streak_days": 0,
                "last_active": None
            }

        total_content = len(progress_records)
        completed_content = len([p for p in progress_records if p.status == ProgressStatus.COMPLETED])
        in_progress_content = len([p for p in progress_records if p.status == ProgressStatus.IN_PROGRESS])
        not_started_content = len([p for p in progress_records if p.status == ProgressStatus.NOT_STARTED])

        completion_percentage = (completed_content / total_content * 100) if total_content > 0 else 0

        total_time_spent = sum(p.time_spent_seconds or 0 for p in progress_records)

        # Calculate current streak (simplified approach)
        current_streak = self._calculate_current_streak(db, user_id)

        # Get last active date
        last_active = max((p.updated_at for p in progress_records if p.updated_at), default=None)

        return {
            "user_id": user_id,
            "course_id": course_id,
            "total_content": total_content,
            "completed_content": completed_content,
            "in_progress_content": in_progress_content,
            "not_started_content": not_started_content,
            "completion_percentage": round(completion_percentage, 2),
            "total_time_spent_seconds": total_time_spent,
            "current_streak_days": current_streak,
            "last_active": last_active,
            "progress_distribution": {
                "completed": completed_content,
                "in_progress": in_progress_content,
                "not_started": not_started_content
            }
        }

    def _calculate_current_streak(self, db: Session, user_id: uuid.UUID) -> int:
        """
        Calculate current learning streak in days
        """
        # This is a simplified implementation
        # In a real system, you would check daily activity logs
        from datetime import date, timedelta

        today = date.today()
        streak = 0

        # Check for activity in the last few days to calculate streak
        for i in range(7):  # Look back 7 days to calculate streak
            check_date = today - timedelta(days=i)

            # Query for any progress updates on this date
            activity = db.query(Progress).filter(
                Progress.user_id == user_id,
                Progress.updated_at >= datetime(check_date.year, check_date.month, check_date.day),
                Progress.updated_at < datetime(check_date.year, check_date.month, check_date.day) + timedelta(days=1)
            ).first()

            if activity:
                streak += 1
            else:
                break  # Break at first day without activity

        return streak

    def update_content_progress(
        self,
        db: Session,
        user_id: uuid.UUID,
        content_id: uuid.UUID,
        status: ProgressStatus,
        completion_percentage: float = 0.0,
        time_spent_seconds: int = 0
    ) -> Progress:
        """
        Update progress for a specific content item
        """
        # Check if progress record already exists
        existing_progress = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.content_id == content_id
        ).first()

        if existing_progress:
            # Update existing progress
            existing_progress.status = status
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
                status=status,
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

    def get_content_progress(self, db: Session, user_id: uuid.UUID, content_id: uuid.UUID) -> Optional[Progress]:
        """
        Get progress for a specific content item
        """
        return db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.content_id == content_id
        ).first()

    def get_course_progress_summary(self, db: Session, user_id: uuid.UUID, course_id: uuid.UUID) -> Dict[str, Any]:
        """
        Get detailed progress summary for a specific course
        """
        from models.content import Content

        # Get all content in the course
        course_content = db.query(Content).filter(
            Content.course_id == course_id
        ).all()

        # Get user's progress for each content item in the course
        user_progress = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.content_id.in_([c.id for c in course_content])
        ).all()

        # Create mapping of content_id to progress
        progress_map = {p.content_id: p for p in user_progress}

        # Calculate progress for each content item
        content_progress_details = []
        completed_count = 0
        total_time_spent = 0

        for content in course_content:
            progress = progress_map.get(content.id)
            if progress:
                content_detail = {
                    "content_id": content.id,
                    "title": content.title,
                    "status": progress.status.value,
                    "completion_percentage": float(progress.completion_percentage) if progress.completion_percentage else 0,
                    "time_spent_seconds": progress.time_spent_seconds or 0,
                    "last_accessed": progress.last_accessed
                }

                if progress.status == ProgressStatus.COMPLETED:
                    completed_count += 1
                total_time_spent += progress.time_spent_seconds or 0
            else:
                content_detail = {
                    "content_id": content.id,
                    "title": content.title,
                    "status": ProgressStatus.NOT_STARTED.value,
                    "completion_percentage": 0,
                    "time_spent_seconds": 0,
                    "last_accessed": None
                }

            content_progress_details.append(content_detail)

        # Calculate course completion percentage
        course_completion_percentage = (completed_count / len(course_content) * 100) if course_content else 0

        return {
            "user_id": user_id,
            "course_id": course_id,
            "total_content_items": len(course_content),
            "completed_items": completed_count,
            "completion_percentage": round(course_completion_percentage, 2),
            "total_time_spent_seconds": total_time_spent,
            "content_progress": content_progress_details,
            "milestones": self._calculate_course_milestones(content_progress_details),
            "recommendations": self._generate_progress_recommendations(content_progress_details)
        }

    def _calculate_course_milestones(self, content_progress: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculate course milestones based on progress
        """
        milestones = []

        total_content = len(content_progress)
        if total_content == 0:
            return milestones

        # Define milestone thresholds
        milestone_thresholds = [
            {"threshold": 0.25, "name": "Quarter Way Through", "emoji": "🕐"},
            {"threshold": 0.50, "name": "Halfway Complete", "emoji": "🕒"},
            {"threshold": 0.75, "name": "Almost Done", "emoji": "🕔"},
            {"threshold": 1.00, "name": "Course Complete", "emoji": "🎉"}
        ]

        completed_count = len([item for item in content_progress if item["status"] == "completed"])
        completion_percentage = completed_count / total_content

        for milestone in milestone_thresholds:
            threshold_count = int(milestone["threshold"] * total_content)
            if completed_count >= threshold_count and milestone["threshold"] <= completion_percentage:
                milestones.append({
                    "name": milestone["name"],
                    "emoji": milestone["emoji"],
                    "threshold_percentage": milestone["threshold"] * 100,
                    "threshold_count": threshold_count,
                    "achieved": completed_count >= threshold_count,
                    "date_achieved": datetime.utcnow() if completed_count >= threshold_count else None
                })

        return milestones

    def _generate_progress_recommendations(self, content_progress: List[Dict[str, Any]]) -> List[str]:
        """
        Generate recommendations based on user's progress
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

        # Recommendation based on time spent
        avg_time_spent = sum(item["time_spent_seconds"] for item in content_progress) / total_count if total_count > 0 else 0
        if avg_time_spent < 300:  # Less than 5 minutes average
            recommendations.append("Consider spending more time with each content item to deepen your understanding.")

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

    def get_user_learning_insights(self, db: Session, user_id: uuid.UUID) -> Dict[str, Any]:
        """
        Get comprehensive learning insights for a user
        """
        from models.content import Content
        from models.course import Course

        # Get all user progress
        all_progress = db.query(Progress).filter(Progress.user_id == user_id).all()

        if not all_progress:
            return {
                "user_id": user_id,
                "total_courses_started": 0,
                "total_courses_completed": 0,
                "total_content_consumed": 0,
                "average_completion_rate": 0.0,
                "total_learning_time_hours": 0,
                "learning_patterns": [],
                "achievement_insights": []
            }

        # Get content details for progress items
        content_ids = [p.content_id for p in all_progress]
        contents = db.query(Content).filter(Content.id.in_(content_ids)).all()
        content_map = {c.id: c for c in contents}

        # Get course details
        course_ids = [content_map[p.content_id].course_id for p in all_progress if p.content_id in content_map]
        courses = db.query(Course).filter(Course.id.in_(course_ids)).all()
        course_map = {c.id: c for c in courses}

        # Calculate insights
        completed_progress = [p for p in all_progress if p.status == ProgressStatus.COMPLETED]
        total_time_spent = sum(p.time_spent_seconds or 0 for p in all_progress)

        # Group progress by course
        progress_by_course = {}
        for progress in all_progress:
            if progress.content_id in content_map:
                content = content_map[progress.content_id]
                course_id = content.course_id

                if course_id not in progress_by_course:
                    progress_by_course[course_id] = {
                        "course": course_map.get(course_id),
                        "total_content": 0,
                        "completed_content": 0,
                        "time_spent": 0
                    }

                progress_by_course[course_id]["total_content"] += 1
                if progress.status == ProgressStatus.COMPLETED:
                    progress_by_course[course_id]["completed_content"] += 1
                progress_by_course[course_id]["time_spent"] += progress.time_spent_seconds or 0

        # Calculate course completion rates
        completed_courses = 0
        for course_data in progress_by_course.values():
            if course_data["total_content"] > 0:
                completion_rate = course_data["completed_content"] / course_data["total_content"]
                if completion_rate >= 0.9:  # 90% or higher completion rate
                    completed_courses += 1

        # Identify favorite content types
        content_types = [content_map[p.content_id].content_type.value if p.content_id in content_map else "unknown"
                        for p in completed_progress]
        from collections import Counter
        type_counter = Counter(content_types)
        favorite_type = type_counter.most_common(1)[0][0] if type_counter else "unknown"

        return {
            "user_id": user_id,
            "total_courses_started": len(progress_by_course),
            "total_courses_completed": completed_courses,
            "total_content_consumed": len(completed_progress),
            "average_completion_rate": sum(
                data["completed_content"]/data["total_content"] if data["total_content"] > 0 else 0
                for data in progress_by_course.values()
            ) / len(progress_by_course) if progress_by_course else 0,
            "total_learning_time_hours": round(total_time_spent / 3600, 2),
            "favorite_content_type": favorite_type,
            "learning_patterns": [
                f"Prefers {favorite_type} content type",
                f"Spend an average of {round(total_time_spent/len(all_progress)/60, 1)} minutes per content item" if all_progress else "No content completed yet"
            ],
            "achievement_insights": [
                f"Completed {len(completed_progress)} content items",
                f"Spent {round(total_time_spent/3600, 1)} hours learning",
                f"Successfully completed {completed_courses} courses"
            ]
        }

    def update_progress_with_validation(
        self,
        db: Session,
        user_id: uuid.UUID,
        content_id: uuid.UUID,
        status: ProgressStatus,
        completion_percentage: float,
        time_spent_seconds: int
    ) -> Dict[str, Any]:
        """
        Update progress with validation and additional analytics
        """
        # Validate completion percentage range
        if not 0 <= completion_percentage <= 100:
            raise ValueError("Completion percentage must be between 0 and 100")

        # Validate content exists
        from models.content import Content
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            raise ValueError("Content not found")

        # Validate user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # Update progress
        updated_progress = self.update_content_progress(
            db, user_id, content_id, status, completion_percentage, time_spent_seconds
        )

        # Calculate updated course progress
        course_progress = self.get_course_progress_summary(db, user_id, content.course_id)

        # Generate any necessary notifications or achievements
        notifications = self._generate_progress_notifications(updated_progress, course_progress)

        return {
            "progress": updated_progress,
            "course_summary": course_progress,
            "notifications": notifications,
            "message": f"Progress updated for {content.title}"
        }

    def _generate_progress_notifications(self, progress: Progress, course_summary: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate notifications based on progress updates
        """
        notifications = []

        # Achievement notification for completion
        if progress.status == ProgressStatus.COMPLETED:
            notifications.append({
                "type": "achievement",
                "message": f"Congratulations! You've completed {progress.content.title}",
                "icon": "🎉"
            })

        # Milestone notification
        if course_summary["completion_percentage"] in [25, 50, 75, 100]:
            milestone_messages = {
                25: "Quarter way through! Great start!",
                50: "Halfway there! Keep up the good work!",
                75: "Almost done! You're doing fantastic!",
                100: "Course complete! Excellent job!"
            }
            notifications.append({
                "type": "milestone",
                "message": milestone_messages.get(int(course_summary["completion_percentage"]), ""),
                "icon": "👍"
            })

        return notifications