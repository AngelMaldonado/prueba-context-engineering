"""
CRUD operations for MVP workout plans.

All operations work with the single MVP user (id=1).
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from datetime import datetime

from app.models.workout_plan import MVPWorkoutPlan
from app.models.user_profile import MVPUserProfile
from app.ai.workout_generator import generate_workout_plan


def get_active_plan(db: Session) -> Optional[MVPWorkoutPlan]:
    """
    Get the currently active workout plan.

    Args:
        db: Database session

    Returns:
        Active MVPWorkoutPlan or None
    """
    return db.query(MVPWorkoutPlan).filter(
        MVPWorkoutPlan.user_id == 1,
        MVPWorkoutPlan.is_active == True
    ).first()


def get_plan_by_id(db: Session, plan_id: int) -> Optional[MVPWorkoutPlan]:
    """
    Get a workout plan by ID.

    Args:
        db: Database session
        plan_id: Plan ID

    Returns:
        MVPWorkoutPlan or None
    """
    return db.query(MVPWorkoutPlan).filter(
        MVPWorkoutPlan.id == plan_id,
        MVPWorkoutPlan.user_id == 1
    ).first()


def get_all_plans(
    db: Session,
    include_completed: bool = False,
    limit: int = 10
) -> List[MVPWorkoutPlan]:
    """
    Get all workout plans for the user.

    Args:
        db: Database session
        include_completed: Include completed plans
        limit: Maximum number of plans to return

    Returns:
        List of MVPWorkoutPlan
    """
    query = db.query(MVPWorkoutPlan).filter(MVPWorkoutPlan.user_id == 1)

    if not include_completed:
        query = query.filter(MVPWorkoutPlan.completed == False)

    return query.order_by(desc(MVPWorkoutPlan.created_at)).limit(limit).all()


def create_workout_plan(
    db: Session,
    profile: MVPUserProfile,
    duration_weeks: int = 4,
    custom_notes: Optional[str] = None
) -> MVPWorkoutPlan:
    """
    Generate and save a new workout plan.

    Deactivates any existing active plans.

    Args:
        db: Database session
        profile: User profile for personalization
        duration_weeks: Plan duration in weeks
        custom_notes: Additional user requirements

    Returns:
        Created MVPWorkoutPlan
    """
    # Generate plan using AI
    plan_data = generate_workout_plan(
        profile=profile,
        duration_weeks=duration_weeks,
        custom_notes=custom_notes
    )

    # Deactivate existing active plans
    db.query(MVPWorkoutPlan).filter(
        MVPWorkoutPlan.user_id == 1,
        MVPWorkoutPlan.is_active == True
    ).update({"is_active": False})

    # Create new plan
    new_plan = MVPWorkoutPlan(
        user_id=1,
        title=plan_data["title"],
        description=plan_data.get("description"),
        duration_weeks=duration_weeks,
        plan_structure=plan_data["plan_structure"],
        sport_focus=profile.primary_sport,
        is_active=True,
        completed=False
    )

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return new_plan


def mark_plan_completed(db: Session, plan_id: int) -> Optional[MVPWorkoutPlan]:
    """
    Mark a workout plan as completed.

    Args:
        db: Database session
        plan_id: Plan ID

    Returns:
        Updated MVPWorkoutPlan or None
    """
    plan = get_plan_by_id(db, plan_id)

    if not plan:
        return None

    plan.completed = True
    plan.completed_at = datetime.utcnow()
    plan.is_active = False

    db.commit()
    db.refresh(plan)

    return plan


def set_active_plan(db: Session, plan_id: int) -> Optional[MVPWorkoutPlan]:
    """
    Set a plan as the active plan.

    Deactivates all other plans.

    Args:
        db: Database session
        plan_id: Plan ID to activate

    Returns:
        Activated MVPWorkoutPlan or None
    """
    plan = get_plan_by_id(db, plan_id)

    if not plan:
        return None

    # Deactivate all plans
    db.query(MVPWorkoutPlan).filter(
        MVPWorkoutPlan.user_id == 1
    ).update({"is_active": False})

    # Activate selected plan
    plan.is_active = True

    db.commit()
    db.refresh(plan)

    return plan


def delete_plan(db: Session, plan_id: int) -> bool:
    """
    Delete a workout plan.

    Args:
        db: Database session
        plan_id: Plan ID

    Returns:
        True if deleted, False if not found
    """
    plan = get_plan_by_id(db, plan_id)

    if not plan:
        return False

    db.delete(plan)
    db.commit()

    return True
