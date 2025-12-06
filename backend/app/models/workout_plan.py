"""
Workout Plan model for CoachX MVP.

Stores AI-generated workout plans for the single MVP user.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional

from app.database.models import Base


class MVPWorkoutPlan(Base):
    """
    Workout plan model for MVP (single user).

    Stores AI-generated personalized workout plans with detailed structure.
    Each plan includes weekly schedule, exercises, and progression guidelines.
    """
    __tablename__ = "mvp_workout_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('mvp_users.id', ondelete='CASCADE'), nullable=False, default=1)

    # Plan Metadata
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    duration_weeks = Column(Integer, nullable=False)  # Plan duration in weeks

    # Plan Structure (JSON)
    # Format: {
    #   "week_1": [
    #     {
    #       "day": "Monday",
    #       "focus": "Upper Body",
    #       "exercises": [
    #         {
    #           "name": "Push-ups",
    #           "sets": 3,
    #           "reps": "12-15",
    #           "rest_seconds": 60,
    #           "notes": "Keep core tight"
    #         }
    #       ]
    #     }
    #   ]
    # }
    plan_structure = Column(JSON, nullable=False)

    # AI Generation Context
    generation_prompt = Column(Text, nullable=True)  # Prompt used to generate this plan
    sport_focus = Column(String(50), nullable=True)  # boxing, crossfit, gym, etc.

    # Status
    is_active = Column(Boolean, default=True, nullable=False)  # Only one active plan at a time
    completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("MVPUser", backref="workout_plans")

    # Constraint: Only allow user_id=1 for MVP
    __table_args__ = (
        CheckConstraint('user_id = 1', name='mvp_single_user_workout'),
    )

    def __repr__(self):
        return f"<MVPWorkoutPlan(id={self.id}, title='{self.title}', active={self.is_active})>"
