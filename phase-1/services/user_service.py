from sqlalchemy.orm import Session
from models.user import User, SubscriptionTier, SubscriptionStatus
from schemas.user_schemas import UserCreate, UserUpdate
from typing import Optional
import uuid
from datetime import datetime

class UserService:
    def __init__(self):
        pass

    def get_user_by_id(self, db: Session, user_id: uuid.UUID) -> Optional[User]:
        """Get a user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get a user by email"""
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        user = User(
            email=user_data.email,
            name=user_data.name,
            subscription_tier=user_data.subscription_tier or SubscriptionTier.FREE,
            subscription_status=SubscriptionStatus.ACTIVE
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update_user(self, db: Session, user_id: uuid.UUID, user_data: UserUpdate) -> Optional[User]:
        """Update a user"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            if user_data.name is not None:
                user.name = user_data.name
            if user_data.subscription_tier is not None:
                user.subscription_tier = user_data.subscription_tier
            if user_data.subscription_status is not None:
                user.subscription_status = user_data.subscription_status
            user.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(user)
        return user

    def verify_subscription_status(self, db: Session, user_id: uuid.UUID) -> bool:
        """Verify if a user has an active subscription"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user.subscription_status == SubscriptionStatus.ACTIVE
        return False

    def get_subscription_tier(self, db: Session, user_id: uuid.UUID) -> Optional[SubscriptionTier]:
        """Get the subscription tier of a user"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user.subscription_tier
        return None