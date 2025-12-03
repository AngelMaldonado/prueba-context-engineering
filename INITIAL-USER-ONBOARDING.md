# User Onboarding & Profiles - Implementation Guide

**Feature**: User Authentication and Personalized Profiles
**Status**: Ready for Implementation
**Complexity**: Medium-High
**Estimated Time**: 6-8 hours

---

## What This Feature Enables

This feature transforms CoachX from a general training assistant into a **personalized AI coach** by:

1. **User Accounts**: Secure authentication with email/password
2. **Onboarding Flow**: Capturing fitness background, goals, and limitations
3. **Profile Management**: Storing and updating user preferences
4. **Personalization Foundation**: Enabling AI responses tailored to each user

---

## The Big Picture

### Before (Current State)
```
User → Ask Question → AI → General Response
```

**Example:**
- Question: "Should I increase my squat weight?"
- Response: Generic advice about progression

### After (With User Profiles)
```
User → Authenticate → Ask Question → AI + User Context → Personalized Response
```

**Example:**
- Question: "Should I increase my squat weight?"
- AI knows:
  - Your experience level (intermediate)
  - Your goal (muscle gain)
  - Your limitation (previous knee injury)
  - Your last 3 squat sessions
- Response: "Based on your intermediate level and your last 3 sessions where you completed 3x10 at 100kg comfortably, yes - but increase to 105kg (5% increment) and monitor your knee. Given your injury history, if you feel any discomfort, stay at 100kg for another week."

---

## Key Components

### 1. Authentication System

**Technology Stack:**
- **JWT Tokens**: Secure, stateless authentication
- **Bcrypt**: Password hashing (never store plain text)
- **OAuth2**: Industry-standard security pattern

**User Flow:**
```
1. User registers → Email + Password → Account created
2. User logs in → Credentials verified → JWT token issued
3. User makes requests → JWT token validated → Access granted
```

### 2. User Database Models

**User Table:**
```
users
├── id (PK)
├── email (unique)
├── hashed_password
├── full_name
├── is_active
└── created_at
```

**User Profile Table:**
```
user_profiles
├── id (PK)
├── user_id (FK → users)
│
├── Personal Info
│   ├── age, gender, height, weight
│
├── Fitness Background
│   ├── experience_level (beginner/intermediate/advanced)
│   ├── primary_sport (boxing/crossfit/gym/etc.)
│   └── years_training
│
├── Goals (JSON array)
│   └── [weight_loss, muscle_gain, strength, endurance, ...]
│
├── Limitations (JSON)
│   ├── injuries
│   ├── health_conditions
│   └── medications
│
├── Availability
│   ├── available_days_per_week
│   ├── preferred_session_duration
│   └── preferred_training_times
│
└── Equipment & Access
    ├── has_gym_membership
    ├── available_equipment (JSON array)
    └── training_location
```

### 3. Onboarding Flow

**Step-by-Step Process:**

```
┌─────────────────────────────────────────┐
│  Step 1: Account Creation               │
│  - Email, password, full name           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Step 2: Personal Information           │
│  - Age, gender, height, weight          │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Step 3: Fitness Background             │
│  - Experience level                     │
│  - Primary sport                        │
│  - Years of training                    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Step 4: Goals Selection                │
│  - Weight loss                          │
│  - Muscle gain                          │
│  - Strength, endurance, etc.            │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Step 5: Limitations & Health           │
│  - Current/past injuries                │
│  - Health conditions                    │
│  - Medications                          │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Step 6: Availability & Preferences     │
│  - Days per week available              │
│  - Session duration preference          │
│  - Preferred training times             │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Step 7: Equipment & Access             │
│  - Gym membership status                │
│  - Available equipment                  │
│  - Training location                    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  ✓ Profile Complete!                    │
│  Ready for personalized training        │
└─────────────────────────────────────────┘
```

---

## API Endpoints

### Authentication
```http
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

### Onboarding
```http
POST /api/onboarding
```

### Profile Management
```http
GET   /api/profile
PUT   /api/profile
PATCH /api/profile/goals
```

---

## Example Usage

### 1. Register a User

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

**Response:**
```json
{
  "id": 1,
  "email": "john@example.com",
  "full_name": "John Doe",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### 2. Login

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=SecurePass123!"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "full_name": "John Doe"
  }
}
```

### 3. Complete Onboarding

**Request:**
```bash
curl -X POST http://localhost:8000/api/onboarding \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{
    "personal_info": {
      "age": 28,
      "gender": "male",
      "height_cm": 175,
      "weight_kg": 75
    },
    "fitness_background": {
      "experience_level": "intermediate",
      "primary_sport": "boxing",
      "years_training": 3
    },
    "goals": ["muscle_gain", "strength"],
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
      "available_equipment": ["barbell", "dumbbells", "boxing_gloves"],
      "training_location": "gym"
    }
  }'
```

**Response:**
```json
{
  "message": "Onboarding completed successfully",
  "profile": {
    "id": 1,
    "user_id": 1,
    "onboarding_completed": true,
    "profile_completion_percentage": 100,
    "experience_level": "intermediate",
    "primary_sport": "boxing"
  }
}
```

### 4. Get User Profile

**Request:**
```bash
curl -X GET http://localhost:8000/api/profile \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "age": 28,
  "gender": "male",
  "experience_level": "intermediate",
  "primary_sport": "boxing",
  "fitness_goals": ["muscle_gain", "strength"],
  "injuries": ["previous_knee_injury"],
  "available_days_per_week": 4,
  "onboarding_completed": true,
  "profile_completion_percentage": 100
}
```

---

## How This Integrates with Existing Features

### Enhanced AI Chat

**Before:**
```python
# General response
response = generate_with_rag(query="How to improve jab?", sport="boxing")
```

**After:**
```python
# Personalized response
user_context = {
    "name": "John",
    "experience": "intermediate",
    "goals": ["muscle_gain", "strength"],
    "injuries": ["previous_knee_injury"],
    "training_days": 4
}

response = generate_with_rag(
    query="How to improve jab?",
    sport="boxing",
    user_context=user_context  # NEW!
)
```

**Result:**
```
"Hi John! As an intermediate boxer working on muscle gain and strength
with 4 training days per week, let's focus on power development for
your jab. Given your knee injury history, we'll keep footwork simple..."
```

---

## Implementation Checklist

### Phase 1: Core Authentication
- [ ] Install dependencies (python-jose, passlib, python-multipart)
- [ ] Create User model
- [ ] Implement password hashing
- [ ] Create JWT token generation/validation
- [ ] Build registration endpoint
- [ ] Build login endpoint
- [ ] Create authentication dependency
- [ ] Test authentication flow

### Phase 2: User Profiles
- [ ] Create UserProfile model
- [ ] Design onboarding schema
- [ ] Build onboarding endpoint
- [ ] Create profile retrieval endpoint
- [ ] Create profile update endpoint
- [ ] Calculate profile completion percentage
- [ ] Test profile management

### Phase 3: Integration
- [ ] Update AI chat endpoint to use user context
- [ ] Modify RAG prompts to include user info
- [ ] Add authentication to existing endpoints
- [ ] Update API documentation
- [ ] Write integration tests

### Phase 4: Polish
- [ ] Add input validation
- [ ] Implement error handling
- [ ] Add logging for security events
- [ ] Performance testing
- [ ] Security audit

---

## Security Best Practices

### Implemented
✅ Password hashing with bcrypt (never store plain text)
✅ JWT tokens for stateless authentication
✅ Token expiration (7 days default)
✅ SQL injection prevention (SQLAlchemy ORM)
✅ Input validation with Pydantic

### Recommended for Production
- Use HTTPS/SSL in production
- Store SECRET_KEY in environment variables
- Implement rate limiting on auth endpoints
- Add email verification
- Consider refresh tokens for better security
- Add password complexity requirements
- Implement account lockout after failed attempts

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### User Profiles Table
```sql
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    age INTEGER,
    gender VARCHAR(50),
    experience_level VARCHAR(50),
    primary_sport VARCHAR(100),
    fitness_goals TEXT,  -- JSON array
    injuries TEXT,  -- JSON array
    available_days_per_week INTEGER,
    onboarding_completed BOOLEAN DEFAULT 0,
    profile_completion_percentage INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## Testing Plan

### Manual Testing

**Test 1: User Registration**
```bash
# Should succeed
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "Test123!", "full_name": "Test User"}'

# Should fail (duplicate email)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "Test123!", "full_name": "Test User"}'
```

**Test 2: Login**
```bash
# Should succeed
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@test.com&password=Test123!"

# Should fail (wrong password)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@test.com&password=WrongPassword"
```

**Test 3: Protected Endpoint**
```bash
# Should fail (no token)
curl -X GET http://localhost:8000/api/profile

# Should succeed (with token)
curl -X GET http://localhost:8000/api/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Automated Tests
- Unit tests for password hashing
- Unit tests for JWT creation/validation
- Integration tests for registration flow
- Integration tests for login flow
- Integration tests for onboarding
- Integration tests for profile updates

---

## Next Steps After Implementation

Once this feature is complete, you'll be able to:

1. **Create User Accounts** - Secure registration and login
2. **Capture User Preferences** - Through onboarding flow
3. **Store User Data** - In structured database
4. **Authenticate Requests** - Protect endpoints with JWT

### Enables Future Features:
- **Training Plan Generation** - Personalized to user's profile
- **Progress Tracking** - Track workouts and improvements
- **AI Chat History** - Store conversations per user
- **Personalized Recommendations** - Based on user context

---

## Common Questions

**Q: Why JWT instead of sessions?**
A: JWT is stateless, scalable, and works well with microservices and mobile apps. No need to maintain session storage.

**Q: How is the password stored?**
A: Passwords are hashed using bcrypt before storage. We never store plain text passwords. Even admins can't see user passwords.

**Q: What if a user forgets their password?**
A: Password reset flow will be added in a future enhancement (requires email service integration).

**Q: Can users update their profile later?**
A: Yes! The PUT /api/profile endpoint allows users to update any field after onboarding.

**Q: How long does the token last?**
A: Default is 7 days. This can be configured in settings.

---

## Resources

**Detailed Implementation Guide:**
- See `PRPs/user-onboarding-profiles.md` for complete specification

**Dependencies:**
```bash
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.6
```

**Useful Documentation:**
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- JWT: https://jwt.io/introduction
- Bcrypt: https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html

---

**Document Version**: 1.0
**Last Updated**: 2024-12-02
**Ready to Implement**: Yes ✅
