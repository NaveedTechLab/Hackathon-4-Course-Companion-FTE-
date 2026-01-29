from sqlalchemy.orm import Session
from ..models.course import Course, Enrollment
from ..models.content import Content
from ..models.progress import Progress, ProgressStatus
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

class NavigationService:
    """
    Service for course navigation and content sequencing
    This is a deterministic service that handles navigation without any LLM integration
    """

    def __init__(self):
        pass

    def get_course_structure(self, db: Session, course_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        Get the hierarchical structure of a course
        """
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return None

        # Get all content for the course
        course_content = db.query(Content).filter(
            Content.course_id == course_id
        ).order_by(Content.position).all()

        # Group content by chapters/sections if they have chapter metadata
        chapters = []
        current_chapter = None
        chapter_contents = []

        for content in course_content:
            # Simple grouping by content metadata - in a real implementation,
            # this might use a more sophisticated chapter structure
            content_metadata = content.content_metadata or "{}"

            # Group content by chapter if specified in metadata
            # For now, we'll group by position ranges to simulate chapters
            chapter_position = content.position // 5  # Group every 5 items as a chapter

            if current_chapter != chapter_position:
                if current_chapter is not None:
                    chapters.append({
                        "chapter_number": current_chapter + 1,
                        "title": f"Chapter {current_chapter + 1}",
                        "content_items": chapter_contents
                    })

                current_chapter = chapter_position
                chapter_contents = []

            chapter_contents.append({
                "id": content.id,
                "title": content.title,
                "content_type": content.content_type.value,
                "position": content.position,
                "created_at": content.created_at
            })

        # Add the last chapter
        if current_chapter is not None:
            chapters.append({
                "chapter_number": current_chapter + 1,
                "title": f"Chapter {current_chapter + 1}",
                "content_items": chapter_contents
            })

        return {
            "course_id": course_id,
            "title": course.title,
            "chapters": chapters,
            "total_chapters": len(chapters),
            "total_content_items": len(course_content)
        }

    def get_next_content(self, db: Session, user_id: uuid.UUID, course_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        Get the next content item based on user's progress in the course
        """
        # Get all content for the course ordered by position
        course_content = db.query(Content).filter(
            Content.course_id == course_id
        ).order_by(Content.position).all()

        if not course_content:
            return None

        # Get user's progress for each content item in the course
        user_progress = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.content_id.in_([c.id for c in course_content])
        ).all()

        # Create a map of content_id to progress status
        progress_map = {p.content_id: p.status for p in user_progress}

        # Find the first incomplete content item
        for content in course_content:
            status = progress_map.get(content.id, ProgressStatus.NOT_STARTED)
            if status != ProgressStatus.COMPLETED:
                return {
                    "id": content.id,
                    "title": content.title,
                    "content_type": content.content_type.value,
                    "position": content.position,
                    "progress_status": status.value,
                    "course_id": course_id
                }

        # If all content is completed, return None
        return None

    def get_prev_content(self, db: Session, course_id: uuid.UUID, current_content_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        Get the previous content item in the course sequence
        """
        # Get all content for the course ordered by position
        course_content = db.query(Content).filter(
            Content.course_id == course_id
        ).order_by(Content.position).all()

        if not course_content:
            return None

        # Find the current content item
        current_index = None
        for i, content in enumerate(course_content):
            if content.id == current_content_id:
                current_index = i
                break

        # If current content is found and not the first item, return previous
        if current_index is not None and current_index > 0:
            prev_content = course_content[current_index - 1]
            return {
                "id": prev_content.id,
                "title": prev_content.title,
                "content_type": prev_content.content_type.value,
                "position": prev_content.position,
                "course_id": course_id
            }

        return None

    def set_bookmark(self, db: Session, user_id: uuid.UUID, content_id: uuid.UUID,
                     position: int, note: str = None) -> Dict[str, Any]:
        """
        Set a bookmark for content position
        """
        from ..models.bookmark import Bookmark

        # Check if bookmark already exists
        existing_bookmark = db.query(Bookmark).filter(
            Bookmark.user_id == user_id,
            Bookmark.content_id == content_id
        ).first()

        if existing_bookmark:
            # Update existing bookmark
            existing_bookmark.position = position
            existing_bookmark.note = note
            existing_bookmark.updated_at = datetime.utcnow()
        else:
            # Create new bookmark
            from ..models.bookmark import Bookmark as BookmarkModel
            new_bookmark = BookmarkModel(
                user_id=user_id,
                content_id=content_id,
                position=position,
                note=note
            )
            db.add(new_bookmark)

        db.commit()

        return {
            "user_id": user_id,
            "content_id": content_id,
            "position": position,
            "note": note,
            "bookmarked_at": datetime.utcnow()
        }

    def get_user_bookmarks(self, db: Session, user_id: uuid.UUID, course_id: uuid.UUID = None) -> List[Dict[str, Any]]:
        """
        Get user's bookmarks, optionally filtered by course
        """
        from ..models.bookmark import Bookmark

        query = db.query(Bookmark).filter(Bookmark.user_id == user_id)

        if course_id:
            query = query.join(Content).filter(Content.course_id == course_id)

        bookmarks = query.all()

        bookmark_list = []
        for bookmark in bookmarks:
            # Get content details
            content = db.query(Content).filter(Content.id == bookmark.content_id).first()

            bookmark_list.append({
                "content_id": bookmark.content_id,
                "content_title": content.title if content else "Unknown",
                "position": bookmark.position,
                "note": bookmark.note,
                "bookmarked_at": bookmark.created_at
            })

        return bookmark_list

    def get_content_position(self, db: Session, course_id: uuid.UUID, content_id: uuid.UUID) -> Optional[int]:
        """
        Get the position of a content item within a course
        """
        content = db.query(Content).filter(
            Content.course_id == course_id,
            Content.id == content_id
        ).first()

        if content:
            return content.position

        return None

    def get_course_progress_percentage(self, db: Session, user_id: uuid.UUID, course_id: uuid.UUID) -> float:
        """
        Calculate the overall progress percentage for a course
        """
        # Get all content for the course
        course_content = db.query(Content).filter(
            Content.course_id == course_id
        ).all()

        if not course_content:
            return 0.0

        # Get user's progress for content in this course
        completed_content = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.content_id.in_([c.id for c in course_content]),
            Progress.status == ProgressStatus.COMPLETED
        ).count()

        return (completed_content / len(course_content)) * 100 if course_content else 0.0

    def get_course_navigation_path(self, db: Session, user_id: uuid.UUID, course_id: uuid.UUID) -> List[Dict[str, Any]]:
        """
        Get the complete navigation path for a course with progress indicators
        """
        course_structure = self.get_course_structure(db, course_id)
        if not course_structure:
            return []

        # Get all user progress for this course
        course_content_ids = []
        for chapter in course_structure["chapters"]:
            for content_item in chapter["content_items"]:
                course_content_ids.append(content_item["id"])

        user_progress = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.content_id.in_(course_content_ids)
        ).all()

        # Create progress map
        progress_map = {p.content_id: p.status for p in user_progress}

        # Update content items with progress status
        for chapter in course_structure["chapters"]:
            for content_item in chapter["content_items"]:
                content_item["progress_status"] = progress_map.get(
                    content_item["id"], ProgressStatus.NOT_STARTED.value
                )

        return course_structure