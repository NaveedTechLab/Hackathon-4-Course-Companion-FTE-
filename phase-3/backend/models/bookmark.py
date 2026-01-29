from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base
from datetime import datetime
import uuid

class Bookmark(Base):
    """
    Database model for user content bookmarks
    """
    __tablename__ = "bookmarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Foreign key to User
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id"), nullable=False)  # Foreign key to Content
    position = Column(Integer, default=0)  # Position within the content (e.g., page number, timestamp)
    note = Column(Text)  # Optional note from the user
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="bookmarks")
    content = relationship("Content", back_populates="bookmarks")

    def __repr__(self):
        return f"<Bookmark(user_id={self.user_id}, content_id={self.content_id}, position={self.position})>"