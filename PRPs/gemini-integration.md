# PRP: Gemini AI Integration

**Feature:** Google Gemini API integration for AI-powered response generation
**Time:** 30-45 minutes
**Difficulty:** Medium

---

## 1. Feature Overview

### What We're Building
Complete integration of Google Gemini Flash API to generate AI-powered responses for CoachX, combining RAG context with LLM capabilities for personalized training advice.

### Architecture
```
User Query → RAG System (query_knowledge)
                ↓
         Context Retrieved
                ↓
         Gemini API Client
                ↓
    Prompt + Context → Gemini Flash
                ↓
         AI Response
                ↓
    Return to User (via API endpoint)
```

### Why This Feature Matters
- Enables conversational AI coaching responses
- Combines factual RAG context with LLM reasoning
- Provides personalized, motivating training advice
- Uses free tier Gemini Flash (fast and cost-effective)

### Success Criteria
- ✅ Gemini API client successfully authenticates
- ✅ Can generate basic text responses without context
- ✅ Can generate RAG-enhanced responses with sport-specific context
- ✅ Error handling for API failures, rate limits, timeouts
- ✅ Safety settings prevent inappropriate content
- ✅ Test endpoint `/ai/chat` returns coherent responses
- ✅ Response time < 3 seconds for typical queries
- ✅ Configuration properly loaded from environment

---

## 2. Technical Approach

### Technology Choices
- **google-generativeai** SDK (official Python client)
- **gemini-1.5-flash** model (fast, free tier, good for chat)
- **Singleton pattern** for client (consistent with RAG module)
- **Environment-based configuration** (Pydantic Settings)
- **Structured prompt templates** (similar to examples/)

### Integration Points
1. **With RAG System** (`app.ai.rag`): Import `query_knowledge`, `format_context_for_llm`
2. **With Config** (`app.config`): Add `GEMINI_API_KEY`, `GEMINI_MODEL` to Settings
3. **With FastAPI** (`app.main`): Add test endpoint `/ai/chat`

### Key Patterns to Follow
- **Singleton pattern** (from rag.py): `get_gemini_client()`
- **Error handling** (from api_endpoint.py): Try/except with specific exceptions
- **Type hints** (project standard): All function signatures
- **Google docstrings** (project standard): All public functions
- **Logging** (from rag.py): Info/warning/error with context

---

## 3. File Structure

### Files to Create
```
backend/app/ai/gemini.py         ← Main Gemini integration module
```

### Files to Modify
```
backend/app/config.py            ← Add GEMINI_API_KEY, GEMINI_MODEL
backend/app/main.py              ← Add /ai/chat test endpoint
backend/requirements.txt         ← Add google-generativeai
backend/.env.example             ← Add GEMINI_API_KEY example
```

### Files to Reference (Do Not Modify)
```
backend/app/ai/rag.py            ← RAG functions to import
```

---

## 4. Step-by-Step Implementation Plan

### Step 1: Install Gemini SDK

**Action:** Add dependency and install

**File:** `backend/requirements.txt`

Add at the end:
```txt
google-generativeai==0.3.1
```

**Command:**
```bash
cd backend
source venv/bin/activate
pip install google-generativeai==0.3.1
```

**Validation:**
```bash
python -c "import google.generativeai as genai; print('✅ Gemini SDK installed')"
```

**Expected:** `✅ Gemini SDK installed`

---

### Step 2: Update Configuration

**Action:** Add Gemini settings to Pydantic config

**File:** `backend/app/config.py`

Add these fields inside the `Settings` class (after CORS settings):

```python
    # AI - Google Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"
```

**Validation:**
```bash
python -c "from app.config import settings; print(f'Model: {settings.GEMINI_MODEL}'); print('✅ Config updated')"
```

**Expected:** `Model: gemini-1.5-flash` and `✅ Config updated`

---

### Step 3: Update Environment Example

**Action:** Add Gemini API key placeholder

**File:** `backend/.env.example`

Add at the end:
```bash
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

---

### Step 4: Create Gemini Module

**Action:** Implement main Gemini integration module

**File:** `backend/app/ai/gemini.py`

**Full Implementation:**

```python
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

You have access to official training knowledge from professional sources.

CONTEXT FROM KNOWLEDGE BASE:
{context}

USER QUESTION:
{query}

Provide accurate, helpful, and motivating training advice based on the context above.
If the context doesn't contain relevant information, use your general knowledge but mention this.
Always prioritize safety and proper technique.
Keep your response clear, concise, and actionable."""

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
```

**Validation:**
```bash
python -c "from app.ai.gemini import get_gemini_client; print('✅ Gemini module created')"
```

---

### Step 5: Add Test Endpoints

**Action:** Add `/ai/chat` endpoint to test Gemini integration

**File:** `backend/app/main.py`

Add import at top (after other imports):
```python
from app.ai.gemini import generate_with_rag, test_gemini_connection, GeminiAuthenticationError
```

Add endpoints after the `/rag/query` endpoint:

```python
@app.get("/ai/test")
async def ai_test() -> dict:
    """
    Test Gemini API connection.

    Returns:
        Connection test results
    """
    return test_gemini_connection()


@app.get("/ai/chat")
async def ai_chat(
    q: str,
    sport: Optional[str] = None,
    top_k: int = 3
) -> dict:
    """
    AI chat endpoint with RAG context.

    Combines RAG retrieval with Gemini generation to provide
    context-aware, personalized training advice.

    Args:
        q: User's question
        sport: Optional sport filter (boxing, crossfit, gym)
        top_k: Number of RAG context chunks (default: 3)

    Returns:
        AI-generated response with metadata

    Example:
        GET /ai/chat?q=how+to+improve+jab&sport=boxing
    """
    from fastapi import HTTPException, status

    try:
        if not q or len(q.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query parameter 'q' is required"
            )

        logger.info(f"Chat request: q='{q[:50]}...', sport={sport}")

        response_text = generate_with_rag(query=q, sport=sport, top_k=top_k)

        return {
            "query": q,
            "sport": sport,
            "response": response_text,
            "status": "success"
        }

    except GeminiAuthenticationError as e:
        logger.error(f"Gemini authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI service not configured. Please check GEMINI_API_KEY."
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response: {str(e)}"
        )
```

**Validation:**
```bash
python -c "from app.main import app; print('✅ Endpoints added')"
```

---

### Step 6: Start Server and Test

**Action:** Start FastAPI server and test Gemini integration

**Commands:**
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

**Expected Output:**
```
INFO: Starting CoachX API...
INFO: RAG System: 138 chunks loaded
INFO: Application startup complete
INFO: Uvicorn running on http://127.0.0.1:8000
```

---

### Step 7: Test Basic Connection

**Action:** Test Gemini API connection

**Command:**
```bash
curl http://127.0.0.1:8000/ai/test
```

**Expected Success:**
```json
{
  "status": "success",
  "model": "gemini-1.5-flash",
  "test_response": "CoachX is ready!",
  "message": "Gemini API connection successful"
}
```

---

### Step 8: Test RAG-Enhanced Chat

**Action:** Test full RAG + Gemini integration

**Test 1: Boxing Query**
```bash
curl "http://127.0.0.1:8000/ai/chat?q=how+to+throw+a+proper+jab&sport=boxing"
```

**Expected:** Detailed response about jab technique with context from knowledge base

**Test 2: CrossFit Query**
```bash
curl "http://127.0.0.1:8000/ai/chat?q=warmup+routine&sport=crossfit"
```

**Test 3: General Query**
```bash
curl "http://127.0.0.1:8000/ai/chat?q=beginner+workout+plan&sport=gym"
```

---

### Step 9: Final Validation

**Checklist:**

- [ ] `google-generativeai` in requirements.txt
- [ ] `GEMINI_API_KEY` added to config.py
- [ ] `backend/app/ai/gemini.py` created with all functions
- [ ] Singleton pattern implemented
- [ ] Error classes defined
- [ ] All functions have type hints and docstrings
- [ ] `/ai/test` endpoint works
- [ ] `/ai/chat` endpoint works
- [ ] Response quality is appropriate
- [ ] `.env` file has valid API key

---

## 5. Testing Strategy

### Manual Tests

**Test 1: Connection**
```bash
curl http://127.0.0.1:8000/ai/test
```

**Test 2: Basic Chat**
```bash
curl "http://127.0.0.1:8000/ai/chat?q=what+is+a+jab"
```

**Test 3: Sport-Specific**
```bash
curl "http://127.0.0.1:8000/ai/chat?q=warmup&sport=crossfit&top_k=5"
```

---

## 6. Commit Message Suggestions

### Option 1: Single Commit
```bash
feat(ai): integrate Google Gemini Flash for AI generation

- Add google-generativeai SDK (v0.3.1)
- Implement Gemini client with singleton pattern
- Create generate_response() for basic generation
- Create generate_with_rag() for context-aware responses
- Add /ai/test and /ai/chat endpoints
- Implement safety settings and error handling

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Option 2: Atomic Commits

**Commit 1:**
```bash
build(ai): add Gemini SDK dependency

- Add google-generativeai==0.3.1 to requirements.txt

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Commit 2:**
```bash
feat(ai): implement Gemini client and generation

- Create app/ai/gemini.py with Gemini integration
- Implement get_gemini_client() with singleton pattern
- Add generate_response() and generate_with_rag()
- Add error handling and safety settings
- Update config.py with GEMINI_API_KEY setting

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Commit 3:**
```bash
feat(api): add AI chat endpoints with RAG integration

- Add /ai/test endpoint for connection testing
- Add /ai/chat endpoint for RAG-enhanced chat
- Integrate Gemini with existing RAG system

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## 7. Common Issues & Solutions

### Issue: "API key not found"
**Solution:** Create `backend/.env` with `GEMINI_API_KEY=your_key_here`

### Issue: "Module not found: google.generativeai"
**Solution:** `pip install google-generativeai==0.3.1`

### Issue: "Rate limit exceeded"
**Solution:** Wait 60 seconds (free tier: 15 RPM)

### Issue: "Empty response"
**Solution:** Check safety settings, verify prompt is valid

---

**Ready to execute!**
**Estimated time:** 30-45 minutes
**Complexity:** Medium
