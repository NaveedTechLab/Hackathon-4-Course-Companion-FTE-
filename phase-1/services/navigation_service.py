from sqlalchemy.orm import Session
from models.content import Content
from models.course import Course
from models.progress import Progress, ProgressStatus
from typing import Optional, List
import uuid

class NavigationService:
    def __init__(self):
        pass

    def get_course_structure(self, db: Session, course_id: uuid.UUID) -> List[Content]:
        """Get the hierarchical structure of a course"""
        return db.query(Content).filter(
            Content.course_id == course_id
        ).order_by(Content.created_at).all()

    def get_next_content(self, db: Session, user_id: uuid.UUID, course_id: uuid.UUID) -> Optional[Content]:
        """Get the next available content based on user's progress in the course"""
        # Get all content for the course ordered by creation date
        course_contents = db.query(Content).filter(
            Content.course_id == course_id
        ).order_by(Content.created_at).all()

        # Get user's progress for each content item
        completed_content_ids = set()
        for content in course_contents:
            progress = db.query(Progress).filter(
                Progress.user_id == user_id,
                Progress.content_id == content.id
            ).first()

            if progress and progress.status == ProgressStatus.COMPLETED:
                completed_content_ids.add(content.id)

        # Find the first non-completed content item
        for content in course_contents:
            if content.id not in completed_content_ids:
                return content

        # If all content is completed, return None
        return None

    def get_prev_content(self, db: Session, user_id: uuid.UUID, course_id: uuid.UUID, current_content_id: uuid.UUID) -> Optional[Content]:
        """Get the previous content item in the course sequence"""
        # Get all content for the course ordered by creation date
        course_contents = db.query(Content).filter(
            Content.course_id == course_id
        ).order_by(Content.created_at).all()

        # Find the current content index and return the previous one
        current_index = None
        for i, content in enumerate(course_contents):
            if content.id == current_content_id:
                current_index = i
                break

        if current_index is not None and current_index > 0:
            return course_contents[current_index - 1]

        return None

    def get_content_position(self, db: Session, course_id: uuid.UUID, content_id: uuid.UUID) -> Optional[int]:
        """Get the position of a content item within a course"""
        course_contents = db.query(Content).filter(
            Content.course_id == course_id
        ).order_by(Content.created_at).all()

        for i, content in enumerate(course_contents):
            if content.id == content_id:
                return i

        return None

    def get_course_progress_percentage(self, db: Session, user_id: uuid.UUID, course_id: uuid.UUID) -> float:
        """Calculate the overall progress percentage for a course"""
        course_contents = db.query(Content).filter(
            Content.course_id == course_id
        ).all()

        if not course_contents:
            return 0.0

        completed_count = 0
        for content in course_contents:
            progress = db.query(Progress).filter(
                Progress.user_id == user_id,
                Progress.content_id == content.id
            ).first()

            if progress and progress.status == ProgressStatus.COMPLETED:
                completed_count += 1

        return (completed_count / len(course_contents)) * 100.0

    def is_prerequisite_completed(self, db: Session, user_id: uuid.UUID, content_id: uuid.UUID) -> bool:
        """Check if prerequisites for a content item are completed"""
        # For now, we'll consider the previous content in sequence as a prerequisite
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            return False

        # Get the course this content belongs to
        course = db.query(Course).filter(Course.id == content.course_id).first()
        if not course:
            return False

        # Get all content in the course ordered by creation date
        course_contents = db.query(Content).filter(
            Content.course_id == course.id
        ).order_by(Content.created_at).all()

        # Find the current content and check if the previous one is completed
        current_index = None
        for i, c in enumerate(course_contents):
            if c.id == content_id:
                current_index = i
                break

        # If this is the first content item, no prerequisites
        if current_index == 0:
            return True

        # Check if the previous content is completed
        prev_content = course_contents[current_index - 1]
        progress = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.content_id == prev_content.id
        ).first()

        return progress and progress.status == ProgressStatus.COMPLETED