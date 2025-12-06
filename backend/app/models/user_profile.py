"""
UserProfile model for CoachX.

Stores detailed fitness information from user onboarding.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import json

from app.database.models import Base


class MVPUserProfile(Base):
    """
    User profile with detailed fitness information.

    Stores all onboarding data: personal info, fitness background,
    goals, limitations, availability, and equipment access.
    """
    __tablename__ = "mvp_user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('mvp_users.id', ondelete='CASCADE'), nullable=False, default=1)

    # Personal Information
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)  # male, female, other, prefer_not_to_say
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)

    # Fitness Background
    experience_level = Column(String(50), nullable=True)  # beginner, intermediate, advanced
    primary_sport = Column(String(100), nullable=True)  # boxing, crossfit, gym, running, etc.
    secondary_sports = Column(Text, nullable=True)  # JSON array
    years_training = Column(Integer, nullable=True)

    # Goals (JSON array of strings)
    fitness_goals = Column(Text, nullable=True)  # JSON: ["muscle_gain", "strength", ...]

    # Limitations & Health (JSON arrays)
    injuries = Column(Text, nullable=True)  # JSON: ["knee_injury", ...]
    health_conditions = Column(Text, nullable=True)  # JSON: ["asthma", ...]
    medications = Column(Text, nullable=True)  # JSON: ["ibuprofen", ...]

    # Availability & Preferences
    available_days_per_week = Column(Integer, nullable=True)  # 1-7
    preferred_session_duration = Column(Integer, nullable=True)  # minutes
    preferred_training_times = Column(Text, nullable=True)  # JSON: ["morning", "evening"]

    # Equipment & Access
    has_gym_membership = Column(Boolean, nullable=True)
    available_equipment = Column(Text, nullable=True)  # JSON: ["dumbbells", "barbell", ...]
    training_location = Column(String(50), nullable=True)  # home, gym, outdoor, hybrid

    # Onboarding Status
    onboarding_completed = Column(Boolean, default=False, nullable=False)
    onboarding_completed_at = Column(DateTime(timezone=True), nullable=True)
    profile_completion_percentage = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("MVPUser", back_populates="profile")

    # Constraint: Only allow user_id=1 for MVP
    __table_args__ = (
        CheckConstraint('user_id = 1', name='mvp_single_user_profile'),
    )

    def __repr__(self):
        return f"<MVPUserProfile(id={self.id}, user_id={self.user_id}, sport='{self.primary_sport}', completed={self.onboarding_completed})>"

    # Helper methods for JSON fields
    def get_secondary_sports(self):
        """Get secondary sports as Python list."""
        if self.secondary_sports:
            try:
                return json.loads(self.secondary_sports)
            except:
                return []
        return []

    def set_secondary_sports(self, sports_list):
        """Set secondary sports from Python list."""
        self.secondary_sports = json.dumps(sports_list) if sports_list else None

    def get_fitness_goals(self):
        """Get fitness goals as Python list."""
        if self.fitness_goals:
            try:
                return json.loads(self.fitness_goals)
            except:
                return []
        return []

    def set_fitness_goals(self, goals_list):
        """Set fitness goals from Python list."""
        self.fitness_goals = json.dumps(goals_list) if goals_list else None

    def get_injuries(self):
        """Get injuries as Python list."""
        if self.injuries:
            try:
                return json.loads(self.injuries)
            except:
                return []
        return []

    def set_injuries(self, injuries_list):
        """Set injuries from Python list."""
        self.injuries = json.dumps(injuries_list) if injuries_list else None

    def get_health_conditions(self):
        """Get health conditions as Python list."""
        if self.health_conditions:
            try:
                return json.loads(self.health_conditions)
            except:
                return []
        return []

    def set_health_conditions(self, conditions_list):
        """Set health conditions from Python list."""
        self.health_conditions = json.dumps(conditions_list) if conditions_list else None

    def get_medications(self):
        """Get medications as Python list."""
        if self.medications:
            try:
                return json.loads(self.medications)
            except:
                return []
        return []

    def set_medications(self, medications_list):
        """Set medications from Python list."""
        self.medications = json.dumps(medications_list) if medications_list else None

    def get_preferred_training_times(self):
        """Get preferred training times as Python list."""
        if self.preferred_training_times:
            try:
                return json.loads(self.preferred_training_times)
            except:
                return []
        return []

    def set_preferred_training_times(self, times_list):
        """Set preferred training times from Python list."""
        self.preferred_training_times = json.dumps(times_list) if times_list else None

    def get_available_equipment(self):
        """Get available equipment as Python list."""
        if self.available_equipment:
            try:
                return json.loads(self.available_equipment)
            except:
                return []
        return []

    def set_available_equipment(self, equipment_list):
        """Set available equipment from Python list."""
        self.available_equipment = json.dumps(equipment_list) if equipment_list else None
