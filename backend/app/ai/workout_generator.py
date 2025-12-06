"""
Workout Plan Generator using AI.

Generates personalized workout plans based on user profile and RAG context.
"""

import json
import logging
from typing import Dict, Any, Optional

from app.ai.gemini import get_gemini_client, GeminiGenerationError
from app.ai.rag import query_knowledge, format_context_for_llm
from app.models.user_profile import MVPUserProfile

logger = logging.getLogger(__name__)


def generate_workout_plan(
    profile: MVPUserProfile,
    duration_weeks: int = 1,
    custom_notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate a personalized workout plan using AI.

    Args:
        profile: User profile with fitness information
        duration_weeks: Duration of the plan in weeks (1-2)
        custom_notes: Additional user requirements

    Returns:
        Dictionary with plan structure:
        {
            "title": str,
            "description": str,
            "plan_structure": {
                "week_1": [...],
                "week_2": [...]
            }
        }

    Raises:
        GeminiGenerationError: If plan generation fails
    """
    try:
        logger.info(f"Generating {duration_weeks}-week workout plan for user profile {profile.id}")

        # Step 1: Build user context
        user_context = _build_user_context(profile)

        # Step 2: Query RAG for relevant workout knowledge
        sport = profile.primary_sport or "general fitness"
        rag_context = _get_workout_knowledge(sport, profile.fitness_goals or [])

        # Step 3: Build generation prompt
        prompt = _build_workout_plan_prompt(
            user_context=user_context,
            rag_context=rag_context,
            duration_weeks=duration_weeks,
            sport=sport,
            custom_notes=custom_notes
        )

        logger.info(f"Generating plan with prompt length: {len(prompt)} characters")

        # Step 4: Generate plan with Gemini
        # Use maximum token limit for plan generation
        from google.generativeai.types import GenerationConfig

        generation_config = GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            top_k=40,
            max_output_tokens=8192,  # Maximum for Gemini 2.5 Flash
        )

        model = get_gemini_client()
        response = model.generate_content(prompt, generation_config=generation_config)

        # Check if response has candidates and text
        if not response.candidates:
            raise GeminiGenerationError("No response candidates returned from Gemini")

        candidate = response.candidates[0]

        # Check finish_reason
        if candidate.finish_reason != 1:  # 1 = STOP (normal completion)
            finish_reason_map = {
                2: "MAX_TOKENS",
                3: "SAFETY",
                4: "RECITATION",
                5: "OTHER"
            }
            reason = finish_reason_map.get(candidate.finish_reason, "UNKNOWN")
            raise GeminiGenerationError(f"Generation stopped due to: {reason}. Try with a shorter prompt or different content.")

        if not response.text:
            raise GeminiGenerationError("Empty response from Gemini")

        # Step 5: Parse JSON response
        plan_data = _parse_plan_response(response.text)

        logger.info(f"Workout plan generated successfully: {plan_data['title']}")

        return plan_data

    except Exception as e:
        logger.error(f"Error generating workout plan: {e}", exc_info=True)
        raise GeminiGenerationError(f"Failed to generate workout plan: {str(e)}")


def _build_user_context(profile: MVPUserProfile) -> str:
    """Build user context string from profile."""
    context_parts = []

    # Basic info
    if profile.age:
        context_parts.append(f"Age: {profile.age}")
    if profile.gender:
        context_parts.append(f"Gender: {profile.gender}")

    # Experience and goals
    if profile.experience_level:
        context_parts.append(f"Experience level: {profile.experience_level}")
    if profile.primary_sport:
        context_parts.append(f"Primary sport: {profile.primary_sport}")
    if profile.fitness_goals:
        goals = profile.get_fitness_goals()
        if goals:
            context_parts.append(f"Goals: {', '.join(goals)}")

    # Limitations
    if profile.injuries:
        injuries = profile.get_injuries()
        if injuries:
            context_parts.append(f"⚠️ Injuries to work around: {', '.join(injuries)}")
    if profile.health_conditions:
        conditions = profile.get_health_conditions()
        if conditions:
            context_parts.append(f"⚠️ Health conditions: {', '.join(conditions)}")

    # Training schedule
    if profile.available_days_per_week:
        context_parts.append(f"Available: {profile.available_days_per_week} days/week")
    if profile.preferred_session_duration:
        context_parts.append(f"Session duration: {profile.preferred_session_duration} minutes")

    # Equipment
    if profile.training_location:
        context_parts.append(f"Location: {profile.training_location}")
    if profile.available_equipment:
        equipment = profile.get_available_equipment()
        if equipment:
            context_parts.append(f"Equipment: {', '.join(equipment)}")
    elif profile.has_gym_membership:
        context_parts.append("Has gym access")

    return "\n".join(context_parts)


def _get_workout_knowledge(sport: str, goals: list) -> str:
    """Query RAG system for workout-related knowledge."""
    # Query for sport-specific exercises
    queries = [
        f"{sport} exercises",
        f"{sport} training program",
        "workout programming principles"
    ]

    # Add goal-specific queries
    for goal in goals[:2]:  # Limit to top 2 goals
        queries.append(f"{goal} training")

    all_results = []
    for query in queries[:2]:  # Limit total queries to 2
        try:
            results = query_knowledge(query=query, sport=sport, top_k=1)  # Only 1 result per query
            all_results.extend(results)
        except Exception as e:
            logger.warning(f"RAG query failed for '{query}': {e}")

    if not all_results:
        return "Use general fitness principles and progressive overload."

    return format_context_for_llm(all_results[:3])  # Top 3 results total


def _build_workout_plan_prompt(
    user_context: str,
    rag_context: str,
    duration_weeks: int,
    sport: str,
    custom_notes: Optional[str]
) -> str:
    """Build the prompt for workout plan generation."""
    custom_section = f"\n\nADDITIONAL REQUIREMENTS:\n{custom_notes}" if custom_notes else ""

    # Build week structure example based on duration
    weeks_structure = []
    for week_num in range(1, min(duration_weeks + 1, 4)):  # Show first 3 weeks as example
        weeks_structure.append(f'    "week_{week_num}": [...]')
    weeks_example = ',\n'.join(weeks_structure)

    prompt = f"""Create a {duration_weeks}-week {sport} training plan. JSON only, be concise.

User: {user_context[:400]}
{custom_section}

IMPORTANT:
- Generate EXACTLY {duration_weeks} weeks (week_1 through week_{duration_weeks})
- Include REST DAYS explicitly in each week
- For rest days use: {{"day": "Rest", "focus": "Recovery", "exercises": [], "duration_min": 0}}

Format:
{{
  "title": "Short title",
  "description": "1 sentence",
  "plan_structure": {{
{weeks_example}
  }}
}}

Week structure: Array of daily workouts
Day format: {{"day": "Day name", "focus": "Focus area", "exercises": [{{"name": "Exercise", "sets": 3, "reps": "10-12", "rest_seconds": 60, "notes": "Optional tip"}}], "duration_min": 45}}

Guidelines:
- Use {sport}-specific exercises, bodyweight if no equipment
- 3-5 exercises per training day
- Include 1-2 rest days per week based on user's available days
- Progress difficulty across weeks
- Keep exercise notes brief
- Include warmup/cooldown in duration

JSON only, no markdown blocks."""

    return prompt


def _parse_plan_response(response_text: str) -> Dict[str, Any]:
    """Parse and validate the AI response."""
    # Try to extract JSON from response
    response_text = response_text.strip()

    # Remove markdown code blocks if present
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    try:
        plan_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        logger.error(f"Response text: {response_text[:500]}")
        raise GeminiGenerationError(f"Invalid JSON response from AI: {str(e)}")

    # Validate required fields
    if "title" not in plan_data:
        raise GeminiGenerationError("Missing 'title' in generated plan")
    if "plan_structure" not in plan_data:
        raise GeminiGenerationError("Missing 'plan_structure' in generated plan")

    # Ensure description exists
    if "description" not in plan_data:
        plan_data["description"] = plan_data["title"]

    return plan_data
