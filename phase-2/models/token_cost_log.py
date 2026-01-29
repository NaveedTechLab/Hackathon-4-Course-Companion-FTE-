from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
from datetime import datetime
import uuid

class TokenCostLog(Base):
    """
    Database model for tracking token usage and costs per request
    """
    __tablename__ = "token_cost_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # Links to User table
    feature_type = Column(String, nullable=False)  # e.g., "adaptive_learning", "assessment_grading", "synthesis"
    request_id = Column(String, nullable=False)  # Unique identifier for the request
    tokens_input = Column(Integer, default=0)  # Number of input tokens used
    tokens_output = Column(Integer, default=0)  # Number of output tokens generated
    total_tokens = Column(Integer, default=0)  # Total tokens (input + output)
    estimated_cost_usd = Column(Numeric(precision=10, scale=6), default=0.0)  # Estimated cost in USD
    model_used = Column(String, nullable=False)  # Which model was used (e.g., "claude-3-sonnet-20240229")
    created_at = Column(DateTime, default=datetime.utcnow)
    request_metadata = Column(Text)  # JSON serialized metadata about the request

    def __repr__(self):
        return f"<TokenCostLog(user_id={self.user_id}, feature={self.feature_type}, cost=${self.estimated_cost_usd})>"