"""
CRUD operations for MVP user profile.

All operations work with the single MVP user (id=1).
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, Dict, Any
from datetime import datetime
import json

from app.models.user import MVPUser
from app.models.user_profile import MVPUserProfile
from app.schemas.profile import OnboardingRequest, ProfileUpdateRequest


def get_or_create_mvp_user(db: Session) -> MVPUser:
    """
    Get or create the single MVP user (id=1).

    Args:
        db: Database session

    Returns:
        MVPUser instance with id=1
    """
    user = db.query(MVPUser).filter(MVPUser.id == 1).first()

    if not user:
        user = MVPUser(id=1, full_name="Default User")
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


def get_profile(db: Session) -> Optional[MVPUserProfile]:
    """
    Get the MVP user profile.

    Args:
        db: Database session

    Returns:
        MVPUserProfile if exists, None otherwise
    """
    return db.query(MVPUserProfile).filter(MVPUserProfile.user_id == 1).first()


def get_or_create_profile(db: Session) -> MVPUserProfile:
    """
    Get or create the MVP user profile.

    Ensures the MVP user exists first.

    Args:
        db: Database session

    Returns:
        MVPUserProfile instance
    """
    # Ensure user exists
    get_or_create_mvp_user(db)

    # Get or create profile
    profile = get_profile(db)

    if not profile:
        profile = MVPUserProfile(user_id=1)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


def calculate_profile_completion(profile: MVPUserProfile) -> int:
    """
    Calculate profile completion percentage.

    Considers only fields that are part of the standard onboarding flow.
    Optional fields (medications, secondary_sports, preferred_training_times) are excluded.

    Args:
        profile: MVPUserProfile instance

    Returns:
        Completion percentage (0-100)
    """
    total_fields = 0
    completed_fields = 0

    # Personal info (4 fields - all required in onboarding)
    personal_fields = [profile.age, profile.gender, profile.height_cm, profile.weight_kg]
    total_fields += len(personal_fields)
    completed_fields += sum(1 for f in personal_fields if f is not None)

    # Fitness background (3 fields - secondary_sports is optional)
    fitness_fields = [
        profile.experience_level,
        profile.primary_sport,
        profile.years_training
    ]
    total_fields += len(fitness_fields)
    completed_fields += sum(1 for f in fitness_fields if f is not None)

    # Goals (1 field but important)
    if profile.fitness_goals:
        completed_fields += 1
    total_fields += 1

    # Health info is completely optional - not counted in completion
    # Users without injuries/conditions should reach 100%

    # Availability (2 fields - preferred_training_times is optional)
    availability_fields = [
        profile.available_days_per_week,
        profile.preferred_session_duration
    ]
    total_fields += len(availability_fields)
    completed_fields += sum(1 for f in availability_fields if f is not None)

    # Equipment (3 fields - all required in onboarding)
    equipment_fields = [
        profile.has_gym_membership,
        profile.available_equipment,
        profile.training_location
    ]
    total_fields += len(equipment_fields)
    completed_fields += sum(1 for f in equipment_fields if f is not None)

    # Calculate percentage
    if total_fields == 0:
        return 0

    return int((completed_fields / total_fields) * 100)


def update_profile_from_onboarding(
    db: Session,
    onboarding_data: OnboardingRequest,
    mark_completed: bool = True
) -> MVPUserProfile:
    """
    Update profile from onboarding data.

    Only updates fields that are provided (not None).

    Args:
        db: Database session
        onboarding_data: OnboardingRequest with user data
        mark_completed: Whether to mark onboarding as completed

    Returns:
        Updated MVPUserProfile
    """
    profile = get_or_create_profile(db)

    # Update user's full name if provided
    if onboarding_data.full_name is not None:
        user = get_or_create_mvp_user(db)
        user.full_name = onboarding_data.full_name
        db.commit()

    # Update personal information
    if onboarding_data.age is not None:
        profile.age = onboarding_data.age
    if onboarding_data.gender is not None:
        profile.gender = onboarding_data.gender
    if onboarding_data.height_cm is not None:
        profile.height_cm = onboarding_data.height_cm
    if onboarding_data.weight_kg is not None:
        profile.weight_kg = onboarding_data.weight_kg

    # Update fitness background
    if onboarding_data.experience_level is not None:
        profile.experience_level = onboarding_data.experience_level
    if onboarding_data.primary_sport is not None:
        profile.primary_sport = onboarding_data.primary_sport
    if onboarding_data.secondary_sports is not None:
        profile.set_secondary_sports(onboarding_data.secondary_sports)
    if onboarding_data.years_training is not None:
        profile.years_training = onboarding_data.years_training

    # Update goals
    if onboarding_data.fitness_goals is not None:
        profile.set_fitness_goals(onboarding_data.fitness_goals)

    # Update limitations & health
    if onboarding_data.injuries is not None:
        profile.set_injuries(onboarding_data.injuries)
    if onboarding_data.health_conditions is not None:
        profile.set_health_conditions(onboarding_data.health_conditions)
    if onboarding_data.medications is not None:
        profile.set_medications(onboarding_data.medications)

    # Update availability
    if onboarding_data.available_days_per_week is not None:
        profile.available_days_per_week = onboarding_data.available_days_per_week
    if onboarding_data.preferred_session_duration is not None:
        profile.preferred_session_duration = onboarding_data.preferred_session_duration
    if onboarding_data.preferred_training_times is not None:
        profile.set_preferred_training_times(onboarding_data.preferred_training_times)

    # Update equipment
    if onboarding_data.has_gym_membership is not None:
        profile.has_gym_membership = onboarding_data.has_gym_membership
    if onboarding_data.available_equipment is not None:
        profile.set_available_equipment(onboarding_data.available_equipment)
    if onboarding_data.training_location is not None:
        profile.training_location = onboarding_data.training_location

    # Mark onboarding as completed if requested
    if mark_completed and not profile.onboarding_completed:
        profile.onboarding_completed = True
        profile.onboarding_completed_at = datetime.utcnow()

    # Calculate and update completion percentage
    profile.profile_completion_percentage = calculate_profile_completion(profile)

    db.commit()
    db.refresh(profile)

    return profile


def update_profile(
    db: Session,
    update_data: ProfileUpdateRequest
) -> MVPUserProfile:
    """
    Update profile with new data.

    Only updates provided fields (partial update).

    Args:
        db: Database session
        update_data: ProfileUpdateRequest with fields to update

    Returns:
        Updated MVPUserProfile
    """
    profile = get_or_create_profile(db)

    # Update personal information
    if update_data.age is not None:
        profile.age = update_data.age
    if update_data.gender is not None:
        profile.gender = update_data.gender
    if update_data.height_cm is not None:
        profile.height_cm = update_data.height_cm
    if update_data.weight_kg is not None:
        profile.weight_kg = update_data.weight_kg

    # Update fitness background
    if update_data.experience_level is not None:
        profile.experience_level = update_data.experience_level
    if update_data.primary_sport is not None:
        profile.primary_sport = update_data.primary_sport
    if update_data.secondary_sports is not None:
        profile.set_secondary_sports(update_data.secondary_sports)
    if update_data.years_training is not None:
        profile.years_training = update_data.years_training

    # Update goals
    if update_data.fitness_goals is not None:
        profile.set_fitness_goals(update_data.fitness_goals)

    # Update limitations & health
    if update_data.injuries is not None:
        profile.set_injuries(update_data.injuries)
    if update_data.health_conditions is not None:
        profile.set_health_conditions(update_data.health_conditions)
    if update_data.medications is not None:
        profile.set_medications(update_data.medications)

    # Update availability
    if update_data.available_days_per_week is not None:
        profile.available_days_per_week = update_data.available_days_per_week
    if update_data.preferred_session_duration is not None:
        profile.preferred_session_duration = update_data.preferred_session_duration
    if update_data.preferred_training_times is not None:
        profile.set_preferred_training_times(update_data.preferred_training_times)

    # Update equipment
    if update_data.has_gym_membership is not None:
        profile.has_gym_membership = update_data.has_gym_membership
    if update_data.available_equipment is not None:
        profile.set_available_equipment(update_data.available_equipment)
    if update_data.training_location is not None:
        profile.training_location = update_data.training_location

    # Recalculate completion percentage
    profile.profile_completion_percentage = calculate_profile_completion(profile)

    db.commit()
    db.refresh(profile)

    return profile


def update_fitness_goals(db: Session, goals: list[str]) -> MVPUserProfile:
    """
    Update only fitness goals.

    Args:
        db: Database session
        goals: List of fitness goals

    Returns:
        Updated MVPUserProfile
    """
    profile = get_or_create_profile(db)
    profile.set_fitness_goals(goals)

    # Recalculate completion percentage
    profile.profile_completion_percentage = calculate_profile_completion(profile)

    db.commit()
    db.refresh(profile)

    return profile


def delete_profile(db: Session) -> bool:
    """
    Delete (reset) the MVP user profile and all associated data.

    Deletes:
    - User profile
    - All workout plans
    - Resets user name

    Creates a new empty profile after deletion.

    Args:
        db: Database session

    Returns:
        True if profile was deleted and recreated
    """
    from app.models.workout_plan import MVPWorkoutPlan

    # Get user
    user = get_or_create_mvp_user(db)

    # Delete all workout plans
    db.query(MVPWorkoutPlan).filter(MVPWorkoutPlan.user_id == user.id).delete()

    # Delete profile
    profile = get_profile(db)
    if profile:
        db.delete(profile)

    # Reset user name
    user.full_name = "MVP User"

    db.commit()

    # Create new empty profile
    get_or_create_profile(db)

    return True


def build_user_context_for_ai(profile: MVPUserProfile) -> str:
    """
    Build a formatted context string about the user for AI prompts.

    This context will be injected into AI chat prompts to personalize responses.

    Args:
        profile: MVPUserProfile instance

    Returns:
        Formatted context string
    """
    context_parts = []

    # Basic info
    if profile.age:
        context_parts.append(f"Age: {profile.age} years old")
    if profile.gender:
        context_parts.append(f"Gender: {profile.gender}")

    # Physical stats
    physical = []
    if profile.height_cm:
        physical.append(f"Height: {profile.height_cm}cm")
    if profile.weight_kg:
        physical.append(f"Weight: {profile.weight_kg}kg")
    if physical:
        context_parts.append(", ".join(physical))

    # Training background
    if profile.experience_level:
        context_parts.append(f"Experience level: {profile.experience_level}")
    if profile.primary_sport:
        context_parts.append(f"Primary sport: {profile.primary_sport}")
    if profile.secondary_sports:
        secondary = profile.get_secondary_sports()
        if secondary:
            context_parts.append(f"Also trains: {', '.join(secondary)}")
    if profile.years_training:
        context_parts.append(f"Training for {profile.years_training} years")

    # Goals
    if profile.fitness_goals:
        goals = profile.get_fitness_goals()
        if goals:
            context_parts.append(f"Goals: {', '.join(goals)}")

    # Limitations
    limitations = []
    if profile.injuries:
        injuries = profile.get_injuries()
        if injuries:
            limitations.append(f"Injuries: {', '.join(injuries)}")
    if profile.health_conditions:
        conditions = profile.get_health_conditions()
        if conditions:
            limitations.append(f"Health conditions: {', '.join(conditions)}")
    if limitations:
        context_parts.append(" | ".join(limitations))

    # Availability
    if profile.available_days_per_week:
        context_parts.append(f"Can train {profile.available_days_per_week} days/week")
    if profile.preferred_session_duration:
        context_parts.append(f"Prefers {profile.preferred_session_duration}-minute sessions")

    # Equipment
    if profile.training_location:
        context_parts.append(f"Trains at: {profile.training_location}")
    if profile.has_gym_membership is not None:
        gym_status = "has gym access" if profile.has_gym_membership else "no gym access"
        context_parts.append(gym_status)
    if profile.available_equipment:
        equipment = profile.get_available_equipment()
        if equipment:
            context_parts.append(f"Available equipment: {', '.join(equipment)}")

    # Join all context
    if context_parts:
        return "USER PROFILE:\n" + "\n".join(f"- {part}" for part in context_parts)
    else:
        return "USER PROFILE: No profile information available yet."
