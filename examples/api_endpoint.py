"""
Example: FastAPI Endpoint Pattern for CoachX

This file demonstrates the standard pattern for creating API endpoints
in the CoachX project. All new endpoints should follow this structure.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session
from typing import Optional
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Create router with prefix and tags
router = APIRouter(prefix="/api/training", tags=["training"])

# Request/Response models with Pydantic
class WorkoutRequest(BaseModel):
    """Request model for workout generation."""
    
    user_id: int = Field(..., gt=0, description="User ID")
    sport: str = Field(..., description="Sport type")
    experience_level: str = Field(..., description="Experience level")
    days_per_week: int = Field(..., ge=1, le=7, description="Training days per week")
    goals: Optional[str] = Field(None, max_length=200, description="User goals")
    
    @validator('sport')
    def validate_sport(cls, v: str) -> str:
        """Validate sport is one of the allowed types."""
        allowed = ['boxing', 'crossfit', 'gym', 'calisthenics', 'running']
        if v.lower() not in allowed:
            raise ValueError(f'Sport must be one of: {", ".join(allowed)}')
        return v.lower()
    
    @validator('experience_level')
    def validate_experience(cls, v: str) -> str:
        """Validate experience level is valid."""
        allowed = ['beginner', 'intermediate', 'advanced']
        if v.lower() not in allowed:
            raise ValueError(f'Experience must be one of: {", ".join(allowed)}')
        return v.lower()
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "sport": "boxing",
                "experience_level": "intermediate",
                "days_per_week": 4,
                "goals": "Improve technique and conditioning"
            }
        }


class WorkoutResponse(BaseModel):
    """Response model for workout generation."""
    
    success: bool
    plan_id: Optional[int] = None
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "plan_id": 123,
                "message": "Workout plan generated successfully"
            }
        }


# Database dependency (simplified for example)
def get_db():
    """Dependency to get database session."""
    # In real implementation, this would yield a session
    pass


@router.post("/generate", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
async def generate_workout_plan(
    request: WorkoutRequest,
    db: Session = Depends(get_db)
) -> WorkoutResponse:
    """
    Generate a personalized workout plan for a user.
    
    This endpoint creates a customized training plan based on the user's
    sport, experience level, and goals using AI generation.
    
    Args:
        request: Workout generation parameters
        db: Database session dependency
    
    Returns:
        WorkoutResponse with success status and plan ID
    
    Raises:
        HTTPException: 400 if validation fails
        HTTPException: 404 if user not found
        HTTPException: 500 if generation fails
    
    Example:
        POST /api/training/generate
        {
            "user_id": 1,
            "sport": "boxing",
            "experience_level": "intermediate",
            "days_per_week": 4,
            "goals": "Improve technique"
        }
    """
    try:
        # Log the request
        logger.info(
            f"Generating workout plan for user {request.user_id}",
            extra={
                "user_id": request.user_id,
                "sport": request.sport,
                "experience_level": request.experience_level
            }
        )
        
        # Validate user exists (example)
        # user = db.query(User).filter(User.id == request.user_id).first()
        # if not user:
        #     logger.warning(f"User not found: {request.user_id}")
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"User with ID {request.user_id} not found"
        #     )
        
        # Business logic here
        # This would call your AI service to generate the plan
        # plan = await training_service.generate_plan(request, db)
        
        # Example successful response
        plan_id = 123  # This would be the real plan ID
        
        logger.info(
            f"Successfully generated plan {plan_id} for user {request.user_id}"
        )
        
        return WorkoutResponse(
            success=True,
            plan_id=plan_id,
            message="Workout plan generated successfully"
        )
        
    except ValueError as e:
        # Validation errors
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Unexpected errors
        logger.error(
            f"Error generating workout plan: {str(e)}",
            exc_info=True,
            extra={"user_id": request.user_id}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate workout plan. Please try again later."
        )


@router.get("/{plan_id}", response_model=dict)
async def get_workout_plan(
    plan_id: int,
    db: Session = Depends(get_db)
) -> dict:
    """
    Retrieve a workout plan by ID.
    
    Args:
        plan_id: ID of the workout plan
        db: Database session dependency
    
    Returns:
        Workout plan details
    
    Raises:
        HTTPException: 404 if plan not found
    
    Example:
        GET /api/training/123
    """
    try:
        logger.info(f"Retrieving workout plan {plan_id}")
        
        # Retrieve from database
        # plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == plan_id).first()
        # if not plan:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"Workout plan {plan_id} not found"
        #     )
        
        # Example response
        return {
            "id": plan_id,
            "user_id": 1,
            "plan_data": {
                "weeks": 4,
                "days_per_week": 4,
                "exercises": []
            },
            "created_at": "2024-12-02T10:00:00Z"
        }
        
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error retrieving plan {plan_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve workout plan"
        )


# Key Patterns to Follow:
# 
# 1. Router Setup:
#    - Use prefix for API versioning (/api/v1/...)
#    - Add descriptive tags for OpenAPI docs
#
# 2. Request/Response Models:
#    - Use Pydantic BaseModel for validation
#    - Add Field() with description and constraints
#    - Include validators for custom validation
#    - Add Config with examples for docs
#
# 3. Endpoint Function:
#    - Use async def for better performance
#    - Add type hints for all parameters
#    - Include comprehensive docstring
#    - Use Depends() for database sessions
#
# 4. Error Handling:
#    - Try/except for all operations
#    - Log errors with context
#    - Raise appropriate HTTPException
#    - Return user-friendly error messages
#
# 5. Logging:
#    - Log entry point (info level)
#    - Log errors (error level)
#    - Include context (user_id, etc.)
#    - Use structured logging
#
# 6. Response:
#    - Use proper HTTP status codes
#    - Return consistent response format
#    - Include success flag
#    - Add helpful messages
