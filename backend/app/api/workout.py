"""
Workout Plan API endpoints.

All endpoints work with the single MVP user (id=1).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.database.connection import get_db
from app.crud import profile as crud_profile
from app.crud import workout as crud_workout
from app.schemas.workout import (
    WorkoutPlanRequest,
    WorkoutPlanResponse,
    WorkoutPlanListResponse,
    WorkoutPlanSummary
)
from app.schemas.profile import MessageResponse

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/workouts",
    tags=["workouts"],
    responses={404: {"description": "Not found"}}
)


@router.post("/generate", response_model=WorkoutPlanResponse, status_code=status.HTTP_201_CREATED)
def generate_workout_plan(
    request: WorkoutPlanRequest,
    db: Session = Depends(get_db)
) -> WorkoutPlanResponse:
    """
    Generate a new personalized workout plan.

    Requires user to have completed onboarding.
    Deactivates any existing active plans.

    Args:
        request: WorkoutPlanRequest with duration and notes
        db: Database session (injected)

    Returns:
        WorkoutPlanResponse with generated plan

    Raises:
        400: If user profile not found or onboarding not completed
        500: If generation fails
    """
    try:
        # Get user profile
        profile = crud_profile.get_profile(db)

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User profile not found. Complete onboarding first."
            )

        if not profile.onboarding_completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Onboarding not completed. Complete your profile first."
            )

        logger.info(f"Generating {request.duration_weeks}-week workout plan")

        # Generate and save plan
        plan = crud_workout.create_workout_plan(
            db=db,
            profile=profile,
            duration_weeks=request.duration_weeks,
            custom_notes=request.custom_notes
        )

        logger.info(f"Workout plan generated: {plan.title} (ID: {plan.id})")

        return WorkoutPlanResponse.model_validate(plan)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating workout plan: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate workout plan: {str(e)}"
        )


@router.get("", response_model=WorkoutPlanListResponse)
def get_workout_plans(
    include_completed: bool = False,
    db: Session = Depends(get_db)
) -> WorkoutPlanListResponse:
    """
    Get all workout plans.

    Args:
        include_completed: Include completed plans (default: False)
        db: Database session (injected)

    Returns:
        WorkoutPlanListResponse with list of plans
    """
    plans = crud_workout.get_all_plans(
        db=db,
        include_completed=include_completed
    )

    active_plan = crud_workout.get_active_plan(db)

    summaries = [
        WorkoutPlanSummary.model_validate(plan) for plan in plans
    ]

    return WorkoutPlanListResponse(
        plans=summaries,
        total=len(summaries),
        active_plan_id=active_plan.id if active_plan else None
    )


@router.get("/active", response_model=WorkoutPlanResponse)
def get_active_workout_plan(
    db: Session = Depends(get_db)
) -> WorkoutPlanResponse:
    """
    Get the currently active workout plan.

    Returns:
        WorkoutPlanResponse with active plan

    Raises:
        404: If no active plan found
    """
    plan = crud_workout.get_active_plan(db)

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active workout plan. Generate one first."
        )

    return WorkoutPlanResponse.model_validate(plan)


@router.get("/{plan_id}", response_model=WorkoutPlanResponse)
def get_workout_plan(
    plan_id: int,
    db: Session = Depends(get_db)
) -> WorkoutPlanResponse:
    """
    Get a specific workout plan by ID.

    Args:
        plan_id: Plan ID
        db: Database session (injected)

    Returns:
        WorkoutPlanResponse with plan details

    Raises:
        404: If plan not found
    """
    plan = crud_workout.get_plan_by_id(db, plan_id)

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout plan {plan_id} not found"
        )

    return WorkoutPlanResponse.model_validate(plan)


@router.post("/{plan_id}/activate", response_model=WorkoutPlanResponse)
def activate_workout_plan(
    plan_id: int,
    db: Session = Depends(get_db)
) -> WorkoutPlanResponse:
    """
    Set a plan as the active plan.

    Deactivates all other plans.

    Args:
        plan_id: Plan ID to activate
        db: Database session (injected)

    Returns:
        WorkoutPlanResponse with activated plan

    Raises:
        404: If plan not found
    """
    plan = crud_workout.set_active_plan(db, plan_id)

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout plan {plan_id} not found"
        )

    logger.info(f"Activated workout plan: {plan.title} (ID: {plan.id})")

    return WorkoutPlanResponse.model_validate(plan)


@router.post("/{plan_id}/complete", response_model=WorkoutPlanResponse)
def complete_workout_plan(
    plan_id: int,
    db: Session = Depends(get_db)
) -> WorkoutPlanResponse:
    """
    Mark a workout plan as completed.

    Args:
        plan_id: Plan ID to complete
        db: Database session (injected)

    Returns:
        WorkoutPlanResponse with completed plan

    Raises:
        404: If plan not found
    """
    plan = crud_workout.mark_plan_completed(db, plan_id)

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout plan {plan_id} not found"
        )

    logger.info(f"Completed workout plan: {plan.title} (ID: {plan.id})")

    return WorkoutPlanResponse.model_validate(plan)


@router.delete("/{plan_id}", response_model=MessageResponse)
def delete_workout_plan(
    plan_id: int,
    db: Session = Depends(get_db)
) -> MessageResponse:
    """
    Delete a workout plan.

    Args:
        plan_id: Plan ID to delete
        db: Database session (injected)

    Returns:
        MessageResponse confirming deletion

    Raises:
        404: If plan not found
    """
    deleted = crud_workout.delete_plan(db, plan_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout plan {plan_id} not found"
        )

    logger.info(f"Deleted workout plan ID: {plan_id}")

    return MessageResponse(
        message=f"Workout plan {plan_id} deleted successfully",
        success=True
    )
