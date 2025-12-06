"""
Example: SQLAlchemy Database Model Pattern for CoachX

This file demonstrates the standard pattern for creating database models
in the CoachX project. All new models should follow this structure.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List


# Base class for all models
class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class User(Base):
    """
    User model representing a training app user.
    
    This model stores all user profile information collected during
    onboarding, including their sport preference, experience level,
    and training goals.
    
    Relationships:
        - One user has many workout plans (one-to-many)
        - One user has many chat messages (one-to-many)
    """
    
    __tablename__ = "users"
    
    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # User Profile Fields
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    weight_kg: Mapped[Optional[float]] = mapped_column(nullable=True)
    height_cm: Mapped[Optional[float]] = mapped_column(nullable=True)
    
    # Training Preferences
    sport: Mapped[str] = mapped_column(String(50), nullable=False)
    # Valid values: boxing, crossfit, gym, calisthenics, running
    
    experience_level: Mapped[str] = mapped_column(String(20), nullable=False)
    # Valid values: beginner, intermediate, advanced
    
    days_per_week: Mapped[int] = mapped_column(Integer, nullable=False)
    # Valid range: 1-7
    
    goals: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    limitations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
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
    
    def to_dict(self) -> dict:
        """Convert model to dictionary for JSON responses."""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "weight_kg": self.weight_kg,
            "height_cm": self.height_cm,
            "sport": self.sport,
            "experience_level": self.experience_level,
            "days_per_week": self.days_per_week,
            "goals": self.goals,
            "limitations": self.limitations,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class WorkoutPlan(Base):
    """
    Workout plan model storing AI-generated training programs.
    
    The plan_data field stores the complete workout structure as JSON,
    allowing flexibility for different sports and plan formats.
    
    Relationships:
        - Many plans belong to one user (many-to-one)
    """
    
    __tablename__ = "workout_plans"
    
    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Foreign Key to User
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Plan Details
    duration_weeks: Mapped[int] = mapped_column(Integer, nullable=False)
    plan_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    # Structure: {
    #   "weeks": [...],
    #   "days_per_week": 4,
    #   "sport": "boxing",
    #   "level": "intermediate"
    # }
    
    # Status
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    # Timestamps (REQUIRED)
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
    user: Mapped["User"] = relationship(
        "User",
        back_populates="workout_plans"
    )
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"<WorkoutPlan(id={self.id}, user_id={self.user_id}, "
            f"duration_weeks={self.duration_weeks})>"
        )
    
    def to_dict(self) -> dict:
        """Convert model to dictionary for JSON responses."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "duration_weeks": self.duration_weeks,
            "plan_data": self.plan_data,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ChatMessage(Base):
    """
    Chat message model for storing conversation history.
    
    Stores both user messages and AI responses to maintain
    conversation context for the RAG-powered chat system.
    
    Relationships:
        - Many messages belong to one user (many-to-one)
    """
    
    __tablename__ = "chat_messages"
    
    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Foreign Key to User
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Message Details
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    # Valid values: "user" or "assistant"
    
    message: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Optional: Store RAG context used for this message
    rag_context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps (REQUIRED)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True  # Index for ordering by time
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="chat_messages"
    )
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        preview = self.message[:50] + "..." if len(self.message) > 50 else self.message
        return (
            f"<ChatMessage(id={self.id}, user_id={self.user_id}, "
            f"role='{self.role}', message='{preview}')>"
        )
    
    def to_dict(self) -> dict:
        """Convert model to dictionary for JSON responses."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "role": self.role,
            "message": self.message,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# Key Patterns to Follow:
#
# 1. Model Structure:
#    - Inherit from Base (DeclarativeBase)
#    - Use __tablename__ for table name
#    - Use Mapped[] for type hints
#    - Use mapped_column() for columns
#
# 2. Primary Keys:
#    - Always use Integer primary key
#    - Always add index=True
#    - Name it simply: id
#
# 3. Foreign Keys:
#    - Use ForeignKey() with table.column
#    - Add ondelete="CASCADE" for automatic cleanup
#    - Add index=True for query performance
#    - Use plural for parent table name
#
# 4. Timestamps:
#    - ALWAYS include created_at
#    - ALWAYS include updated_at with onupdate
#    - Use datetime.utcnow as default
#    - Make them non-nullable
#
# 5. Relationships:
#    - Use relationship() for ORM relationships
#    - Always add back_populates on both sides
#    - Use cascade for child deletions
#    - Use List[] type hint for one-to-many
#
# 6. Helper Methods:
#    - Add __repr__() for debugging
#    - Add to_dict() for JSON serialization
#    - Keep methods simple and focused
#
# 7. Field Naming:
#    - Use snake_case for all fields
#    - Use descriptive names
#    - Add _id suffix for foreign keys
#    - Add _at suffix for timestamps
#
# 8. Validation:
#    - Add comments for valid values
#    - Use nullable=False for required fields
#    - Use Optional[] type hint for nullable fields
#    - Document constraints in docstrings
#
# 9. JSON Fields:
#    - Use JSON type for flexible data
#    - Document structure in comments
#    - Use dict type hint
#
# 10. Indexes:
#     - Add index=True for foreign keys
#     - Add index=True for frequently queried fields
#     - Add index=True for timestamp if ordering needed
