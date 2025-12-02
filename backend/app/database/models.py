"""
Database models for CoachX.

All models follow SQLAlchemy 2.0 syntax with Mapped types.
"""

from sqlalchemy import Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class User(Base):
    """
    User model representing a CoachX user.

    Stores user profile information collected during onboarding including
    sport preference, experience level, and training goals.

    Relationships:
        - One user has many workout plans (one-to-many)
        - One user has many chat messages (one-to-many)
    """

    __tablename__ = "users"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Profile Fields
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    # Training Preferences
    sport: Mapped[str] = mapped_column(String(50), nullable=False)
    # Valid: boxing, crossfit, gym, calisthenics, running

    experience_level: Mapped[str] = mapped_column(String(20), nullable=False)
    # Valid: beginner, intermediate, advanced

    days_per_week: Mapped[int] = mapped_column(Integer, nullable=False)
    # Valid: 1-7

    goals: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Timestamps (REQUIRED for all models)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    workout_plans: Mapped[List["WorkoutPlan"]] = relationship(
        "WorkoutPlan",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    chat_messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<User(id={self.id}, name='{self.name}', sport='{self.sport}')>"


class WorkoutPlan(Base):
    """
    Workout plan model.

    Stores AI-generated workout plans for users. plan_data is stored as
    JSON for flexibility in structure.

    Relationships:
        - Many workout plans belong to one user (many-to-one)
    """

    __tablename__ = "workout_plans"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Foreign Key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Plan Data (flexible JSON structure)
    plan_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    duration_weeks: Mapped[int] = mapped_column(Integer, nullable=False)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="workout_plans")

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<WorkoutPlan(id={self.id}, user_id={self.user_id})>"


class ChatMessage(Base):
    """
    Chat message model.

    Stores conversation history between user and AI assistant.

    Relationships:
        - Many chat messages belong to one user (many-to-one)
    """

    __tablename__ = "chat_messages"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Foreign Key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Message Data
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    # Valid: "user" or "assistant"

    message: Mapped[str] = mapped_column(Text, nullable=False)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="chat_messages")

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<ChatMessage(id={self.id}, role='{self.role}')>"
