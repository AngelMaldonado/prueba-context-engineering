"""
Pydantic schemas for workout plans.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class Exercise(BaseModel):
    """Schema for a single exercise."""

    name: str = Field(..., description="Exercise name")
    sets: int = Field(..., ge=1, le=10, description="Number of sets")
    reps: str = Field(..., description="Reps (e.g., '12-15', '10', 'AMRAP')")
    rest_seconds: int = Field(..., ge=0, le=600, description="Rest between sets in seconds")
    notes: Optional[str] = Field(None, description="Additional notes or form cues")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Push-ups",
                "sets": 3,
                "reps": "12-15",
                "rest_seconds": 60,
                "notes": "Keep core tight, full range of motion"
            }
        }


class WorkoutDay(BaseModel):
    """Schema for a single workout day."""

    day: str = Field(..., description="Day of week or day number")
    focus: str = Field(..., description="Workout focus (e.g., 'Upper Body', 'Cardio')")
    exercises: List[Exercise] = Field(..., min_items=1, description="List of exercises")
    duration_minutes: Optional[int] = Field(None, description="Estimated workout duration")
    warmup: Optional[str] = Field(None, description="Warmup instructions")
    cooldown: Optional[str] = Field(None, description="Cooldown instructions")

    class Config:
        json_schema_extra = {
            "example": {
                "day": "Monday",
                "focus": "Upper Body Strength",
                "warmup": "5 min light cardio + dynamic stretches",
                "exercises": [
                    {
                        "name": "Push-ups",
                        "sets": 3,
                        "reps": "12-15",
                        "rest_seconds": 60,
                        "notes": "Modify on knees if needed"
                    }
                ],
                "cooldown": "5 min stretching",
                "duration_minutes": 45
            }
        }


class WorkoutPlanRequest(BaseModel):
    """Schema for requesting a new workout plan generation."""

    duration_weeks: int = Field(default=4, ge=1, le=12, description="Plan duration in weeks")
    custom_notes: Optional[str] = Field(None, description="Additional requirements or notes")

    class Config:
        json_schema_extra = {
            "example": {
                "duration_weeks": 4,
                "custom_notes": "Focus on progressive overload, avoid jumping exercises"
            }
        }


class WorkoutPlanResponse(BaseModel):
    """Schema for workout plan response."""

    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    duration_weeks: int
    plan_structure: Dict[str, Any]  # Flexible structure for weeks/days
    sport_focus: Optional[str] = None
    is_active: bool
    completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "title": "4-Week Beginner Boxing Strength Program",
                "description": "Progressive strength training focused on boxing-specific movements",
                "duration_weeks": 4,
                "plan_structure": {
                    "week_1": [
                        {
                            "day": "Monday",
                            "focus": "Upper Body",
                            "exercises": [
                                {
                                    "name": "Push-ups",
                                    "sets": 3,
                                    "reps": "10-12",
                                    "rest_seconds": 60,
                                    "notes": "Full range of motion"
                                }
                            ]
                        }
                    ]
                },
                "sport_focus": "boxing",
                "is_active": True,
                "completed": False,
                "completed_at": None,
                "created_at": "2025-12-03T10:00:00",
                "updated_at": "2025-12-03T10:00:00"
            }
        }


class WorkoutPlanSummary(BaseModel):
    """Schema for workout plan summary (list view)."""

    id: int
    title: str
    duration_weeks: int
    sport_focus: Optional[str] = None
    is_active: bool
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class WorkoutPlanListResponse(BaseModel):
    """Schema for list of workout plans."""

    plans: List[WorkoutPlanSummary]
    total: int
    active_plan_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "plans": [
                    {
                        "id": 1,
                        "title": "4-Week Beginner Program",
                        "duration_weeks": 4,
                        "sport_focus": "boxing",
                        "is_active": True,
                        "completed": False,
                        "created_at": "2025-12-03T10:00:00"
                    }
                ],
                "total": 1,
                "active_plan_id": 1
            }
        }
