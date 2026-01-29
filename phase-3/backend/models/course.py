from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Enum as SQLEnum

class CourseStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class Course(Base):
    """
    Database model for course information
    """
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))  # Foreign key to User
    status = Column(SQLEnum(CourseStatus), default=CourseStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    enrollment_count = Column(Integer, default=0)

    # Relationship
    creator = relationship("User", back_populates="created_courses")

    def is_published(self) -> bool:
        """Check if course is published and available"""
        return self.status == CourseStatus.PUBLISHED

    def __repr__(self):
        return f"<Course(id={self.id}, title={self.title}, status={self.status.value})>"


# Add relationship to User model if it doesn't exist in the user model file
# This should be added to the User model file as well:
"""
creator_courses = relationship("Course", back_populates="creator", foreign_keys=[Course.creator_id])
enrolled_courses = relationship("Course", secondary="enrollments", back_populates="enrolled_users")
"""

class Enrollment(Base):
    """
    Database model for user course enrollment
    """
    __tablename__ = "enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    progress_percentage = Column(Integer, default=0)  # 0-100

    # Relationships
    user = relationship("User")
    course = relationship("Course")

    def __repr__(self):
        return f"<Enrollment(user_id={self.user_id}, course_id={self.course_id}, progress={self.progress_percentage}%)>"