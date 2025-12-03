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


def generate_with_rag(
    query: str,
    sport: Optional[str] = None,
    top_k: int = 3
) -> str:
    """
    Generate AI response enhanced with RAG context.

    Queries the RAG system for relevant context, formats it into a prompt,
    and generates a response using Gemini that combines the context with
    LLM reasoning.

    Args:
        query: User's question or request
        sport: Optional sport filter (boxing, crossfit, gym, etc.)
        top_k: Number of RAG context chunks to retrieve (default: 3)

    Returns:
        AI-generated response incorporating RAG context

    Raises:
        GeminiGenerationError: If generation fails

    Example:
        >>> response = generate_with_rag(
        ...     query="How do I improve my jab?",
        ...     sport="boxing",
        ...     top_k=3
        ... )
        >>> print(response)
    """
    try:
        logger.info(f"RAG-enhanced generation for query: {query[:50]}... (sport={sport})")

        # Step 1: Query RAG system for context
        rag_results = query_knowledge(query=query, sport=sport, top_k=top_k)
        context = format_context_for_llm(rag_results)

        logger.info(f"Retrieved {len(rag_results)} context chunks from RAG")

        # Step 2: Build prompt with context
        sport_context = f" specializing in {sport}" if sport else ""

        prompt = f"""You are CoachX, an expert personal training assistant{sport_context}.

IMPORTANT RULES:
1. You ONLY answer questions related to fitness, training, sports, exercise, nutrition, and athletic performance.
2. If the user asks about topics unrelated to fitness (cooking, politics, general knowledge, etc.), you MUST respond with:
   "Lo siento, solo puedo ayudarte con temas relacionados con entrenamiento, ejercicio y fitness. ¿Tienes alguna pregunta sobre tu entrenamiento?"
3. If the user uses inappropriate language or insults, respond professionally and redirect:
   "Estoy aquí para ayudarte con tu entrenamiento. ¿En qué puedo asistirte?"
4. DO NOT use your general knowledge to answer non-fitness questions.

You have access to official training knowledge from professional sources.

CONTEXT FROM KNOWLEDGE BASE:
{context}

USER QUESTION:
{query}

First, determine if this question is related to fitness, training, sports, exercise, or nutrition.
- If YES: Provide accurate, helpful, and motivating training advice based on the context above.
  Always prioritize safety and proper technique. Keep your response clear, concise, and actionable.
- If NO: Respond with the appropriate message from the rules above.

REMEMBER: You are a fitness assistant ONLY. Do not answer questions outside your domain."""

        # Step 3: Generate response
        response = generate_response(prompt)

        logger.info("RAG-enhanced response generated successfully")
        return response

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
