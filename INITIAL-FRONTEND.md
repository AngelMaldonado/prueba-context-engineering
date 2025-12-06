# INITIAL: Frontend Implementation for CoachX

## Context

The CoachX backend is **fully functional** with:
- ✅ FastAPI backend running on localhost:8000
- ✅ User profile & onboarding system (MVP single user)
- ✅ AI-powered workout plan generation with RAG
- ✅ Chat endpoint with personalized responses
- ✅ All API endpoints tested and working
- ✅ CORS configured for localhost:3000

**Now we need to build the frontend** that connects to this backend.

---

## What We're Building

A **minimal but functional** React frontend that:
1. Shows a home/landing page
2. Has an onboarding form to create user profile
3. Displays the generated workout plan
4. Basic chat interface (optional/stretch goal)

**NOT building:**
- Authentication (MVP = single user)
- Complex state management (keep it simple)
- Mobile app
- Advanced features

---

## Tech Stack Already Setup

**✅ Installed and Configured:**
- Vite 7.2.4 + React 19.2.0 + TypeScript
- Tailwind CSS 4.1.17 (configured)
- React Router DOM 7.10.0
- Axios 1.13.2
- Zustand 5.0.9 (for state if needed)

**✅ Folders Created:**
- `src/pages/` - Page components
- `src/components/` - Reusable components
- `src/lib/` - Utilities and API client
- `src/types/` - TypeScript types

**✅ Already Created:**
- `src/lib/api.ts` - Complete API client with all backend endpoints
- `tailwind.config.js` - Tailwind configuration with custom theme
- `postcss.config.js` - PostCSS configuration
- `.env` and `.env.example` - Environment variables

---

## What Needs to Be Built

### 1. Router Setup in App.tsx
- Configure React Router with routes:
  - `/` - HomePage (landing)
  - `/onboarding` - OnboardingPage
  - `/dashboard` - DashboardPage (shows workout plan)

### 2. HomePage (`src/pages/HomePage.tsx`)
- Simple landing page with:
  - Hero section explaining CoachX
  - Button to start onboarding
  - Connection status indicator (backend health check)
- Design: Clean, modern, Tailwind-based

### 3. OnboardingPage (`src/pages/OnboardingPage.tsx`)
- Multi-step form collecting user profile data
- Fields needed (from backend API):
  - **Basic Info**: name, age, gender, height, weight
  - **Experience**: experience_level (beginner/intermediate/advanced), primary_sport, years_training
  - **Goals**: fitness_goals (array: muscle_gain, weight_loss, strength, endurance, etc.)
  - **Limitations**: injuries, health_conditions (arrays)
  - **Availability**: available_days_per_week, preferred_session_duration, training_location
  - **Equipment**: has_gym_membership, available_equipment (array)

- Form behavior:
  - Multi-step (3-4 steps) for better UX
  - Validation per step
  - Progress indicator
  - Submit to `POST /api/profile/onboarding`
  - Redirect to `/dashboard` on success

### 4. DashboardPage (`src/pages/DashboardPage.tsx`)
- Show user profile summary
- Display active workout plan:
  - Fetch from `GET /api/workouts/active`
  - Show week-by-week structure
  - Each day shows: focus, warmup, exercises (name, sets, reps, rest, notes), cooldown
  - Duration per day
- Button to generate new plan:
  - Modal/form for duration_weeks and custom_notes
  - Call `POST /api/workouts/generate`
  - Show loading state (AI generation takes 10-30 seconds)
- (Stretch) Simple chat section:
  - Input for question
  - Call `GET /ai/chat?q=...&sport=...`
  - Display response

### 5. Components (as needed)
- `LoadingSpinner.tsx` - Reusable loading indicator
- `ErrorMessage.tsx` - Error display component
- (Optional) `WorkoutDayCard.tsx` - Display individual workout day
- (Optional) `ExerciseList.tsx` - Display exercises

---

## API Endpoints Available

All endpoints are in `src/lib/api.ts`:

```typescript
// Profile
api.profile.getStatus()
api.profile.getProfile()
api.profile.submitOnboarding(data)

// Workout Plans
api.workout.generatePlan({ duration_weeks, custom_notes })
api.workout.getActivePlan()
api.workout.getAllPlans()

// Chat
api.chat.sendMessage({ q, sport, top_k })

// Health
api.health.check()
```

---

## Design Guidelines

### Visual Style
- **Color Scheme**: Primary blue (already in Tailwind config as `primary-*`)
- **Typography**: System fonts, clean and readable
- **Layout**: Responsive, mobile-first
- **Components**: Use Tailwind utility classes

### UX Principles
1. **Loading States**: Always show loading spinners for API calls
2. **Error Handling**: Clear error messages with retry options
3. **Feedback**: Success messages after actions
4. **Navigation**: Clear back/next buttons
5. **Responsive**: Works on mobile and desktop

### Pre-built Tailwind Classes
Already available in `src/index.css`:
- `.btn-primary` - Primary button style
- `.btn-secondary` - Secondary button style
- `.card` - Card container
- `.input` - Form input style

---

## Implementation Order

**Priority 1 (Must Have):**
1. Router setup in App.tsx
2. HomePage with backend health check
3. OnboardingPage with form
4. DashboardPage showing workout plan

**Priority 2 (Nice to Have):**
5. Generate new plan functionality
6. Chat section in dashboard

**Priority 3 (Stretch):**
7. Polish and animations
8. More components and refactoring

---

## Success Criteria

The frontend is successful when:
1. ✅ User can see the homepage and verify backend connection
2. ✅ User can complete onboarding and create profile
3. ✅ User can view their workout plan with all details
4. ✅ Loading states work correctly
5. ✅ Errors are handled gracefully
6. ✅ Navigation between pages works
7. ✅ UI looks professional and is responsive

---

## Files to Create

```
frontend/src/
├── App.tsx                    # UPDATE: Add router
├── pages/
│   ├── HomePage.tsx          # CREATE
│   ├── OnboardingPage.tsx    # CREATE
│   └── DashboardPage.tsx     # CREATE
├── components/
│   ├── LoadingSpinner.tsx    # CREATE
│   └── ErrorMessage.tsx      # CREATE
└── types/
    └── index.ts              # CREATE: TypeScript interfaces
```

---

## Notes and Gotchas

1. **API Timing**: Workout plan generation takes 10-30 seconds (AI + RAG)
2. **CORS**: Already configured on backend for localhost:3000
3. **Single User**: No auth needed, backend uses user_id=1
4. **Workout Structure**: `plan_structure` is JSON with weeks → days → exercises
5. **Form Validation**: Use browser validation + custom checks
6. **State Management**: Keep it simple - use React state, Zustand only if needed
7. **Error Cases**: Backend might be down, API might fail, handle gracefully
8. **Environment**: Use `import.meta.env.VITE_API_URL` for API URL

---

## Example Workout Plan Structure

```json
{
  "id": 1,
  "title": "4-Week Boxing Strength Plan",
  "plan_structure": {
    "week_1": [
      {
        "day": "Monday",
        "focus": "Upper Body Strength",
        "warmup": "5 min light cardio",
        "exercises": [
          {
            "name": "Push-ups",
            "sets": 3,
            "reps": "10-12",
            "rest_seconds": 60,
            "notes": "Keep core tight"
          }
        ],
        "cooldown": "5 min stretching",
        "duration_minutes": 60
      }
    ]
  }
}
```

---

## Testing Plan

1. **Homepage**: Visit `/`, check backend connection indicator
2. **Onboarding**: Complete form, verify data saved
3. **Dashboard**: View generated plan, all data displays correctly
4. **Generate Plan**: Create new plan, loading works, new plan shows
5. **Errors**: Disconnect backend, verify error handling

---

## References

- Backend API docs: http://localhost:8000/docs
- API client: `frontend/src/lib/api.ts`
- Tailwind docs: https://tailwindcss.com
- React Router: https://reactrouter.com

---

**Ready to generate PRP for implementation!**
