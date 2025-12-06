# PRP: User Onboarding & Profiles (MVP) - CoachX

**Feature**: User Onboarding & Profiles (Single User MVP)
**Status**: Planning
**Priority**: High
**Estimated Complexity**: Medium

---

## 1. Objective

Implement a simplified user profile system for MVP that captures user preferences, fitness goals, experience level, and limitations. This enables personalized training recommendations without the complexity of multi-user authentication.

**Key Goals:**
- Store single user profile in database
- Capture essential onboarding data
- Enable profile updates and management
- Provide foundation for personalized AI coaching
- **DEFER to post-MVP**: Multi-user support, authentication, login/register

---

## 2. MVP Simplifications

### What We're Building (MVP)
- ✅ Single user profile (no authentication)
- ✅ Onboarding flow to capture user data
- ✅ Profile storage in SQLite
- ✅ Profile retrieval and updates
- ✅ AI chat personalization using profile

### What We're Deferring (Post-MVP)
- ❌ User registration/login
- ❌ JWT authentication
- ❌ Password management
- ❌ Multiple user accounts
- ❌ Email verification

**Rationale**: For MVP running locally, a single user profile is sufficient. Authentication adds complexity that's not needed for testing personalization features.

---

## 3. Current State

### What We Have ✅
- SQLAlchemy configured with SQLite
- FastAPI backend structure
- RAG system with general training knowledge
- Gemini AI integration for responses

### What's Missing ❌
- User profile model
- Onboarding endpoints
- Profile storage and retrieval
- User context in AI responses

---

## 4. Requirements

### 4.1 Functional Requirements

**Single User Profile:**
- System maintains one user profile
- Profile created on first onboarding
- Profile persists across server restarts
- Profile can be updated/reset

**Onboarding Flow:**
- Capture personal information (name, age, gender)
- Capture fitness background (experience level, primary sport)
- Capture goals (weight loss, muscle gain, endurance, etc.)
- Capture limitations (injuries, health conditions)
- Capture availability (days per week, session duration)
- Capture preferences (equipment access, gym membership)

**Profile Management:**
- View current profile
- Update profile information
- Update fitness goals
- Reset profile (start onboarding again)
- Track profile completion status

### 4.2 Technical Requirements

**Database Models:**
- `User`: Simple user record (id=1, name)
- `UserProfile`: Detailed fitness and preference data
- Automatic creation of default user on startup

**API Endpoints:**
- `GET /api/profile` - Get current user profile
- `POST /api/profile/onboarding` - Submit onboarding data
- `PUT /api/profile` - Update user profile
- `PATCH /api/profile/goals` - Update fitness goals
- `DELETE /api/profile` - Reset profile (for testing)

**No Authentication Required:**
- All endpoints are public (single user)
- No tokens, no passwords, no sessions
- Simple and fast for MVP

---

## 5. Database Schema

### 5.1 User Model (Simplified)

```python
class User(Base):
    """Single user for MVP."""
    __tablename__ = "users"

    id: int = 1  # Always 1 for MVP
    full_name: str
    created_at: datetime
    updated_at: datetime

    # Relationships
    profile: UserProfile (one-to-one)
```

### 5.2 UserProfile Model

```python
class UserProfile(Base):
    """Detailed user fitness profile from onboarding."""
    __tablename__ = "user_profiles"

    id: int (PK, autoincrement)
    user_id: int = 1  # Always links to user id=1

    # Personal Information
    age: int (optional)
    gender: str (male/female/other/prefer_not_to_say)
    height_cm: float (optional)
    weight_kg: float (optional)

    # Fitness Background
    experience_level: str (beginner/intermediate/advanced)
    primary_sport: str (boxing/crossfit/gym/running/other)
    secondary_sports: JSON (list of additional sports)
    years_training: int (optional)

    # Goals (JSON array)
    fitness_goals: JSON ([
        "weight_loss", "muscle_gain", "strength",
        "endurance", "flexibility", "athletic_performance",
        "general_fitness", "stress_relief"
    ])

    # Limitations & Health
    injuries: JSON (list of current/past injuries)
    health_conditions: JSON (list of conditions)
    medications: JSON (optional)

    # Availability & Preferences
    available_days_per_week: int (1-7)
    preferred_session_duration: int (minutes)
    preferred_training_times: JSON (morning/afternoon/evening)

    # Equipment & Access
    has_gym_membership: bool
    available_equipment: JSON (list of equipment)
    training_location: str (home/gym/outdoor/hybrid)

    # Onboarding Status
    onboarding_completed: bool (default=False)
    onboarding_completed_at: datetime (optional)
    profile_completion_percentage: int (0-100)

    # Timestamps
    created_at: datetime
    updated_at: datetime

    # Relationships
    user: User
```

### 5.3 Database Tables SQL

```sql
-- Users table (simplified for MVP)
CREATE TABLE users (
    id INTEGER PRIMARY KEY CHECK (id = 1),  -- Only allow id=1
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User profiles table
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL DEFAULT 1,

    -- Personal info
    age INTEGER,
    gender VARCHAR(50),
    height_cm REAL,
    weight_kg REAL,

    -- Fitness background
    experience_level VARCHAR(50),
    primary_sport VARCHAR(100),
    secondary_sports TEXT,  -- JSON
    years_training INTEGER,

    -- Goals and limitations
    fitness_goals TEXT,  -- JSON
    injuries TEXT,  -- JSON
    health_conditions TEXT,  -- JSON
    medications TEXT,  -- JSON

    -- Availability
    available_days_per_week INTEGER,
    preferred_session_duration INTEGER,
    preferred_training_times TEXT,  -- JSON

    -- Equipment
    has_gym_membership BOOLEAN,
    available_equipment TEXT,  -- JSON
    training_location VARCHAR(50),

    -- Status
    onboarding_completed BOOLEAN DEFAULT 0,
    onboarding_completed_at TIMESTAMP,
    profile_completion_percentage INTEGER DEFAULT 0,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (user_id = 1)  -- Only allow user_id=1 for MVP
);

-- Create default user
INSERT INTO users (id, full_name) VALUES (1, 'Default User');
```

---

## 6. API Endpoints Specification

### 6.1 Get Profile

#### GET /api/profile
**Description**: Get current user profile
**Authentication**: None (single user MVP)

**Response (200 OK) - Profile exists:**
```json
{
  "user": {
    "id": 1,
    "full_name": "John Doe"
  },
  "profile": {
    "id": 1,
    "age": 28,
    "gender": "male",
    "height_cm": 175,
    "weight_kg": 75,
    "experience_level": "intermediate",
    "primary_sport": "boxing",
    "secondary_sports": ["running", "gym"],
    "fitness_goals": ["muscle_gain", "strength"],
    "injuries": ["previous_knee_injury"],
    "available_days_per_week": 4,
    "preferred_session_duration": 60,
    "has_gym_membership": true,
    "training_location": "gym",
    "onboarding_completed": true,
    "profile_completion_percentage": 100,
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

**Response (200 OK) - No profile yet:**
```json
{
  "user": {
    "id": 1,
    "full_name": "Default User"
  },
  "profile": null,
  "message": "No profile created yet. Complete onboarding to get started."
}
```

---

### 6.2 Submit Onboarding

#### POST /api/profile/onboarding
**Description**: Submit onboarding data (creates or updates profile)
**Authentication**: None

**Request Body:**
```json
{
  "full_name": "John Doe",
  "personal_info": {
    "age": 28,
    "gender": "male",
    "height_cm": 175,
    "weight_kg": 75
  },
  "fitness_background": {
    "experience_level": "intermediate",
    "primary_sport": "boxing",
    "secondary_sports": ["running", "gym"],
    "years_training": 3
  },
  "goals": [
    "muscle_gain",
    "strength",
    "athletic_performance"
  ],
  "limitations": {
    "injuries": ["previous_knee_injury"],
    "health_conditions": [],
    "medications": []
  },
  "availability": {
    "available_days_per_week": 4,
    "preferred_session_duration": 60,
    "preferred_training_times": ["evening"]
  },
  "equipment": {
    "has_gym_membership": true,
    "available_equipment": [
      "barbell", "dumbbells", "pull_up_bar",
      "boxing_gloves", "heavy_bag"
    ],
    "training_location": "gym"
  }
}
```

**Response (201 Created):**
```json
{
  "message": "Onboarding completed successfully",
  "user": {
    "id": 1,
    "full_name": "John Doe"
  },
  "profile": {
    "id": 1,
    "onboarding_completed": true,
    "profile_completion_percentage": 100,
    "experience_level": "intermediate",
    "primary_sport": "boxing",
    "fitness_goals": ["muscle_gain", "strength", "athletic_performance"]
  }
}
```

**Validation:**
- All required fields must be present
- Experience level must be: beginner/intermediate/advanced
- At least one fitness goal required
- Age must be 13-120 if provided
- Available days must be 1-7

---

### 6.3 Update Profile

#### PUT /api/profile
**Description**: Update user profile (partial updates allowed)
**Authentication**: None

**Request Body (any fields):**
```json
{
  "full_name": "John Doe Jr.",
  "age": 29,
  "weight_kg": 73,
  "available_days_per_week": 5,
  "fitness_goals": ["muscle_gain", "strength", "endurance"]
}
```

**Response (200 OK):**
```json
{
  "message": "Profile updated successfully",
  "profile": {
    "id": 1,
    "age": 29,
    "weight_kg": 73,
    "available_days_per_week": 5,
    "fitness_goals": ["muscle_gain", "strength", "endurance"],
    "updated_at": "2024-01-20T15:30:00Z"
  }
}
```

---

### 6.4 Update Goals

#### PATCH /api/profile/goals
**Description**: Update fitness goals specifically
**Authentication**: None

**Request Body:**
```json
{
  "fitness_goals": ["weight_loss", "general_fitness"]
}
```

**Response (200 OK):**
```json
{
  "message": "Goals updated successfully",
  "goals": ["weight_loss", "general_fitness"]
}
```

---

### 6.5 Reset Profile (Testing)

#### DELETE /api/profile
**Description**: Delete profile and reset to onboarding (useful for testing)
**Authentication**: None

**Response (200 OK):**
```json
{
  "message": "Profile reset successfully. Complete onboarding to create new profile."
}
```

---

## 7. Pydantic Schemas

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Personal Info
class PersonalInfo(BaseModel):
    age: Optional[int] = Field(None, ge=13, le=120)
    gender: Optional[str] = None
    height_cm: Optional[float] = Field(None, gt=0)
    weight_kg: Optional[float] = Field(None, gt=0)

# Fitness Background
class FitnessBackground(BaseModel):
    experience_level: str = Field(
        pattern="^(beginner|intermediate|advanced)$"
    )
    primary_sport: str
    secondary_sports: Optional[List[str]] = []
    years_training: Optional[int] = Field(None, ge=0)

# Limitations
class Limitations(BaseModel):
    injuries: Optional[List[str]] = []
    health_conditions: Optional[List[str]] = []
    medications: Optional[List[str]] = []

# Availability
class Availability(BaseModel):
    available_days_per_week: int = Field(ge=1, le=7)
    preferred_session_duration: int = Field(ge=15, le=180)
    preferred_training_times: List[str] = []

# Equipment
class Equipment(BaseModel):
    has_gym_membership: bool
    available_equipment: List[str]
    training_location: str

# Onboarding Request
class OnboardingRequest(BaseModel):
    full_name: str = Field(min_length=1)
    personal_info: PersonalInfo
    fitness_background: FitnessBackground
    goals: List[str] = Field(min_items=1)
    limitations: Limitations
    availability: Availability
    equipment: Equipment

# Profile Update (all optional)
class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    available_days_per_week: Optional[int] = None
    fitness_goals: Optional[List[str]] = None

# Goals Update
class GoalsUpdate(BaseModel):
    fitness_goals: List[str] = Field(min_items=1)

# Response Schemas
class UserResponse(BaseModel):
    id: int
    full_name: str

class ProfileResponse(BaseModel):
    id: int
    age: Optional[int]
    gender: Optional[str]
    experience_level: Optional[str]
    primary_sport: Optional[str]
    fitness_goals: List[str]
    injuries: List[str]
    onboarding_completed: bool
    profile_completion_percentage: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProfileWithUser(BaseModel):
    user: UserResponse
    profile: Optional[ProfileResponse]
    message: Optional[str] = None
```

---

## 8. Implementation Steps

### Step 1: Create Database Models (30 min)
```bash
# Files to create/modify
backend/app/models/user.py          # User model
backend/app/models/user_profile.py  # UserProfile model
backend/app/database/connection.py  # Add models to Base
```

### Step 2: Create Pydantic Schemas (20 min)
```bash
backend/app/schemas/profile.py  # All profile schemas
```

### Step 3: Create CRUD Operations (30 min)
```bash
backend/app/crud/user.py     # Get/create default user
backend/app/crud/profile.py  # Profile CRUD operations
```

### Step 4: Create Helper Functions (20 min)
```bash
backend/app/utils/profile.py  # Profile completion calculation, etc.
```

### Step 5: Create API Endpoints (45 min)
```bash
backend/app/api/profile.py  # All profile endpoints
```

### Step 6: Update Main App (15 min)
```bash
backend/app/main.py  # Include profile router
```

### Step 7: Create Startup Function (15 min)
```python
# In app/main.py startup event
@app.on_event("startup")
async def startup_event():
    # ... existing code ...

    # Ensure default user exists
    from app.crud.user import ensure_default_user
    ensure_default_user()
```

### Step 8: Update AI Chat Endpoint (30 min)
```python
# Modify /ai/chat to use profile context
@app.get("/ai/chat")
async def ai_chat(q: str, sport: Optional[str] = None):
    # Get user profile
    profile = get_user_profile()

    if profile and profile.onboarding_completed:
        user_context = build_user_context(profile)
        response = generate_with_rag(
            query=q,
            sport=sport or profile.primary_sport,
            user_context=user_context
        )
    else:
        # No profile - use general response
        response = generate_with_rag(query=q, sport=sport)

    return {
        "query": q,
        "response": response,
        "personalized": bool(profile and profile.onboarding_completed)
    }
```

### Step 9: Testing (45 min)
- Test onboarding submission
- Test profile retrieval
- Test profile updates
- Test AI chat with/without profile
- Test profile reset

### Step 10: Documentation (15 min)
- Update API docs
- Add usage examples

**Total Estimated Time**: 4-5 hours

---

## 9. Helper Functions

### Profile Completion Calculator

```python
# app/utils/profile.py

def calculate_profile_completion(profile: UserProfile) -> int:
    """Calculate profile completion percentage."""
    total_fields = 0
    filled_fields = 0

    # Required fields (worth more)
    required = [
        (profile.experience_level, 15),
        (profile.primary_sport, 15),
        (profile.fitness_goals and len(profile.fitness_goals) > 0, 20),
        (profile.available_days_per_week, 10),
        (profile.preferred_session_duration, 10),
    ]

    # Optional fields
    optional = [
        (profile.age, 5),
        (profile.gender, 5),
        (profile.height_cm, 3),
        (profile.weight_kg, 3),
        (profile.years_training, 3),
        (profile.secondary_sports and len(profile.secondary_sports) > 0, 3),
        (profile.injuries and len(profile.injuries) > 0, 3),
        (profile.has_gym_membership is not None, 5),
        (profile.available_equipment and len(profile.available_equipment) > 0, 5),
        (profile.training_location, 5),
    ]

    all_fields = required + optional

    for field_value, weight in all_fields:
        total_fields += weight
        if field_value:
            filled_fields += weight

    return int((filled_fields / total_fields) * 100)


def build_user_context(profile: UserProfile, user: User) -> str:
    """Build user context string for AI prompts."""
    context_parts = [
        f"User Profile for {user.full_name}:",
        f"- Experience Level: {profile.experience_level}",
        f"- Primary Sport: {profile.primary_sport}",
    ]

    if profile.fitness_goals:
        goals_str = ", ".join(profile.fitness_goals)
        context_parts.append(f"- Fitness Goals: {goals_str}")

    if profile.injuries:
        injuries_str = ", ".join(profile.injuries)
        context_parts.append(f"- Injuries/Limitations: {injuries_str}")

    if profile.available_days_per_week:
        context_parts.append(
            f"- Training Availability: {profile.available_days_per_week} days/week"
        )

    if profile.age:
        context_parts.append(f"- Age: {profile.age}")

    return "\n".join(context_parts)
```

---

## 10. Example Usage Flow

### First Time User

```bash
# 1. Check if profile exists
curl http://localhost:8000/api/profile

# Response: { "user": {...}, "profile": null, "message": "..." }

# 2. Complete onboarding
curl -X POST http://localhost:8000/api/profile/onboarding \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "personal_info": {
      "age": 28,
      "gender": "male"
    },
    "fitness_background": {
      "experience_level": "intermediate",
      "primary_sport": "boxing"
    },
    "goals": ["muscle_gain", "strength"],
    "limitations": {
      "injuries": ["knee_injury"]
    },
    "availability": {
      "available_days_per_week": 4,
      "preferred_session_duration": 60,
      "preferred_training_times": ["evening"]
    },
    "equipment": {
      "has_gym_membership": true,
      "available_equipment": ["dumbbells", "barbell"],
      "training_location": "gym"
    }
  }'

# 3. Now AI chat is personalized
curl "http://localhost:8000/ai/chat?q=should+I+increase+squat+weight"

# Response includes personalized advice based on profile!
```

### Returning User

```bash
# 1. Get current profile
curl http://localhost:8000/api/profile

# 2. Update weight
curl -X PUT http://localhost:8000/api/profile \
  -H "Content-Type: application/json" \
  -d '{"weight_kg": 73}'

# 3. Update goals
curl -X PATCH http://localhost:8000/api/profile/goals \
  -H "Content-Type: application/json" \
  -d '{"fitness_goals": ["strength", "endurance"]}'
```

---

## 11. Testing Strategy

### Manual Tests

**Test 1: First Time Onboarding**
```bash
# Should return no profile
curl http://localhost:8000/api/profile

# Submit onboarding
curl -X POST http://localhost:8000/api/profile/onboarding \
  -H "Content-Type: application/json" \
  -d @test_onboarding.json

# Should now return profile
curl http://localhost:8000/api/profile
```

**Test 2: Profile Updates**
```bash
# Update profile
curl -X PUT http://localhost:8000/api/profile \
  -H "Content-Type: application/json" \
  -d '{"age": 29, "weight_kg": 72}'

# Verify update
curl http://localhost:8000/api/profile
```

**Test 3: Personalized AI**
```bash
# Before onboarding (generic response)
curl "http://localhost:8000/ai/chat?q=training+advice"

# After onboarding (personalized response)
curl -X POST http://localhost:8000/api/profile/onboarding -d @onboarding.json
curl "http://localhost:8000/ai/chat?q=training+advice"
```

**Test 4: Profile Reset**
```bash
# Reset profile
curl -X DELETE http://localhost:8000/api/profile

# Should return no profile again
curl http://localhost:8000/api/profile
```

### Unit Tests

```python
# tests/test_profile.py

def test_onboarding_creates_profile(client):
    """Test onboarding creates profile."""
    response = client.post("/api/profile/onboarding", json={
        "full_name": "Test User",
        "personal_info": {"age": 25},
        "fitness_background": {
            "experience_level": "beginner",
            "primary_sport": "gym"
        },
        "goals": ["muscle_gain"],
        "limitations": {"injuries": []},
        "availability": {
            "available_days_per_week": 3,
            "preferred_session_duration": 45,
            "preferred_training_times": ["morning"]
        },
        "equipment": {
            "has_gym_membership": False,
            "available_equipment": ["dumbbells"],
            "training_location": "home"
        }
    })

    assert response.status_code == 201
    data = response.json()
    assert data["profile"]["onboarding_completed"] == True
    assert data["user"]["full_name"] == "Test User"

def test_get_profile_without_onboarding(client):
    """Test getting profile before onboarding."""
    response = client.get("/api/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["profile"] is None

def test_update_profile(client, completed_onboarding):
    """Test updating profile."""
    response = client.put("/api/profile", json={
        "age": 30,
        "weight_kg": 75
    })
    assert response.status_code == 200
    data = response.json()
    assert data["profile"]["age"] == 30
```

---

## 12. Integration with AI Chat

### Updated generate_with_rag Function

```python
# app/ai/gemini.py

def generate_with_rag(
    query: str,
    sport: Optional[str] = None,
    top_k: int = 3,
    user_context: Optional[str] = None  # NEW parameter
) -> str:
    """Generate AI response enhanced with RAG context and user profile."""

    # Step 1: Query RAG system
    rag_results = query_knowledge(query=query, sport=sport, top_k=top_k)
    context = format_context_for_llm(rag_results)

    # Step 2: Build prompt with optional user context
    sport_context = f" specializing in {sport}" if sport else ""

    # Include user context if available
    if user_context:
        prompt = f"""You are CoachX, an expert personal training assistant{sport_context}.

{user_context}

CONTEXT FROM KNOWLEDGE BASE:
{context}

USER QUESTION:
{query}

Provide personalized advice considering the user's profile, experience level,
goals, limitations, and available training time. Reference their specific
situation when relevant. Always prioritize safety and proper technique.
Keep your response clear, concise, and actionable."""
    else:
        # Fallback to general prompt (no profile)
        prompt = f"""You are CoachX, an expert personal training assistant{sport_context}.

CONTEXT FROM KNOWLEDGE BASE:
{context}

USER QUESTION:
{query}

Provide accurate, helpful, and motivating training advice based on the context above.
Always prioritize safety and proper technique.
Keep your response clear, concise, and actionable."""

    # Step 3: Generate response
    response = generate_response(prompt)
    return response
```

---

## 13. Success Criteria

### Functionality
- ✅ User can complete onboarding and profile is saved
- ✅ Profile persists across server restarts
- ✅ User can view their profile
- ✅ User can update profile fields
- ✅ AI chat uses profile context when available
- ✅ Profile completion percentage calculates correctly

### Quality
- ✅ Input validation prevents invalid data
- ✅ Proper error messages for all failure cases
- ✅ Profile updates are atomic (all or nothing)

### Performance
- ✅ Profile retrieval < 100ms
- ✅ Onboarding submission < 500ms
- ✅ Profile updates < 200ms

### User Experience
- ✅ Clear response messages
- ✅ Personalized AI responses reference user context
- ✅ Profile reset works for testing

---

## 14. Migration to Multi-User (Post-MVP)

When ready to add authentication, the migration path is:

1. Add authentication tables (users become multi-row)
2. Add JWT token generation/validation
3. Add login/register endpoints
4. Add authentication middleware
5. Modify endpoints to use `current_user` dependency
6. Remove user_id=1 constraint
7. Add user_id to all queries

**Key advantage of this approach**: The UserProfile model and onboarding logic remain unchanged. We just add authentication on top.

---

## 15. File Structure

```
backend/
├── app/
│   ├── models/
│   │   ├── user.py              # NEW
│   │   └── user_profile.py      # NEW
│   ├── schemas/
│   │   └── profile.py           # NEW
│   ├── crud/
│   │   ├── user.py              # NEW
│   │   └── profile.py           # NEW
│   ├── api/
│   │   └── profile.py           # NEW
│   ├── utils/
│   │   └── profile.py           # NEW
│   ├── ai/
│   │   └── gemini.py            # MODIFIED (add user_context)
│   └── main.py                  # MODIFIED (add router, startup)
└── tests/
    └── test_profile.py          # NEW
```

---

## 16. Dependencies

No new dependencies needed! We already have:
- ✅ SQLAlchemy (database ORM)
- ✅ Pydantic (validation)
- ✅ FastAPI (API framework)

---

**PRP Version**: 2.0 (MVP - Single User)
**Last Updated**: 2024-12-02
**Ready to Implement**: Yes ✅
