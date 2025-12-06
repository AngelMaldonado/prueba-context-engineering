"""
Profile API endpoints for user onboarding and profile management.

All endpoints work with the single MVP user (id=1).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.database.connection import get_db
from app.models.user import MVPUser
from app.models.user_profile import MVPUserProfile
from app.crud import profile as crud_profile
from app.schemas.profile import (
    OnboardingRequest,
    ProfileUpdateRequest,
    GoalsUpdateRequest,
    ProfileResponse,
    ProfileStatusResponse,
    MessageResponse
)

# Setup logging
logger = logging.getLogger(__name__)

# Create router with prefix
router = APIRouter(
    prefix="/api/profile",
    tags=["profile"],
    responses={404: {"description": "Not found"}}
)


def build_profile_response(user: MVPUser, profile: MVPUserProfile) -> ProfileResponse:
    """
    Build ProfileResponse from user and profile models.

    Converts JSON fields to Python lists for response.

    Args:
        user: MVPUser instance
        profile: MVPUserProfile instance

    Returns:
        ProfileResponse with all data
    """
    return ProfileResponse(
        user_id=user.id,
        full_name=user.full_name,
        profile_id=profile.id,
        age=profile.age,
        gender=profile.gender,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        experience_level=profile.experience_level,
        primary_sport=profile.primary_sport,
        secondary_sports=profile.get_secondary_sports(),
        years_training=profile.years_training,
        fitness_goals=profile.get_fitness_goals(),
        injuries=profile.get_injuries(),
        health_conditions=profile.get_health_conditions(),
        medications=profile.get_medications(),
        available_days_per_week=profile.available_days_per_week,
        preferred_session_duration=profile.preferred_session_duration,
        preferred_training_times=profile.get_preferred_training_times(),
        has_gym_membership=profile.has_gym_membership,
        available_equipment=profile.get_available_equipment(),
        training_location=profile.training_location,
        onboarding_completed=profile.onboarding_completed,
        onboarding_completed_at=profile.onboarding_completed_at,
        profile_completion_percentage=profile.profile_completion_percentage,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )


@router.get("/status", response_model=ProfileStatusResponse)
def get_profile_status(db: Session = Depends(get_db)) -> ProfileStatusResponse:
    """
    Check profile status.

    Returns whether profile exists and onboarding completion status.

    Returns:
        ProfileStatusResponse with status info
    """
    profile = crud_profile.get_profile(db)

    if not profile:
        return ProfileStatusResponse(
            exists=False,
            onboarding_completed=False,
            profile_completion_percentage=0
        )

    return ProfileStatusResponse(
        exists=True,
        onboarding_completed=profile.onboarding_completed,
        profile_completion_percentage=profile.profile_completion_percentage
    )


@router.get("", response_model=ProfileResponse)
def get_profile(db: Session = Depends(get_db)) -> ProfileResponse:
    """
    Get user profile.

    Returns complete profile data. Creates empty profile if doesn't exist.

    Returns:
        ProfileResponse with all profile data
    """
    user = crud_profile.get_or_create_mvp_user(db)
    profile = crud_profile.get_or_create_profile(db)

    logger.info(f"Profile retrieved: completion={profile.profile_completion_percentage}%")

    return build_profile_response(user, profile)


@router.post("/onboarding", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def submit_onboarding(
    onboarding_data: OnboardingRequest,
    db: Session = Depends(get_db)
) -> ProfileResponse:
    """
    Submit onboarding data.

    Creates or updates profile with onboarding data. Only updates provided fields.
    Marks onboarding as completed if this is the first submission.

    Args:
        onboarding_data: OnboardingRequest with user data

    Returns:
        ProfileResponse with updated profile data
    """
    try:
        # Get existing profile to check if onboarding was already completed
        existing_profile = crud_profile.get_profile(db)
        mark_completed = existing_profile is None or not existing_profile.onboarding_completed

        # Update profile
        profile = crud_profile.update_profile_from_onboarding(
            db=db,
            onboarding_data=onboarding_data,
            mark_completed=mark_completed
        )

        user = crud_profile.get_or_create_mvp_user(db)

        logger.info(
            f"Onboarding data submitted: "
            f"completed={profile.onboarding_completed}, "
            f"completion={profile.profile_completion_percentage}%"
        )

        return build_profile_response(user, profile)

    except Exception as e:
        logger.error(f"Error submitting onboarding data: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save onboarding data: {str(e)}"
        )


@router.put("", response_model=ProfileResponse)
def update_profile(
    update_data: ProfileUpdateRequest,
    db: Session = Depends(get_db)
) -> ProfileResponse:
    """
    Update user profile.

    Allows partial updates - only updates provided fields.

    Args:
        update_data: ProfileUpdateRequest with fields to update

    Returns:
        ProfileResponse with updated profile data
    """
    try:
        profile = crud_profile.update_profile(db=db, update_data=update_data)
        user = crud_profile.get_or_create_mvp_user(db)

        logger.info(f"Profile updated: completion={profile.profile_completion_percentage}%")

        return build_profile_response(user, profile)

    except Exception as e:
        logger.error(f"Error updating profile: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        )


@router.patch("/goals", response_model=ProfileResponse)
def update_fitness_goals(
    goals_data: GoalsUpdateRequest,
    db: Session = Depends(get_db)
) -> ProfileResponse:
    """
    Update fitness goals only.

    Args:
        goals_data: GoalsUpdateRequest with new goals

    Returns:
        ProfileResponse with updated profile data
    """
    try:
        profile = crud_profile.update_fitness_goals(
            db=db,
            goals=goals_data.fitness_goals
        )
        user = crud_profile.get_or_create_mvp_user(db)

        logger.info(f"Fitness goals updated: {goals_data.fitness_goals}")

        return build_profile_response(user, profile)

    except Exception as e:
        logger.error(f"Error updating fitness goals: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update fitness goals: {str(e)}"
        )


@router.delete("", response_model=MessageResponse)
def delete_profile(db: Session = Depends(get_db)) -> MessageResponse:
    """
    Delete (reset) user profile.

    Deletes all profile data and creates a new empty profile.

    Returns:
        MessageResponse confirming deletion
    """
    try:
        crud_profile.delete_profile(db)

        logger.info("Profile deleted and reset")

        return MessageResponse(
            message="Profile deleted and reset successfully",
            success=True
        )

    except Exception as e:
        logger.error(f"Error deleting profile: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete profile: {str(e)}"
        )
