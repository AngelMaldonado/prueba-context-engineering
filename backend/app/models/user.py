"""
User model for CoachX.

For MVP: Single user with id=1 (no authentication).
Post-MVP: Will support multiple users with authentication.
"""

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.models import Base


class MVPUser(Base):
    """
    User model for MVP (single user, no authentication).

    For MVP, only one user exists with id=1.
    """
    __tablename__ = "mvp_users"

    id = Column(Integer, primary_key=True, default=1)
    full_name = Column(String(255), nullable=False, default="Default User")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    profile = relationship("MVPUserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    # Constraint: Only allow id=1 for MVP
    __table_args__ = (
        CheckConstraint('id = 1', name='mvp_single_user'),
    )

    def __repr__(self):
        return f"<MVPUser(id={self.id}, name='{self.full_name}')>"
