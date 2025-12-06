"""
Gemini AI integration for CoachX.

Uses Google Gemini API to generate AI-powered training responses,
combining RAG context with LLM capabilities.
"""

from typing import Optional, Dict, Any
import logging

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from app.config import settings
from app.ai.rag import query_knowledge, format_context_for_llm

logger = logging.getLogger(__name__)

# Global client instance (singleton pattern)
_gemini_model = None


class GeminiError(Exception):
    """Base exception for Gemini-related errors."""
    pass


class GeminiAuthenticationError(GeminiError):
    """Raised when API key is invalid or missing."""
    pass


class GeminiGenerationError(GeminiError):
    """Raised when text generation fails."""
    pass


def get_gemini_client():
    """
    Get or create Gemini model client (singleton pattern).

    Initializes the Gemini API with API key from settings and returns
    a configured GenerativeModel instance.

    Returns:
        GenerativeModel instance configured for text generation

    Raises:
        GeminiAuthenticationError: If API key is missing or invalid

    Example:
        >>> model = get_gemini_client()
        >>> response = model.generate_content("Hello")
    """
    global _gemini_model

    if _gemini_model is None:
        # Validate API key
        if not settings.GEMINI_API_KEY:
            raise GeminiAuthenticationError(
                "GEMINI_API_KEY not found in environment. "
                "Please add it to your .env file."
            )

        try:
            logger.info(f"Initializing Gemini client with model: {settings.GEMINI_MODEL}")

            # Configure Gemini API
            genai.configure(api_key=settings.GEMINI_API_KEY)

            # Create model with safety settings
            _gemini_model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                },
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )

            logger.info("Gemini client initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise GeminiAuthenticationError(f"Gemini initialization failed: {str(e)}")

    return _gemini_model


def generate_response(prompt: str, **kwargs) -> str:
    """
    Generate AI response using Gemini API.

    Basic generation without RAG context. For RAG-enhanced responses,
    use generate_with_rag() instead.

    Args:
        prompt: The prompt text to send to Gemini
        **kwargs: Additional generation parameters (temperature, max_tokens, etc.)

    Returns:
        Generated text response

    Raises:
        GeminiGenerationError: If generation fails
        GeminiAuthenticationError: If API key is invalid

    Example:
        >>> response = generate_response("What is a jab in boxing?")
        >>> print(response)
    """
    try:
        model = get_gemini_client()

        logger.info(f"Generating response for prompt: {prompt[:50]}...")

        # Generate content
        response = model.generate_content(prompt)

        # Extract text from response
        if not response.text:
            raise GeminiGenerationError("Empty response from Gemini API")

        logger.info(f"Response generated: {len(response.text)} characters")
        return response.text

    except GeminiAuthenticationError:
        raise
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise GeminiGenerationError(f"Failed to generate response: {str(e)}")


def _clean_markdown(text: str) -> str:
    """
    Remove common markdown formatting for cleaner display.

    Args:
        text: Text with potential markdown formatting

    Returns:
        Text with markdown formatting removed
    """
    import re

    # Remove bold (**text** or __text__)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)

    # Remove italic (*text* or _text_)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)

    # Remove headers (### text)
    text = re.sub(r'^#{1,6}\s+(.+)$', r'\1', text, flags=re.MULTILINE)

    # Remove code blocks (```code```)
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`(.+?)`', r'\1', text)

    return text


def generate_with_rag(
    query: str,
    sport: Optional[str] = None,
    top_k: int = 3,
    user_context: Optional[str] = None,
    conversation_history: Optional[list] = None
) -> str:
    """
    Generate AI response enhanced with RAG context and user personalization.

    Queries the RAG system for relevant context, formats it into a prompt,
    and generates a response using Gemini that combines the context with
    LLM reasoning, user profile information, and conversation history.

    Args:
        query: User's question or request
        sport: Optional sport filter (boxing, crossfit, gym, etc.)
        top_k: Number of RAG context chunks to retrieve (default: 3)
        user_context: Optional user profile context for personalization
        conversation_history: Optional list of previous messages
            [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

    Returns:
        AI-generated response incorporating RAG context and user profile

    Raises:
        GeminiGenerationError: If generation fails

    Example:
        >>> response = generate_with_rag(
        ...     query="How do I improve my jab?",
        ...     sport="boxing",
        ...     top_k=3,
        ...     user_context="Age: 28, Experience: intermediate...",
        ...     conversation_history=[...]
        ... )
        >>> print(response)
    """
    try:
        logger.info(f"RAG-enhanced generation for query: {query[:50]}... (sport={sport})")

        # Step 1: Query RAG system for context (reduced to 2 for chat)
        rag_results = query_knowledge(query=query, sport=sport, top_k=2)
        context = format_context_for_llm(rag_results)

        # Truncate context if too long (max 800 chars to save tokens)
        if len(context) > 800:
            context = context[:800] + "..."

        logger.info(f"Retrieved {len(rag_results)} context chunks from RAG ({len(context)} chars)")

        # Step 2: Build prompt with context
        sport_context = f" specializing in {sport}" if sport else ""

        # Step 3: Add user personalization context if available
        user_section = ""
        if user_context:
            user_section = f"\n\n{user_context}\n\nIMPORTANT: Use the user profile information above to personalize your response. Consider their experience level, goals, limitations, and available resources when giving advice."

        # Step 4: Format conversation history
        history_section = ""
        if conversation_history and len(conversation_history) > 0:
            # Only include last 3 exchanges (6 messages) to keep context manageable
            recent_history = conversation_history[-6:]
            history_lines = []
            for msg in recent_history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                # Limit each message to 200 chars to save tokens
                if len(content) > 200:
                    content = content[:200] + "..."
                prefix = "Usuario:" if role == "user" else "CoachX:"
                history_lines.append(f"{prefix} {content}")

            history_section = "\n\nCONVERSATION HISTORY:\n" + "\n".join(history_lines) + "\n\nIMPORTANT: Continue this conversation naturally. Reference previous exchanges when relevant."

        prompt = f"""You are CoachX, an expert personal training assistant{sport_context}.
{user_section}

CRITICAL RULES:
1. You ONLY answer questions related to fitness, training, sports, exercise, nutrition, and athletic performance.
2. If the user asks about their profile, identity, or "who am I", provide a summary of their fitness profile using the user context above. This is a valid fitness-related question.
3. NEVER generate complete workout plans or training routines. If asked for a plan, respond:
   "Para generar un plan de entrenamiento personalizado completo, usa el botón 'Generate Workout Plan' en el dashboard. Yo estoy aquí para responder preguntas específicas sobre técnica, nutrición, ejercicios individuales y consejos de entrenamiento."
4. You CAN give advice on:
   - User's fitness profile and background
   - Specific exercise techniques (how to do a proper squat, jab technique, etc.)
   - Nutrition tips and meal suggestions
   - Recovery and injury prevention
   - Training concepts and principles
   - Exercise modifications
5. If the user asks about topics unrelated to fitness (cooking, politics, general knowledge, etc.), respond:
   "Lo siento, solo puedo ayudarte con temas relacionados con entrenamiento, ejercicio y fitness. ¿Tienes alguna pregunta sobre tu entrenamiento?"
6. If the user uses inappropriate language or insults, respond professionally:
   "Estoy aquí para ayudarte con tu entrenamiento. ¿En qué puedo asistirte?"
7. IMPORTANT: Format your response in plain text. Do NOT use markdown formatting like **, *, ###, or bullet points with *. Use simple numbered lists (1., 2.) or line breaks for structure.

You have access to official training knowledge from professional sources.

CONTEXT FROM KNOWLEDGE BASE:
{context}
{history_section}

USER QUESTION:
{query}

First, determine if this question is related to fitness, training, sports, exercise, or nutrition.
- If YES: Provide accurate, helpful, and motivating training advice based on the context above.
  Always prioritize safety and proper technique. Keep your response clear, concise, and actionable.
- If NO: Respond with the appropriate message from the rules above.

REMEMBER: You are a fitness assistant ONLY. Do not answer questions outside your domain."""

        # Step 3: Generate response with custom config for longer responses
        from google.generativeai.types import GenerationConfig

        model = get_gemini_client()
        generation_config = GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            top_k=40,
            max_output_tokens=4096,  # Increased for detailed training responses
        )

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
            logger.error(f"Generation stopped: {reason}")
            # Return a helpful message instead of crashing
            if candidate.finish_reason == 2:  # MAX_TOKENS
                return "Lo siento, mi respuesta fue demasiado larga. ¿Podrías hacer una pregunta más específica?"
            else:
                raise GeminiGenerationError(f"Generation stopped: {reason}")

        if not response.text:
            raise GeminiGenerationError("Empty response from Gemini")

        # Clean up markdown formatting for better display
        cleaned_response = _clean_markdown(response.text)

        logger.info("RAG-enhanced response generated successfully")
        return cleaned_response

    except Exception as e:
        logger.error(f"Error in RAG-enhanced generation: {e}")
        raise GeminiGenerationError(f"Failed to generate RAG response: {str(e)}")


def test_gemini_connection() -> Dict[str, Any]:
    """
    Test Gemini API connection and basic generation.

    Returns:
        Dictionary with test results

    Example:
        >>> result = test_gemini_connection()
        >>> print(result['status'])
    """
    try:
        model = get_gemini_client()

        # Simple test prompt
        test_response = generate_response("Say 'CoachX is ready!' in one sentence.")

        return {
            "status": "success",
            "model": settings.GEMINI_MODEL,
            "test_response": test_response,
            "message": "Gemini API connection successful"
        }
    except GeminiAuthenticationError as e:
        return {
            "status": "error",
            "error": "authentication_failed",
            "message": str(e)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": "unknown",
            "message": str(e)
        }
