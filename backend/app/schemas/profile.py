"""
Pydantic schemas for user profile and onboarding.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class OnboardingRequest(BaseModel):
    """
    Schema for user onboarding data submission.

    All fields are optional to allow progressive form filling.
    """

    # User Information
    full_name: Optional[str] = Field(None, min_length=2, max_length=255, description="User's full name")

    # Personal Information
    age: Optional[int] = Field(None, ge=13, le=120, description="User age in years")
    gender: Optional[str] = Field(None, description="Gender: male, female, other, prefer_not_to_say")
    height_cm: Optional[float] = Field(None, ge=50, le=300, description="Height in centimeters")
    weight_kg: Optional[float] = Field(None, ge=20, le=500, description="Weight in kilograms")

    # Fitness Background
    experience_level: Optional[str] = Field(None, description="Experience level: beginner, intermediate, advanced")
    primary_sport: Optional[str] = Field(None, description="Primary sport or activity")
    secondary_sports: Optional[List[str]] = Field(None, description="List of secondary sports")
    years_training: Optional[int] = Field(None, ge=0, le=100, description="Years of training experience")

    # Goals
    fitness_goals: Optional[List[str]] = Field(
        None,
        description="List of fitness goals: muscle_gain, weight_loss, strength, endurance, flexibility, etc."
    )

    # Limitations & Health
    injuries: Optional[List[str]] = Field(None, description="Current or past injuries")
    health_conditions: Optional[List[str]] = Field(None, description="Health conditions to consider")
    medications: Optional[List[str]] = Field(None, description="Current medications")

    # Availability & Preferences
    available_days_per_week: Optional[int] = Field(None, ge=1, le=7, description="Days available for training per week")
    preferred_session_duration: Optional[int] = Field(None, ge=15, le=300, description="Preferred session duration in minutes")
    preferred_training_times: Optional[List[str]] = Field(
        None,
        description="Preferred training times: morning, afternoon, evening, night"
    )

    # Equipment & Access
    has_gym_membership: Optional[bool] = Field(None, description="Has gym membership")
    available_equipment: Optional[List[str]] = Field(None, description="Available equipment at home")
    training_location: Optional[str] = Field(
        None,
        description="Training location preference: home, gym, outdoor, hybrid"
    )

    @validator('gender')
    def validate_gender(cls, v):
        """Validate gender values."""
        if v is not None:
            allowed = ['male', 'female', 'other', 'prefer_not_to_say']
            if v.lower() not in allowed:
                raise ValueError(f"Gender must be one of: {', '.join(allowed)}")
        return v.lower() if v else v

    @validator('experience_level')
    def validate_experience_level(cls, v):
        """Validate experience level."""
        if v is not None:
            allowed = ['beginner', 'intermediate', 'advanced']
            if v.lower() not in allowed:
                raise ValueError(f"Experience level must be one of: {', '.join(allowed)}")
        return v.lower() if v else v

    @validator('training_location')
    def validate_training_location(cls, v):
        """Validate training location."""
        if v is not None:
            allowed = ['home', 'gym', 'outdoor', 'hybrid']
            if v.lower() not in allowed:
                raise ValueError(f"Training location must be one of: {', '.join(allowed)}")
        return v.lower() if v else v

    class Config:
        json_schema_extra = {
            "example": {
                "age": 28,
                "gender": "male",
                "height_cm": 175,
                "weight_kg": 75,
                "experience_level": "intermediate",
                "primary_sport": "boxing",
                "secondary_sports": ["gym", "running"],
                "years_training": 3,
                "fitness_goals": ["strength", "endurance", "technique"],
                "injuries": [],
                "health_conditions": [],
                "medications": [],
                "available_days_per_week": 4,
                "preferred_session_duration": 60,
                "preferred_training_times": ["evening"],
                "has_gym_membership": True,
                "available_equipment": ["dumbbells", "pull_up_bar"],
                "training_location": "gym"
            }
        }


class ProfileUpdateRequest(BaseModel):
    """
    Schema for updating user profile.

    All fields are optional to allow partial updates.
    """

    # Personal Information
    age: Optional[int] = Field(None, ge=13, le=120)
    gender: Optional[str] = None
    height_cm: Optional[float] = Field(None, ge=50, le=300)
    weight_kg: Optional[float] = Field(None, ge=20, le=500)

    # Fitness Background
    experience_level: Optional[str] = None
    primary_sport: Optional[str] = None
    secondary_sports: Optional[List[str]] = None
    years_training: Optional[int] = Field(None, ge=0, le=100)

    # Goals
    fitness_goals: Optional[List[str]] = None

    # Limitations & Health
    injuries: Optional[List[str]] = None
    health_conditions: Optional[List[str]] = None
    medications: Optional[List[str]] = None

    # Availability & Preferences
    available_days_per_week: Optional[int] = Field(None, ge=1, le=7)
    preferred_session_duration: Optional[int] = Field(None, ge=15, le=300)
    preferred_training_times: Optional[List[str]] = None

    # Equipment & Access
    has_gym_membership: Optional[bool] = None
    available_equipment: Optional[List[str]] = None
    training_location: Optional[str] = None

    @validator('gender')
    def validate_gender(cls, v):
        if v is not None:
            allowed = ['male', 'female', 'other', 'prefer_not_to_say']
            if v.lower() not in allowed:
                raise ValueError(f"Gender must be one of: {', '.join(allowed)}")
        return v.lower() if v else v

    @validator('experience_level')
    def validate_experience_level(cls, v):
        if v is not None:
            allowed = ['beginner', 'intermediate', 'advanced']
            if v.lower() not in allowed:
                raise ValueError(f"Experience level must be one of: {', '.join(allowed)}")
        return v.lower() if v else v

    @validator('training_location')
    def validate_training_location(cls, v):
        if v is not None:
            allowed = ['home', 'gym', 'outdoor', 'hybrid']
            if v.lower() not in allowed:
                raise ValueError(f"Training location must be one of: {', '.join(allowed)}")
        return v.lower() if v else v


class GoalsUpdateRequest(BaseModel):
    """Schema for updating fitness goals only."""

    fitness_goals: List[str] = Field(
        ...,
        min_items=1,
        description="List of fitness goals"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "fitness_goals": ["muscle_gain", "strength", "endurance"]
            }
        }


class ProfileResponse(BaseModel):
    """
    Schema for profile response.

    Returns complete user profile data.
    """

    # User Info
    user_id: int
    full_name: str

    # Profile Info
    profile_id: int

    # Personal Information
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None

    # Fitness Background
    experience_level: Optional[str] = None
    primary_sport: Optional[str] = None
    secondary_sports: Optional[List[str]] = None
    years_training: Optional[int] = None

    # Goals
    fitness_goals: Optional[List[str]] = None

    # Limitations & Health
    injuries: Optional[List[str]] = None
    health_conditions: Optional[List[str]] = None
    medications: Optional[List[str]] = None

    # Availability & Preferences
    available_days_per_week: Optional[int] = None
    preferred_session_duration: Optional[int] = None
    preferred_training_times: Optional[List[str]] = None

    # Equipment & Access
    has_gym_membership: Optional[bool] = None
    available_equipment: Optional[List[str]] = None
    training_location: Optional[str] = None

    # Onboarding Status
    onboarding_completed: bool
    onboarding_completed_at: Optional[datetime] = None
    profile_completion_percentage: int

    # Timestamps
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enables ORM mode (formerly orm_mode in Pydantic v1)
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "full_name": "Default User",
                "profile_id": 1,
                "age": 28,
                "gender": "male",
                "height_cm": 175.0,
                "weight_kg": 75.0,
                "experience_level": "intermediate",
                "primary_sport": "boxing",
                "secondary_sports": ["gym", "running"],
                "years_training": 3,
                "fitness_goals": ["strength", "endurance", "technique"],
                "injuries": [],
                "health_conditions": [],
                "medications": [],
                "available_days_per_week": 4,
                "preferred_session_duration": 60,
                "preferred_training_times": ["evening"],
                "has_gym_membership": True,
                "available_equipment": ["dumbbells", "pull_up_bar"],
                "training_location": "gym",
                "onboarding_completed": True,
                "onboarding_completed_at": "2025-12-03T10:00:00",
                "profile_completion_percentage": 95,
                "created_at": "2025-12-01T10:00:00",
                "updated_at": "2025-12-03T10:00:00"
            }
        }


class ProfileStatusResponse(BaseModel):
    """Schema for profile status check."""

    exists: bool
    onboarding_completed: bool
    profile_completion_percentage: int

    class Config:
        json_schema_extra = {
            "example": {
                "exists": True,
                "onboarding_completed": True,
                "profile_completion_percentage": 95
            }
        }


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str
    success: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Profile updated successfully",
                "success": True
            }
        }
