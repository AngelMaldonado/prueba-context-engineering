# PRP: User Onboarding & Profiles - CoachX

**Feature**: User Onboarding & Profiles
**Status**: Planning
**Priority**: High
**Estimated Complexity**: Medium-High

---

## 1. Objective

Implement a complete user management system with onboarding flow to capture user preferences, fitness goals, experience level, and limitations. This enables personalized training recommendations and progress tracking.

**Key Goals:**
- Create user accounts with authentication
- Capture essential onboarding data
- Store user profiles with fitness-related information
- Enable profile updates and management
- Provide foundation for personalized AI coaching

---

## 2. Current State

### What We Have ✅
- SQLAlchemy configured with SQLite
- FastAPI backend structure
- RAG system with general training knowledge
- Gemini AI integration for responses

### What's Missing ❌
- User models and authentication
- Onboarding endpoints
- Profile storage and retrieval
- User context in AI responses

---

## 3. Requirements

### 3.1 Functional Requirements

**User Registration & Authentication:**
- Users can create accounts with email/password
- JWT-based authentication for API requests
- Secure password hashing
- Login/logout functionality

**Onboarding Flow:**
- Multi-step onboarding process
- Capture personal information (name, age, gender)
- Capture fitness background (experience level, primary sport)
- Capture goals (weight loss, muscle gain, endurance, etc.)
- Capture limitations (injuries, health conditions)
- Capture availability (days per week, session duration)
- Capture preferences (equipment access, gym membership)

**Profile Management:**
- View user profile
- Update profile information
- Update fitness goals
- Track profile completion status

### 3.2 Technical Requirements

**Database Models:**
- `User`: Core user authentication data
- `UserProfile`: Detailed fitness and preference data
- Proper relationships and constraints
- Timestamps for created/updated tracking

**API Endpoints:**
- `POST /auth/register` - Create new user
- `POST /auth/login` - Authenticate user
- `GET /auth/me` - Get current user
- `POST /onboarding` - Submit onboarding data
- `GET /profile` - Get user profile
- `PUT /profile` - Update user profile
- `PATCH /profile/goals` - Update fitness goals

**Security:**
- Password hashing with bcrypt
- JWT token generation and validation
- Protected endpoints (authentication required)
- Input validation with Pydantic

---

## 4. Database Schema

### 4.1 User Model

```python
class User(Base):
    """Core user authentication and identification."""
    __tablename__ = "users"

    id: int (PK, autoincrement)
    email: str (unique, indexed, not null)
    hashed_password: str (not null)
    full_name: str (not null)
    is_active: bool (default=True)
    is_superuser: bool (default=False)
    created_at: datetime (default=now)
    updated_at: datetime (default=now, onupdate=now)

    # Relationships
    profile: UserProfile (one-to-one)
    training_plans: List[TrainingPlan] (one-to-many)
    workout_sessions: List[WorkoutSession] (one-to-many)
```

### 4.2 UserProfile Model

```python
class UserProfile(Base):
    """Detailed user fitness profile from onboarding."""
    __tablename__ = "user_profiles"

    id: int (PK, autoincrement)
    user_id: int (FK -> users.id, unique, not null)

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

    # Goals (JSON array of goal types)
    fitness_goals: JSON ([
        "weight_loss", "muscle_gain", "strength",
        "endurance", "flexibility", "athletic_performance",
        "general_fitness", "stress_relief"
    ])

    # Limitations & Health
    injuries: JSON (list of current/past injuries)
    health_conditions: JSON (list of conditions to consider)
    medications: JSON (optional, affects training)

    # Availability & Preferences
    available_days_per_week: int (1-7)
    preferred_session_duration: int (minutes: 30/45/60/90)
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
    created_at: datetime (default=now)
    updated_at: datetime (default=now, onupdate=now)

    # Relationships
    user: User (many-to-one)
```

### 4.3 Indexes and Constraints

```sql
-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Unique Constraints
ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE(email);
ALTER TABLE user_profiles ADD CONSTRAINT unique_user_id UNIQUE(user_id);

-- Foreign Keys
ALTER TABLE user_profiles
  ADD CONSTRAINT fk_user_profile_user
  FOREIGN KEY (user_id) REFERENCES users(id)
  ON DELETE CASCADE;
```

---

## 5. API Endpoints Specification

### 5.1 Authentication Endpoints

#### POST /api/auth/register
**Description**: Register a new user
**Authentication**: None (public)

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Validation:**
- Email must be valid format
- Password minimum 8 characters
- Email must be unique (not already registered)

---

#### POST /api/auth/login
**Description**: Authenticate user and get access token
**Authentication**: None (public)

**Request Body (Form Data):**
```
username: user@example.com
password: SecurePass123!
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe"
  }
}
```

**Errors:**
- 401 Unauthorized: Invalid credentials

---

#### GET /api/auth/me
**Description**: Get current authenticated user
**Authentication**: Required (JWT)

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "profile": {
    "onboarding_completed": true,
    "profile_completion_percentage": 85,
    "primary_sport": "boxing",
    "experience_level": "intermediate"
  }
}
```

---

### 5.2 Onboarding Endpoints

#### POST /api/onboarding
**Description**: Submit complete onboarding data
**Authentication**: Required (JWT)

**Request Body:**
```json
{
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
  "profile": {
    "id": 1,
    "user_id": 1,
    "onboarding_completed": true,
    "profile_completion_percentage": 100,
    "experience_level": "intermediate",
    "primary_sport": "boxing",
    "fitness_goals": ["muscle_gain", "strength", "athletic_performance"],
    "created_at": "2024-01-15T11:00:00Z"
  }
}
```

**Validation:**
- All required fields must be present
- Enums must match allowed values
- Age must be 13-120
- Weight/height must be positive numbers

---

### 5.3 Profile Management Endpoints

#### GET /api/profile
**Description**: Get current user's profile
**Authentication**: Required (JWT)

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "age": 28,
  "gender": "male",
  "height_cm": 175,
  "weight_kg": 75,
  "experience_level": "intermediate",
  "primary_sport": "boxing",
  "secondary_sports": ["running", "gym"],
  "fitness_goals": ["muscle_gain", "strength", "athletic_performance"],
  "injuries": ["previous_knee_injury"],
  "available_days_per_week": 4,
  "preferred_session_duration": 60,
  "has_gym_membership": true,
  "onboarding_completed": true,
  "profile_completion_percentage": 100,
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

---

#### PUT /api/profile
**Description**: Update user profile
**Authentication**: Required (JWT)

**Request Body (partial updates allowed):**
```json
{
  "weight_kg": 73,
  "available_days_per_week": 5,
  "fitness_goals": ["muscle_gain", "strength", "endurance"]
}
```

**Response (200 OK):**
```json
{
  "message": "Profile updated successfully",
  "profile": { /* updated profile object */ }
}
```

---

#### PATCH /api/profile/goals
**Description**: Update fitness goals specifically
**Authentication**: Required (JWT)

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

## 6. Pydantic Schemas

### 6.1 Request Schemas

```python
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1)

class UserLogin(BaseModel):
    username: EmailStr  # OAuth2 spec uses 'username'
    password: str

# Onboarding Schemas
class PersonalInfo(BaseModel):
    age: Optional[int] = Field(None, ge=13, le=120)
    gender: Optional[str] = Field(None, pattern="^(male|female|other|prefer_not_to_say)$")
    height_cm: Optional[float] = Field(None, gt=0)
    weight_kg: Optional[float] = Field(None, gt=0)

class FitnessBackground(BaseModel):
    experience_level: str = Field(pattern="^(beginner|intermediate|advanced)$")
    primary_sport: str
    secondary_sports: Optional[List[str]] = []
    years_training: Optional[int] = Field(None, ge=0)

class Limitations(BaseModel):
    injuries: Optional[List[str]] = []
    health_conditions: Optional[List[str]] = []
    medications: Optional[List[str]] = []

class Availability(BaseModel):
    available_days_per_week: int = Field(ge=1, le=7)
    preferred_session_duration: int = Field(ge=15, le=180)
    preferred_training_times: List[str]

class Equipment(BaseModel):
    has_gym_membership: bool
    available_equipment: List[str]
    training_location: str

class OnboardingRequest(BaseModel):
    personal_info: PersonalInfo
    fitness_background: FitnessBackground
    goals: List[str] = Field(min_items=1)
    limitations: Limitations
    availability: Availability
    equipment: Equipment

# Profile Update Schemas
class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    available_days_per_week: Optional[int] = None
    fitness_goals: Optional[List[str]] = None
    # ... other optional fields

class GoalsUpdate(BaseModel):
    fitness_goals: List[str] = Field(min_items=1)
```

### 6.2 Response Schemas

```python
class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ProfileSummary(BaseModel):
    onboarding_completed: bool
    profile_completion_percentage: int
    primary_sport: Optional[str]
    experience_level: Optional[str]

class UserWithProfile(UserResponse):
    profile: Optional[ProfileSummary]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    age: Optional[int]
    gender: Optional[str]
    experience_level: Optional[str]
    primary_sport: Optional[str]
    fitness_goals: List[str]
    onboarding_completed: bool
    profile_completion_percentage: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

---

## 7. Authentication Implementation

### 7.1 JWT Configuration

```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Settings
SECRET_KEY = "your-secret-key-change-in-production"  # Load from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

### 7.2 Authentication Dependency

```python
# app/core/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user (additional check)."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

---

## 8. Implementation Steps

### Step 1: Install Dependencies
```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

Add to `requirements.txt`:
```
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

### Step 2: Create Database Models
- Create `app/models/user.py` with User model
- Create `app/models/user_profile.py` with UserProfile model
- Update `app/database/connection.py` to import models

### Step 3: Create Pydantic Schemas
- Create `app/schemas/user.py` with user schemas
- Create `app/schemas/auth.py` with authentication schemas
- Create `app/schemas/profile.py` with profile schemas

### Step 4: Implement Security Module
- Create `app/core/security.py` with JWT and password functions
- Create `app/core/dependencies.py` with auth dependencies
- Update `app/config.py` with JWT settings

### Step 5: Create CRUD Operations
- Create `app/crud/user.py` with user CRUD operations
- Create `app/crud/profile.py` with profile CRUD operations

### Step 6: Implement API Routes
- Create `app/api/auth.py` with authentication endpoints
- Create `app/api/onboarding.py` with onboarding endpoint
- Create `app/api/profile.py` with profile management endpoints

### Step 7: Update Main App
- Include new routers in `app/main.py`
- Add CORS configuration for authentication
- Update startup events if needed

### Step 8: Create Database Migration
- Run migration to create new tables
- Verify schema with SQLite browser

### Step 9: Testing
- Test user registration
- Test login and token generation
- Test protected endpoints
- Test onboarding flow
- Test profile updates

### Step 10: Documentation
- Update API documentation
- Create user flow diagrams
- Document authentication process

---

## 9. Testing Strategy

### 9.1 Unit Tests

```python
# tests/test_auth.py
def test_create_user(client):
    """Test user registration."""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "TestPass123!",
        "full_name": "Test User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "access_token" in data

def test_login_user(client):
    """Test user login."""
    # First create user
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "TestPass123!",
        "full_name": "Test User"
    })

    # Then login
    response = client.post("/api/auth/login", data={
        "username": "test@example.com",
        "password": "TestPass123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_get_current_user(client, auth_headers):
    """Test getting current user."""
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data

def test_onboarding(client, auth_headers):
    """Test onboarding submission."""
    onboarding_data = {
        "personal_info": {
            "age": 28,
            "gender": "male",
            "height_cm": 175,
            "weight_kg": 75
        },
        "fitness_background": {
            "experience_level": "intermediate",
            "primary_sport": "boxing"
        },
        "goals": ["muscle_gain", "strength"],
        "limitations": {
            "injuries": []
        },
        "availability": {
            "available_days_per_week": 4,
            "preferred_session_duration": 60,
            "preferred_training_times": ["evening"]
        },
        "equipment": {
            "has_gym_membership": true,
            "available_equipment": ["dumbbells"],
            "training_location": "gym"
        }
    }

    response = client.post("/api/onboarding",
                          json=onboarding_data,
                          headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["profile"]["onboarding_completed"] == True
```

### 9.2 Manual Testing Checklist

- [ ] User can register with valid email/password
- [ ] User cannot register with duplicate email
- [ ] User can login with correct credentials
- [ ] User cannot login with incorrect credentials
- [ ] JWT token is generated on successful login
- [ ] Protected endpoints require authentication
- [ ] Invalid tokens are rejected
- [ ] User can complete onboarding
- [ ] Profile is created after onboarding
- [ ] User can view their profile
- [ ] User can update profile information
- [ ] User can update fitness goals
- [ ] Profile completion percentage calculates correctly

---

## 10. Success Criteria

### Functionality
- ✅ Users can register and login
- ✅ JWT authentication works for all protected endpoints
- ✅ Onboarding flow captures all required data
- ✅ User profiles are stored correctly in database
- ✅ Profile updates work as expected

### Quality
- ✅ All unit tests pass
- ✅ Password security (bcrypt hashing)
- ✅ Input validation prevents invalid data
- ✅ Proper error messages for all failure cases

### Performance
- ✅ Login response < 500ms
- ✅ Profile retrieval < 200ms
- ✅ Onboarding submission < 1s

### Documentation
- ✅ API endpoints documented in OpenAPI
- ✅ Authentication flow documented
- ✅ User model schema documented

---

## 11. Future Enhancements

**Phase 2 Improvements:**
- Email verification on registration
- Password reset functionality
- Social authentication (Google, Facebook)
- Profile pictures upload
- Privacy settings
- Account deletion

**Advanced Features:**
- Multi-factor authentication (2FA)
- Session management (multiple devices)
- Activity logging (login history)
- User preferences (notifications, language)

---

## 12. Security Considerations

### Must Have
- ✅ Password hashing (never store plain text)
- ✅ JWT token expiration
- ✅ HTTPS in production (SSL/TLS)
- ✅ Input validation and sanitization
- ✅ SQL injection prevention (SQLAlchemy ORM)

### Should Have
- Email verification before account activation
- Rate limiting on authentication endpoints
- Password complexity requirements
- Token refresh mechanism
- CORS configuration for specific origins

### Nice to Have
- Two-factor authentication (2FA)
- Audit logging for sensitive actions
- IP-based rate limiting
- Suspicious activity detection

---

## 13. Database Migration Script

```sql
-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    is_superuser BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create user_profiles table
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    age INTEGER,
    gender VARCHAR(50),
    height_cm REAL,
    weight_kg REAL,
    experience_level VARCHAR(50),
    primary_sport VARCHAR(100),
    secondary_sports TEXT,  -- JSON
    years_training INTEGER,
    fitness_goals TEXT,  -- JSON
    injuries TEXT,  -- JSON
    health_conditions TEXT,  -- JSON
    medications TEXT,  -- JSON
    available_days_per_week INTEGER,
    preferred_session_duration INTEGER,
    preferred_training_times TEXT,  -- JSON
    has_gym_membership BOOLEAN,
    available_equipment TEXT,  -- JSON
    training_location VARCHAR(50),
    onboarding_completed BOOLEAN DEFAULT 0,
    onboarding_completed_at TIMESTAMP,
    profile_completion_percentage INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_users_created_at ON users(created_at);
```

---

## 14. Integration with Existing Features

### AI Chat Integration
Once users are authenticated, enhance the `/ai/chat` endpoint:

```python
@app.get("/ai/chat")
async def ai_chat(
    q: str,
    sport: Optional[str] = None,
    top_k: int = 3,
    current_user: User = Depends(get_current_user)  # Add authentication
) -> dict:
    """AI chat endpoint with user context."""

    # Load user profile
    profile = current_user.profile

    if profile and profile.onboarding_completed:
        # Use personalized context
        user_context = f"""
        User Profile:
        - Name: {current_user.full_name}
        - Experience: {profile.experience_level}
        - Primary Sport: {profile.primary_sport}
        - Goals: {', '.join(profile.fitness_goals)}
        - Injuries: {', '.join(profile.injuries)}
        """
    else:
        user_context = "New user without profile."

    # Generate RAG-enhanced response with user context
    response_text = generate_with_rag(
        query=q,
        sport=sport or profile.primary_sport,
        top_k=top_k,
        user_context=user_context  # New parameter
    )

    return {
        "query": q,
        "sport": sport,
        "response": response_text,
        "personalized": profile.onboarding_completed if profile else False
    }
```

---

## 15. Notes

**Design Decisions:**
- Using JWT for stateless authentication (scalable)
- Single onboarding endpoint vs. multi-step (simplified UX)
- JSON fields for flexible data (injuries, goals, equipment)
- Profile completion percentage for UX prompts

**Potential Challenges:**
- Password reset flow (requires email service)
- Token refresh strategy (consider adding refresh tokens)
- Profile validation complexity (many optional fields)

**Dependencies:**
- Frontend will need to implement onboarding UI
- Email service for verification (future)
- Consider adding profile completion prompts in UI

---

**PRP Version**: 1.0
**Last Updated**: 2024-12-02
**Author**: CoachX Development Team
