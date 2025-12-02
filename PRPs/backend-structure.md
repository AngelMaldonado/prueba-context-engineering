# PRP: Backend Structure & Database Setup

**Feature:** Foundational backend structure for CoachX with FastAPI and SQLAlchemy
**Time:** 1 hour
**Difficulty:** Medium

---

## 1. Overview

### What We're Building
Complete FastAPI backend with SQLAlchemy models, database connection, CORS, and health check endpoint.

### Database Schema
```
┌─────────────────────────────────────┐
│             users                   │
├─────────────────────────────────────┤
│ id (PK)              INTEGER        │
│ name                 VARCHAR(50)    │
│ age                  INTEGER        │
│ sport                VARCHAR(50)    │
│ experience_level     VARCHAR(20)    │
│ days_per_week        INTEGER        │
│ goals                VARCHAR(200)   │
│ created_at           DATETIME       │
│ updated_at           DATETIME       │
└─────────────────────────────────────┘
           │
           │ 1 : N
           │
           ├──────────────────────┐
           │                      │
           ▼                      ▼
┌──────────────────────┐   ┌─────────────────────┐
│   workout_plans      │   │   chat_messages     │
├──────────────────────┤   ├─────────────────────┤
│ id (PK)              │   │ id (PK)             │
│ user_id (FK)         │   │ user_id (FK)        │
│ plan_data (JSON)     │   │ role                │
│ duration_weeks       │   │ message (TEXT)      │
│ created_at           │   │ created_at          │
└──────────────────────┘   └─────────────────────┘
```

**Relations:** 1 User has many WorkoutPlans and ChatMessages. Cascade delete enabled.

### Why CORS?
- Frontend runs on `localhost:3000` (Next.js - Day 4)
- Backend runs on `localhost:8000` (FastAPI)
- Different ports = different origins = CORS needed
- Without CORS: Browser blocks all frontend → backend requests

### Success Criteria
- ✅ Server runs on localhost:8000
- ✅ GET /health returns `{"status": "healthy"}`
- ✅ Database `coachx.db` created with 3 tables
- ✅ Can create test user via Python
- ✅ All functions have type hints
- ✅ CORS configured for localhost:3000

---

## 2. Implementation Steps

### Step 1: Create Directory Structure

```bash
mkdir -p backend/app/database backend/app/api
cd backend
```

Create files:
```bash
touch app/__init__.py
touch app/main.py
touch app/config.py
touch app/database/__init__.py
touch app/database/connection.py
touch app/database/models.py
touch app/api/__init__.py
touch requirements.txt
touch .env.example
touch pytest.ini
```

**Validate:**
```bash
tree app/
```

---

### Step 2: Create requirements.txt

**File:** `backend/requirements.txt`
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
pytest==7.4.3
```

**Install:**
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Validate:**
```bash
pip list | grep fastapi
# Should show fastapi and version
```

---

### Step 3: Create Configuration

**File:** `backend/app/config.py`

**Pattern:** Follow Pydantic Settings pattern for environment variables

```python
"""
Configuration management for CoachX backend.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Application
    APP_NAME: str = "CoachX API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite:///./coachx.db"
    DATABASE_ECHO: bool = False

    # CORS - Allow frontend to make requests
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()
```

**Validate:**
```bash
python -c "from app.config import settings; print(settings.APP_NAME)"
# Output: CoachX API
```

---

### Step 4: Create .env.example

**File:** `backend/.env.example`
```env
# CoachX Backend Configuration
APP_NAME=CoachX API
DEBUG=true
DATABASE_URL=sqlite:///./coachx.db
CORS_ORIGINS=["http://localhost:3000"]
```

---

### Step 5: Create Database Models

**File:** `backend/app/database/models.py`

**Pattern:** Follow `examples/database_model.py` - SQLAlchemy 2.0 with `Mapped` types

```python
"""Database models for CoachX."""

from sqlalchemy import Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class User(Base):
    """
    User model - stores profile and preferences.

    One user has many workout plans and chat messages.
    """

    __tablename__ = "users"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Profile
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    # Training Preferences
    sport: Mapped[str] = mapped_column(String(50), nullable=False)
    # Valid: boxing, crossfit, gym, calisthenics, running

    experience_level: Mapped[str] = mapped_column(String(20), nullable=False)
    # Valid: beginner, intermediate, advanced

    days_per_week: Mapped[int] = mapped_column(Integer, nullable=False)
    # Valid: 1-7

    goals: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Timestamps (REQUIRED)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    workout_plans: Mapped[List["WorkoutPlan"]] = relationship(
        "WorkoutPlan",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    chat_messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name='{self.name}', sport='{self.sport}')>"


class WorkoutPlan(Base):
    """
    Workout plan model - stores AI-generated plans.

    Many workout plans belong to one user.
    """

    __tablename__ = "workout_plans"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Foreign Key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Plan Data (flexible JSON structure)
    plan_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    duration_weeks: Mapped[int] = mapped_column(Integer, nullable=False)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="workout_plans")

    def __repr__(self) -> str:
        return f"<WorkoutPlan(id={self.id}, user_id={self.user_id})>"


class ChatMessage(Base):
    """
    Chat message model - stores conversation history.

    Many messages belong to one user.
    """

    __tablename__ = "chat_messages"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Foreign Key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Message Data
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    # Valid: "user" or "assistant"

    message: Mapped[str] = mapped_column(Text, nullable=False)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="chat_messages")

    def __repr__(self) -> str:
        return f"<ChatMessage(id={self.id}, role='{self.role}')>"
```

**Validate:**
```bash
python -c "from app.database.models import User, WorkoutPlan, ChatMessage; print('✅ Models OK')"
```

---

### Step 6: Create Database Connection

**File:** `backend/app/database/connection.py`

**Pattern:** Session factory with dependency injection

```python
"""Database connection and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging

from app.config import settings
from app.database.models import Base

logger = logging.getLogger(__name__)

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    connect_args={"check_same_thread": False}  # SQLite needs this
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def create_tables() -> None:
    """Create all database tables on startup."""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created")


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for database sessions.

    Usage in endpoints:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Validate:**
```bash
python -c "from app.database.connection import engine; print('✅ Connection OK')"
```

---

### Step 7: Create FastAPI Application

**File:** `backend/app/main.py`

**Pattern:** Follow `examples/api_endpoint.py` structure with CORS

```python
"""
FastAPI application for CoachX backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.database.connection import create_tables

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered personal training assistant",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware - Allow frontend (localhost:3000) to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


@app.on_event("startup")
async def startup_event() -> None:
    """Create database tables on startup."""
    logger.info(f"🚀 Starting {settings.APP_NAME}...")
    create_tables()
    logger.info("✅ Application ready")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Cleanup on shutdown."""
    logger.info("👋 Shutting down...")


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        Status: healthy
    """
    return {"status": "healthy"}


@app.get("/")
async def root() -> dict:
    """
    Root endpoint with API info.
    """
    return {
        "message": "Welcome to CoachX API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


# Future routers will be added here
# from app.api import onboarding, training, chat
# app.include_router(onboarding.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
```

**Validate:**
```bash
python -m app.main
# Should start server without errors
```

---

### Step 8: Create Pytest Config

**File:** `backend/pytest.ini`
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

---

### Step 9: Test the Server

**Start server:**
```bash
cd backend
source venv/bin/activate
python -m app.main
```

**Expected output:**
```
INFO: 🚀 Starting CoachX API...
INFO: Creating database tables...
INFO: ✅ Database tables created
INFO: ✅ Application ready
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Test endpoints (new terminal):**
```bash
curl http://localhost:8000/health
# Output: {"status":"healthy"}

curl http://localhost:8000/
# Output: {"message":"Welcome to CoachX API",...}

open http://localhost:8000/docs
# Should show Swagger UI
```

---

### Step 10: Verify Database

**Check file created:**
```bash
ls backend/coachx.db
# Should exist
```

**Check tables:**
```bash
sqlite3 backend/coachx.db ".tables"
# Output: users  workout_plans  chat_messages
```

---

### Step 11: Test Database Operations

**Create test script:** `backend/test_db.py`
```python
"""Quick database test."""

from app.database.connection import SessionLocal
from app.database.models import User

db = SessionLocal()

try:
    # Create test user
    user = User(
        name="Test User",
        age=25,
        sport="boxing",
        experience_level="beginner",
        days_per_week=3,
        goals="Learn basics"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print(f"✅ Created: {user}")
    print(f"✅ ID: {user.id}")
    print(f"✅ Created at: {user.created_at}")

    # Query back
    queried = db.query(User).filter(User.id == user.id).first()
    print(f"✅ Queried: {queried}")

finally:
    db.close()

print("\n✅ All database operations successful!")
```

**Run:**
```bash
python test_db.py
```

**Expected:**
```
✅ Created: <User(id=1, name='Test User', sport='boxing')>
✅ ID: 1
✅ Created at: 2024-12-02 ...
✅ Queried: <User(id=1, name='Test User', sport='boxing')>

✅ All database operations successful!
```

---

### Step 12: Final Verification

**Checklist:**
- [ ] Server runs on http://localhost:8000
- [ ] GET /health returns `{"status":"healthy"}`
- [ ] GET /docs shows Swagger UI
- [ ] Database file `coachx.db` exists
- [ ] 3 tables created (users, workout_plans, chat_messages)
- [ ] Can create and query users
- [ ] CORS configured (check CORS headers in response)
- [ ] All imports work without errors
- [ ] Logging shows startup messages

**All should pass ✅**

---

## 3. Code Quality Standards

From CLAUDE.md and examples/:

**✅ Required:**
- Type hints on all functions
- Docstrings (Google style)
- Max 100 characters per line
- Functions under 50 lines
- Use `logging` not `print()`
- Timestamps on all models
- Foreign keys with `index=True`
- Relationships with `back_populates`

---

## 4. Commit Message

```bash
git add backend/
git commit -m "feat(backend): initialize FastAPI app with database models

- Setup FastAPI application with CORS middleware
- Create SQLAlchemy 2.0 models (User, WorkoutPlan, ChatMessage)
- Configure database connection with SQLite
- Add health check endpoint at GET /health
- Implement dependency injection for database sessions
- Add environment configuration with Pydantic Settings

Backend foundation ready for feature development."
```

---

## 5. Common Issues

**"No module named 'app'"**
→ Run from `backend/` directory

**"Database is locked"**
→ Only one process can access SQLite at a time

**"ImportError: Mapped"**
→ Upgrade: `pip install --upgrade sqlalchemy`

**Port 8000 in use**
→ Check: `lsof -i :8000` and kill process

---

## 6. Next Steps

After completing:
1. ✅ Test all endpoints
2. ✅ Verify database operations
3. ✅ Commit changes
4. ➡️ Move to Feature 2: RAG System

---

**Ready to execute!**

Estimated time: 45-60 minutes
