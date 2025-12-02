# CLAUDE.md - CoachX Project Guide

This file provides comprehensive guidance to Claude Code when working on CoachX, an AI-powered personal training assistant.

## 🎯 Project Overview

**CoachX** is an intelligent training assistant that creates personalized workout plans using AI and Retrieval Augmented Generation (RAG), with conversational onboarding and adaptive progression tracking.

**Tech Stack:**

- **Backend:** FastAPI 0.104+ (Python)
- **Frontend:** Next.js 14 (TypeScript/React)
- **Database:** SQLite with SQLAlchemy 2.0+
- **AI Framework:** LangChain 0.1+
- **Vector DB:** ChromaDB (local, persistent)
- **LLM:** Google Gemini Flash (free tier)
- **Embeddings:** sentence-transformers (local, free)

**Key Features:**

1. Conversational onboarding (chat-style profile creation)
2. AI-powered workout plan generation
3. RAG system with sport-specific knowledge base
4. Interactive chat for training questions
5. Weekly adaptive check-ins

**Target Sports:** Boxing, CrossFit, Gym, Calisthenics, Running

## 🧱 Core Development Philosophy

### KISS (Keep It Simple, Stupid)

Simplicity should be a key goal in design. Choose straightforward solutions over complex ones whenever possible. This is an MVP - focus on core functionality that works.

### YAGNI (You Aren't Gonna Need It)

Avoid building functionality on speculation. This is a 4-day technical assessment - implement only what's required to demonstrate competence.

### Design Principles

- **Single Responsibility**: Each function, class, and module should have one clear purpose
- **Fail Fast**: Check for potential errors early and raise exceptions immediately
- **DRY**: Don't Repeat Yourself - reuse code through functions and modules
- **Code for Humans**: Write code that's easy to understand and maintain

## 🏗️ Code Structure & Modularity

### File and Function Limits

- **Files should not exceed 500 lines** - Split into smaller modules if approaching this limit
- **Functions should be under 50 lines** with a single, clear responsibility
- **Classes should be under 100 lines** and represent a single concept
- **Line length: maximum 100 characters** (enforced in backend, preferred in frontend)

### Project Architecture

```
coachx/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Environment configuration
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py   # Database setup
│   │   │   ├── models.py       # SQLAlchemy models
│   │   │   └── tests/
│   │   │       └── test_models.py
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── gemini.py       # Gemini integration
│   │   │   ├── rag.py          # RAG system
│   │   │   ├── prompts.py      # AI prompts
│   │   │   └── tests/
│   │   │       └── test_rag.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── onboarding.py   # Onboarding endpoints
│   │   │   ├── training.py     # Training plan endpoints
│   │   │   ├── chat.py         # Chat endpoints
│   │   │   └── tests/
│   │   │       └── test_api.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── onboarding_service.py
│   │       ├── training_service.py
│   │       └── tests/
│   ├── knowledge_base/          # RAG documents
│   │   ├── boxing/
│   │   ├── crossfit/
│   │   └── gym/
│   ├── requirements.txt
│   ├── .env.example
│   └── pytest.ini
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx           # Home page
│   │   │   ├── onboarding/
│   │   │   │   └── page.tsx       # Onboarding flow
│   │   │   ├── plan/
│   │   │   │   └── page.tsx       # Training plan view
│   │   │   └── chat/
│   │   │       └── page.tsx       # Chat interface
│   │   ├── components/
│   │   │   ├── chat/
│   │   │   │   ├── ChatMessage.tsx
│   │   │   │   └── ChatInput.tsx
│   │   │   └── ui/                # shadcn/ui components
│   │   ├── lib/
│   │   │   ├── api.ts             # API client
│   │   │   └── utils.ts           # Utilities
│   │   └── store/
│   │       └── userStore.ts       # Zustand state
│   ├── package.json
│   ├── .env.local.example
│   └── tailwind.config.ts
│
├── examples/                      # Reference patterns (CRITICAL)
│   ├── README.md
│   ├── api_endpoint.py
│   ├── database_model.py
│   ├── rag_query.py
│   ├── chat_conversation.json
│   └── component.tsx
│
├── PRPs/                          # Generated PRPs
│   └── templates/
│
├── docs/
│   ├── CONTEXT_ENGINEERING.md
│   └── cv.pdf
│
├── .claude/                       # Claude Code configuration
│   └── commands/
│       ├── generate-prp.md
│       └── execute-prp.md
│
├── CLAUDE.md                      # This file
├── PLAN.md                        # Development roadmap
├── INITIAL.md                     # Template for features
└── README.md
```

## 🛠️ Development Environment

### Package Management

**Backend (Python):**

```bash
# Use standard pip (not uv for this project - keep it simple)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add a package
pip install package-name
pip freeze > requirements.txt
```

**Frontend (Node.js):**

```bash
# Use npm (comes with Node.js)
npm install
npm install package-name
npm install --save-dev package-name  # For dev dependencies
```

### Development Commands

**Backend:**

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
python -m uvicorn app.main:app --reload --port 8000

# Alternative: Direct execution
python app/main.py

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Format code (if black is installed)
black app/

# Type checking (if mypy is installed)
mypy app/
```

**Frontend:**

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run production server
npm start

# Lint
npm run lint

# Type check
npm run type-check  # if configured
```

## 📋 Style & Conventions

### Python Style Guide

- **Follow PEP8** with these specifics:
  - Line length: 100 characters maximum
  - Use double quotes for strings
  - Use trailing commas in multi-line structures
- **Always use type hints** for function signatures and class attributes
- **Use Pydantic v2** for data validation and settings management

### TypeScript/React Style Guide

- **Use TypeScript** for all new files
- **Functional components** only (no class components)
- **'use client'** directive when needed for client-side features
- **Export interfaces** for all component props
- **Use Tailwind classes** for styling (no inline styles)

### Docstring Standards

Use Google-style docstrings for all public functions:

```python
def generate_workout_plan(
    user_id: int,
    sport: str,
    experience_level: str,
    days_per_week: int
) -> WorkoutPlan:
    """
    Generate a personalized workout plan for a user.

    Args:
        user_id: Unique identifier for the user
        sport: Sport type (boxing, crossfit, gym, etc.)
        experience_level: beginner, intermediate, or advanced
        days_per_week: Number of training days per week (1-7)

    Returns:
        Complete workout plan with exercises and schedules

    Raises:
        ValueError: If sport is not supported
        ValueError: If days_per_week is not between 1-7

    Example:
        >>> plan = generate_workout_plan(123, "boxing", "intermediate", 4)
        >>> print(plan.weekly_schedule)
    """
```

### Naming Conventions

**Python:**

- Variables and functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private attributes/methods: `_leading_underscore`

**TypeScript/React:**

- Variables and functions: `camelCase`
- Components: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Interfaces/Types: `PascalCase`

**Database:**

- Tables: `plural_snake_case` (users, workout_plans, chat_messages)
- Columns: `snake_case`
- Primary keys: `id`
- Foreign keys: `{table}_id` (user_id, plan_id)
- Timestamps: `created_at`, `updated_at`

## 🧪 Testing Strategy

### Testing Best Practices

```python
# Use pytest fixtures for setup
import pytest
from datetime import datetime

@pytest.fixture
def sample_user():
    """Provide a sample user for testing."""
    return {
        "id": 1,
        "name": "Test User",
        "age": 25,
        "sport": "boxing",
        "experience_level": "intermediate"
    }

# Use descriptive test names
def test_workout_plan_includes_correct_sport_exercises(sample_user):
    """Test that generated plans include sport-specific exercises."""
    plan = generate_workout_plan(sample_user)
    assert any("boxing" in ex.name.lower() for ex in plan.exercises)

# Test edge cases
def test_workout_plan_fails_with_invalid_sport(sample_user):
    """Test that invalid sports are rejected."""
    sample_user["sport"] = "invalid_sport"
    with pytest.raises(ValueError) as exc_info:
        generate_workout_plan(sample_user)
    assert "Unsupported sport" in str(exc_info.value)
```

### Test Organization

- Keep test files next to the code they test (in `tests/` subdirectories)
- Unit tests: Test individual functions/methods
- Integration tests: Test API endpoints
- Focus on critical paths: AI generation, RAG queries, user flows
- Aim for 70%+ code coverage on core business logic

## 🚨 Error Handling

### Exception Best Practices

```python
# Create custom exceptions for your domain
class CoachXError(Exception):
    """Base exception for CoachX application."""
    pass

class AIGenerationError(CoachXError):
    """Raised when AI fails to generate content."""
    pass

class RAGQueryError(CoachXError):
    """Raised when RAG system fails to retrieve information."""
    pass

# Use specific exception handling
from fastapi import HTTPException, status

try:
    plan = await generate_plan(user_data)
except AIGenerationError as e:
    logger.error(f"AI generation failed: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to generate training plan"
    )
except ValidationError as e:
    logger.warning(f"Invalid input: {e}")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e)
    )
```

### Logging Strategy

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Log important events
logger.info("User completed onboarding", extra={"user_id": user_id})
logger.warning("Rate limit approaching", extra={"requests": request_count})
logger.error("AI generation failed", extra={"error": str(e)})
```

## 🤖 AI & RAG System Guidelines

### Gemini Flash Integration

```python
# Key considerations:
# - Free tier: 15 requests per minute (RPM)
# - Be mindful of rate limits
# - Implement retry logic with exponential backoff
# - Cache responses when appropriate

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def call_gemini(prompt: str) -> str:
    """Call Gemini API with retry logic."""
    response = await genai.generate_text(prompt=prompt)
    return response.text
```

### RAG System Best Practices

```python
# ChromaDB configuration
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# Use local embeddings (free, fast, no API)
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"  # Fast and effective
)

# Persistent storage
vectorstore = Chroma(
    collection_name="coachx_knowledge",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# Query configuration
CHUNK_SIZE = 500  # tokens per chunk
CHUNK_OVERLAP = 50  # tokens overlap
TOP_K = 3  # number of relevant chunks to retrieve
```

### Prompt Engineering

```python
# Store prompts in a dedicated module
# app/ai/prompts.py

ONBOARDING_PROMPT = """
You are CoachX, a professional and motivational personal training assistant.
Your goal is to help {name} create their personalized training profile.

Ask ONE question at a time in a friendly, conversational manner.
Current question: {current_question}
User's previous responses: {user_context}

Be encouraging and professional. Keep responses concise (2-3 sentences).
"""

PLAN_GENERATION_PROMPT = """
Generate a personalized {duration}-week training plan for:
- Sport: {sport}
- Experience Level: {experience_level}
- Days per week: {days_per_week}
- Goals: {goals}

Context from knowledge base:
{rag_context}

Create a structured plan with:
1. Weekly overview
2. Daily workouts with exercises, sets, reps
3. Progression notes
4. Recovery recommendations

Format as JSON.
"""
```

## 🎨 Frontend Guidelines

### Next.js 14 App Router

```typescript
// Use App Router conventions
// app/page.tsx - Server component by default

export default function HomePage() {
  return (
    <main className="min-h-screen bg-black text-white">
      <h1 className="text-4xl font-bold text-red-600">CoachX</h1>
    </main>
  );
}

// Client components - use 'use client' directive
// app/onboarding/page.tsx

("use client");

import { useState } from "react";

export default function OnboardingPage() {
  const [step, setStep] = useState(0);
  // ... client-side logic
}
```

### Tailwind & Theme

```typescript
// Use Bred theme consistently (Black + Red)
const THEME = {
  colors: {
    primary: "#DC2626", // red-600
    background: "#000000", // black
    surface: "#1A1A1A", // dark gray
    text: "#FFFFFF", // white
    textSecondary: "#9CA3AF", // gray-400
  },
};

// Example usage
<div className="bg-black text-white">
  <button className="bg-red-600 hover:bg-red-700">Start Training</button>
</div>;
```

### State Management (Zustand)

```typescript
// src/store/userStore.ts
import { create } from "zustand";

interface UserStore {
  userId: number | null;
  profile: UserProfile | null;
  setProfile: (profile: UserProfile) => void;
  clearProfile: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  userId: null,
  profile: null,
  setProfile: (profile) => set({ profile }),
  clearProfile: () => set({ profile: null, userId: null }),
}));
```

### API Client

```typescript
// src/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return response.json();
}
```

## 📊 Database Guidelines

### SQLAlchemy Models

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    sport = Column(String, nullable=False)
    experience_level = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    workout_plans = relationship("WorkoutPlan", back_populates="user")
    chat_messages = relationship("ChatMessage", back_populates="user")

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_data = Column(JSON, nullable=False)  # Flexible storage
    duration_weeks = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="workout_plans")
```

## 🔍 Context Engineering Specifics

### Before Starting Any Feature

1. **Read CLAUDE.md** (this file) completely
2. **Check examples/** for existing patterns to follow
3. **Review similar code** in the codebase
4. **Verify requirements** in INITIAL.md
5. **Check PLAN.md** for context on overall project

### When Implementing from a PRP

1. **Read the entire PRP** before starting
2. **Follow the steps in order** as specified
3. **Run validation commands** after each major step
4. **Fix issues immediately** before proceeding
5. **Test thoroughly** before marking complete

### Quality Checklist (Before Committing)

- [ ] Code follows style guide (PEP8 for Python, consistent for TypeScript)
- [ ] Type hints present (Python) or TypeScript types defined
- [ ] Functions under 50 lines, files under 500 lines
- [ ] Tests written for new functionality
- [ ] No hardcoded values (use environment variables)
- [ ] Error handling implemented
- [ ] Logging added for important events
- [ ] No sensitive data in code
- [ ] Documentation updated (if needed)

## 🚀 Performance Considerations

### Backend Optimization

```python
# Use async for I/O operations
from fastapi import FastAPI
import asyncio

@app.post("/chat")
async def chat_endpoint(message: str):
    # Run AI and RAG queries concurrently
    rag_results, ai_response = await asyncio.gather(
        query_rag_system(message),
        call_gemini(message)
    )
    return combine_responses(rag_results, ai_response)
```

### Frontend Optimization

```typescript
// Use React.memo for expensive components
import { memo } from "react";

export const ChatMessage = memo(function ChatMessage({ message }) {
  return <div>{message.text}</div>;
});

// Use dynamic imports for large components
const PlanViewer = dynamic(() => import("@/components/PlanViewer"), {
  loading: () => <p>Loading plan...</p>,
});
```

## 🛡️ Security Best Practices

### Environment Variables

```python
# backend/.env
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./coachx.db
CHROMA_PERSIST_DIRECTORY=./chroma_db
ALLOWED_ORIGINS=http://localhost:3000

# NEVER commit .env files
# Always use .env.example as template
```

```typescript
// frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

// Only NEXT_PUBLIC_* variables are exposed to browser
// Other variables are server-side only
```

### Input Validation

```python
from pydantic import BaseModel, Field, validator

class OnboardingRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, lt=120)
    sport: str
    experience_level: str

    @validator('sport')
    def sport_must_be_valid(cls, v):
        allowed = ['boxing', 'crossfit', 'gym', 'calisthenics', 'running']
        if v.lower() not in allowed:
            raise ValueError(f'Sport must be one of {allowed}')
        return v.lower()

    @validator('experience_level')
    def level_must_be_valid(cls, v):
        allowed = ['beginner', 'intermediate', 'advanced']
        if v.lower() not in allowed:
            raise ValueError(f'Level must be one of {allowed}')
        return v.lower()
```

## 📚 Useful Resources

### Documentation Links

**Backend:**

- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- LangChain: https://python.langchain.com/
- ChromaDB: https://docs.trychroma.com/
- Google Gemini: https://ai.google.dev/docs

**Frontend:**

- Next.js 14: https://nextjs.org/docs
- React: https://react.dev/
- TailwindCSS: https://tailwindcss.com/docs
- shadcn/ui: https://ui.shadcn.com/
- Zustand: https://docs.pmnd.rs/zustand/

**Context Engineering:**

- Template: https://github.com/coleam00/context-engineering-intro
- Assessment Repo: https://github.com/AngelMaldonado/prueba-context-engineering

## ⚠️ Important Notes

### Critical Guidelines

- **NEVER commit sensitive data** (.env files, API keys)
- **Always use type hints** in Python code
- **Test before committing** - No feature is complete without tests
- **Follow the examples** - Check examples/ folder for patterns
- **Ask for clarification** - Don't assume or guess
- **Document your decisions** - Update docs when needed
- **Keep it simple** - This is a 4-day MVP, not a production app

### Common Gotchas

1. **Gemini Flash rate limits**: 15 RPM on free tier - implement rate limiting
2. **ChromaDB persistence**: Always specify persist_directory
3. **Next.js 14 App Router**: Different from Pages Router - use correct conventions
4. **CORS**: Configure FastAPI CORS for frontend access
5. **SQLite limitations**: Not suitable for production, but perfect for MVP
6. **Type hints**: Required in Python for maintainability

## 🎯 MVP Scope Reminder

**Include (Core Features):**

- ✅ Onboarding chat (8 questions)
- ✅ RAG system with knowledge base
- ✅ AI plan generation
- ✅ Chat interface
- ✅ Weekly check-ins

**Exclude (Out of Scope):**

- ❌ Authentication/Login (single user)
- ❌ Nutrition tracking
- ❌ Progress photos
- ❌ Social features
- ❌ Mobile app
- ❌ Payment system

Focus on demonstrating **AI engineering skills** and **Context Engineering mastery**.

---

## 📞 Project-Specific Commands Summary

**Backend:**

```bash
source venv/bin/activate                    # Activate environment
pip install -r requirements.txt             # Install dependencies
python -m uvicorn app.main:app --reload   # Run server
pytest                                      # Run tests
```

**Frontend:**

```bash
npm install                    # Install dependencies
npm run dev                    # Run dev server
npm run build                  # Build for production
npm run lint                   # Lint code
```

**Git:**

```bash
git add .
git commit -m "feat(scope): description"   # Conventional commits
git push origin main
```

---

_This document is a living guide for CoachX development. Update it as patterns emerge._
