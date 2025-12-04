# PRP: Frontend Implementation for CoachX

**Generated:** 2025-12-03
**Status:** Ready for Execution
**Estimated Complexity:** Medium-High (5-7 files, ~600-800 lines)

---

## Overview

Build a minimal but functional React frontend that connects to the fully operational CoachX backend. The frontend will allow users to complete onboarding, view their AI-generated workout plans, and interact with the AI coach.

**Dependencies:**
- ✅ Backend fully functional (localhost:8000)
- ✅ Vite + React + TypeScript setup complete
- ✅ Tailwind CSS configured
- ✅ API client created (src/lib/api.ts)
- ✅ Folder structure created

---

## Step-by-Step Implementation Plan

### Phase 1: Core Setup & Types

#### Step 1.1: Create TypeScript Types
**File:** `frontend/src/types/index.ts`

Create comprehensive TypeScript interfaces matching backend API responses.

**Required Types:**
```typescript
// User Profile Types
export interface UserProfile {
  id: number;
  user_id: number;
  name: string;
  age: number;
  gender: string;
  height_cm: number;
  weight_kg: number;
  experience_level: 'beginner' | 'intermediate' | 'advanced';
  primary_sport: string;
  years_training: number;
  fitness_goals: string[];
  injuries: string[];
  health_conditions: string[];
  available_days_per_week: number;
  preferred_session_duration: number;
  training_location: string;
  has_gym_membership: boolean;
  available_equipment: string[];
  profile_completion_percentage: number;
  created_at: string;
  updated_at: string;
}

// Onboarding Form Data
export interface OnboardingFormData {
  // Basic Info
  name: string;
  age: number;
  gender: string;
  height_cm: number;
  weight_kg: number;

  // Experience
  experience_level: 'beginner' | 'intermediate' | 'advanced';
  primary_sport: string;
  years_training: number;

  // Goals & Limitations
  fitness_goals: string[];
  injuries: string[];
  health_conditions: string[];

  // Availability
  available_days_per_week: number;
  preferred_session_duration: number;
  training_location: string;

  // Equipment
  has_gym_membership: boolean;
  available_equipment: string[];
}

// Workout Plan Types
export interface Exercise {
  name: string;
  sets: number;
  reps: string;
  rest_seconds: number;
  notes?: string;
}

export interface WorkoutDay {
  day: string;
  focus: string;
  warmup: string;
  exercises: Exercise[];
  cooldown: string;
  duration_minutes: number;
}

export interface WorkoutPlan {
  id: number;
  user_id: number;
  title: string;
  description?: string;
  duration_weeks: number;
  plan_structure: {
    [week: string]: WorkoutDay[];
  };
  sport_focus?: string;
  is_active: boolean;
  completed: boolean;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

// API Response Types
export interface ProfileStatusResponse {
  profile_exists: boolean;
  profile_completion_percentage: number;
  message: string;
}

export interface HealthCheckResponse {
  status: string;
  timestamp: string;
}

// Form Step Types for Multi-step Form
export type OnboardingStep = 1 | 2 | 3 | 4;

export interface FormStepConfig {
  step: OnboardingStep;
  title: string;
  description: string;
}
```

**Validation:**
- All types match backend Pydantic schemas
- Proper use of optional (?) and required fields
- Correct union types for enums

---

#### Step 1.2: Create Reusable Components - LoadingSpinner
**File:** `frontend/src/components/LoadingSpinner.tsx`

Simple, reusable loading indicator for async operations.

**Requirements:**
- Accept optional `size` prop ('sm' | 'md' | 'lg')
- Accept optional `message` prop for custom loading text
- Tailwind-based styling
- Centered by default

**Implementation:**
```typescript
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  message?: string;
}

export default function LoadingSpinner({ size = 'md', message }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'h-8 w-8',
    md: 'h-12 w-12',
    lg: 'h-16 w-16',
  };

  return (
    <div className="flex flex-col items-center justify-center p-8">
      <div className={`animate-spin rounded-full border-4 border-gray-200 border-t-primary-600 ${sizeClasses[size]}`}></div>
      {message && <p className="mt-4 text-gray-600">{message}</p>}
    </div>
  );
}
```

---

#### Step 1.3: Create Reusable Components - ErrorMessage
**File:** `frontend/src/components/ErrorMessage.tsx`

Display errors with optional retry functionality.

**Requirements:**
- Accept `error` prop (string or Error object)
- Accept optional `onRetry` callback
- Show retry button only if `onRetry` provided
- Red/warning styling

**Implementation:**
```typescript
interface ErrorMessageProps {
  error: string | Error;
  onRetry?: () => void;
}

export default function ErrorMessage({ error, onRetry }: ErrorMessageProps) {
  const errorMessage = typeof error === 'string' ? error : error.message;

  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 my-4">
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="ml-3 flex-1">
          <h3 className="text-sm font-medium text-red-800">Error</h3>
          <p className="mt-1 text-sm text-red-700">{errorMessage}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-3 text-sm font-medium text-red-600 hover:text-red-500"
            >
              Try Again
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
```

---

### Phase 2: Router & Navigation

#### Step 2.1: Update App.tsx with Router
**File:** `frontend/src/App.tsx`

Configure React Router with three main routes.

**Requirements:**
- Use `BrowserRouter` from react-router-dom
- Define routes: `/`, `/onboarding`, `/dashboard`
- Clean layout structure
- No authentication checks (MVP single user)

**Implementation:**
```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import OnboardingPage from './pages/OnboardingPage';
import DashboardPage from './pages/DashboardPage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
```

**Validation:**
- All routes render correctly
- No console errors
- Browser back/forward works

---

### Phase 3: HomePage Implementation

#### Step 3.1: Create HomePage
**File:** `frontend/src/pages/HomePage.tsx`

Landing page with hero section and backend health check.

**Requirements:**
1. **Hero Section:**
   - App name and tagline
   - Brief description of CoachX
   - CTA button to start onboarding

2. **Backend Status Indicator:**
   - Call `healthApi.check()` on mount
   - Show green indicator if connected
   - Show red indicator if disconnected
   - Display backend URL and status

3. **Layout:**
   - Centered content
   - Responsive design
   - Professional styling

**Implementation Structure:**
```typescript
export default function HomePage() {
  const [backendStatus, setBackendStatus] = useState<'loading' | 'online' | 'offline'>('loading');
  const navigate = useNavigate();

  useEffect(() => {
    // Check backend health on mount
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      await healthApi.check();
      setBackendStatus('online');
    } catch (error) {
      setBackendStatus('offline');
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      {/* Hero Section */}
      <div className="max-w-3xl mx-auto text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          CoachX
        </h1>
        <p className="text-xl text-gray-600 mb-2">
          Your AI-Powered Personal Training Assistant
        </p>
        <p className="text-lg text-gray-500 mb-8">
          Get personalized workout plans powered by AI and sports science research
        </p>

        <button
          onClick={() => navigate('/onboarding')}
          className="btn-primary text-lg px-8 py-3"
        >
          Get Started
        </button>
      </div>

      {/* Backend Status */}
      <div className="mt-12 card max-w-md">
        <h3 className="text-sm font-medium text-gray-700 mb-2">Backend Status</h3>
        <div className="flex items-center space-x-2">
          {backendStatus === 'loading' && <LoadingSpinner size="sm" />}
          {backendStatus === 'online' && (
            <>
              <div className="h-3 w-3 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-600">Connected</span>
            </>
          )}
          {backendStatus === 'offline' && (
            <>
              <div className="h-3 w-3 bg-red-500 rounded-full"></div>
              <span className="text-sm text-gray-600">Disconnected</span>
            </>
          )}
        </div>
        <p className="text-xs text-gray-500 mt-1">
          {import.meta.env.VITE_API_URL}
        </p>
      </div>
    </div>
  );
}
```

**Validation:**
- Backend status indicator shows correct state
- CTA button navigates to `/onboarding`
- Responsive on mobile and desktop
- No errors in console

---

### Phase 4: OnboardingPage Implementation

#### Step 4.1: Create OnboardingPage with Multi-Step Form
**File:** `frontend/src/pages/OnboardingPage.tsx`

Multi-step form for collecting user profile data.

**Requirements:**

**Form Structure (4 Steps):**

**Step 1: Basic Information**
- Name (text, required)
- Age (number, 13-100, required)
- Gender (select: Male/Female/Other, required)
- Height in cm (number, 100-250, required)
- Weight in kg (number, 30-300, required)

**Step 2: Experience & Sport**
- Experience Level (select: beginner/intermediate/advanced, required)
- Primary Sport (text, required)
- Years Training (number, 0-50, required)

**Step 3: Goals & Limitations**
- Fitness Goals (multi-select checkboxes: muscle_gain, weight_loss, strength, endurance, flexibility, sport_performance)
- Injuries (text input with add/remove, optional)
- Health Conditions (text input with add/remove, optional)

**Step 4: Availability & Equipment**
- Available Days per Week (number, 1-7, required)
- Preferred Session Duration (number, 15-180 minutes, required)
- Training Location (select: home/gym/outdoor/hybrid, required)
- Has Gym Membership (boolean checkbox)
- Available Equipment (multi-select checkboxes: dumbbells, barbell, kettlebells, resistance_bands, pull_up_bar, bench, cardio_machines, none)

**Features:**
- Progress indicator (Step 1/4, 2/4, etc.)
- Next/Previous buttons
- Submit button on last step
- Client-side validation per step
- Loading state during submission
- Error handling with ErrorMessage component
- Redirect to `/dashboard` on success

**Implementation Structure:**
```typescript
export default function OnboardingPage() {
  const [currentStep, setCurrentStep] = useState<OnboardingStep>(1);
  const [formData, setFormData] = useState<OnboardingFormData>({
    // Initialize with empty/default values
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleNext = () => {
    // Validate current step
    if (validateStep(currentStep)) {
      setCurrentStep((prev) => Math.min(4, prev + 1) as OnboardingStep);
    }
  };

  const handlePrevious = () => {
    setCurrentStep((prev) => Math.max(1, prev - 1) as OnboardingStep);
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setError(null);

    try {
      await profileApi.submitOnboarding(formData);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to submit profile');
    } finally {
      setIsSubmitting(false);
    }
  };

  const validateStep = (step: OnboardingStep): boolean => {
    // Implement validation per step
    // Return true if valid, false if invalid (show error message)
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Progress Indicator */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              Step {currentStep} of 4
            </span>
            <span className="text-sm text-gray-500">
              {Math.round((currentStep / 4) * 100)}% Complete
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${(currentStep / 4) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Form Card */}
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            {getStepTitle(currentStep)}
          </h2>

          {error && <ErrorMessage error={error} onRetry={() => setError(null)} />}

          {/* Step Content */}
          {currentStep === 1 && <Step1BasicInfo formData={formData} setFormData={setFormData} />}
          {currentStep === 2 && <Step2Experience formData={formData} setFormData={setFormData} />}
          {currentStep === 3 && <Step3Goals formData={formData} setFormData={setFormData} />}
          {currentStep === 4 && <Step4Availability formData={formData} setFormData={setFormData} />}

          {/* Navigation Buttons */}
          <div className="flex justify-between mt-8">
            <button
              onClick={handlePrevious}
              disabled={currentStep === 1}
              className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>

            {currentStep < 4 ? (
              <button onClick={handleNext} className="btn-primary">
                Next
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="btn-primary disabled:opacity-50"
              >
                {isSubmitting ? 'Submitting...' : 'Complete Onboarding'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// Helper Components (defined in same file or separate files)
function Step1BasicInfo({ formData, setFormData }) { /* ... */ }
function Step2Experience({ formData, setFormData }) { /* ... */ }
function Step3Goals({ formData, setFormData }) { /* ... */ }
function Step4Availability({ formData, setFormData }) { /* ... */ }
```

**Validation:**
- All required fields enforced
- Number fields have min/max validation
- Multi-select arrays work correctly
- Navigation between steps works
- Submit calls API and redirects
- Error handling displays correctly

---

### Phase 5: DashboardPage Implementation

#### Step 5.1: Create DashboardPage
**File:** `frontend/src/pages/DashboardPage.tsx`

Dashboard showing user profile and active workout plan.

**Requirements:**

**Layout Sections:**

1. **Header:**
   - Welcome message with user name
   - Profile completion percentage badge
   - Link to view full profile (stretch)

2. **Profile Summary Card:**
   - Display key profile info: age, experience, primary sport
   - Compact, clean layout

3. **Active Workout Plan Section:**
   - Fetch from `workoutApi.getActivePlan()` on mount
   - Display plan title and description
   - Show week-by-week structure (collapsible/expandable)
   - Each day shows:
     - Day name (e.g., "Monday")
     - Focus (e.g., "Upper Body Strength")
     - Warmup description
     - Exercise list (name, sets, reps, rest, notes)
     - Cooldown description
     - Duration in minutes
   - Button to generate new plan

4. **Generate New Plan Modal/Section:**
   - Input for duration_weeks (1-12, default 4)
   - Textarea for custom_notes (optional)
   - Submit button
   - Show loading state during generation (10-30 seconds)
   - On success, refetch active plan

5. **Error Handling:**
   - No profile: Show message to complete onboarding
   - No active plan: Show message and button to generate first plan
   - API errors: Display with ErrorMessage component

**Implementation Structure:**
```typescript
export default function DashboardPage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [activePlan, setActivePlan] = useState<WorkoutPlan | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [generateParams, setGenerateParams] = useState({
    duration_weeks: 4,
    custom_notes: '',
  });
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Fetch profile and active plan
      const profileData = await profileApi.getProfile();
      setProfile(profileData);

      try {
        const planData = await workoutApi.getActivePlan();
        setActivePlan(planData);
      } catch (planError: any) {
        // No active plan is OK
        if (planError.response?.status !== 404) {
          throw planError;
        }
      }
    } catch (err: any) {
      if (err.response?.status === 404) {
        // No profile, redirect to onboarding
        navigate('/onboarding');
      } else {
        setError(err.response?.data?.detail || 'Failed to load dashboard');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleGeneratePlan = async () => {
    setIsGenerating(true);
    setError(null);

    try {
      await workoutApi.generatePlan(generateParams);
      setShowGenerateModal(false);
      await loadDashboardData(); // Reload to show new plan
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate plan');
    } finally {
      setIsGenerating(false);
    }
  };

  if (isLoading) {
    return <LoadingSpinner size="lg" message="Loading your dashboard..." />;
  }

  if (!profile) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">No profile found</p>
          <button onClick={() => navigate('/onboarding')} className="btn-primary">
            Complete Onboarding
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {profile.name}!
          </h1>
          <p className="text-gray-600 mt-1">
            Profile Completion: {profile.profile_completion_percentage}%
          </p>
        </div>

        {error && <ErrorMessage error={error} onRetry={loadDashboardData} />}

        {/* Profile Summary */}
        <div className="card mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Your Profile</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-gray-500">Age</p>
              <p className="text-lg font-medium">{profile.age}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Experience</p>
              <p className="text-lg font-medium capitalize">{profile.experience_level}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Primary Sport</p>
              <p className="text-lg font-medium">{profile.primary_sport}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Training Days/Week</p>
              <p className="text-lg font-medium">{profile.available_days_per_week}</p>
            </div>
          </div>
        </div>

        {/* Active Workout Plan */}
        {activePlan ? (
          <div className="card mb-6">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{activePlan.title}</h2>
                {activePlan.description && (
                  <p className="text-gray-600 mt-1">{activePlan.description}</p>
                )}
                <p className="text-sm text-gray-500 mt-2">
                  {activePlan.duration_weeks} weeks • Created {new Date(activePlan.created_at).toLocaleDateString()}
                </p>
              </div>
              <button
                onClick={() => setShowGenerateModal(true)}
                className="btn-secondary"
              >
                Generate New Plan
              </button>
            </div>

            {/* Workout Weeks */}
            <WorkoutPlanDisplay plan={activePlan} />
          </div>
        ) : (
          <div className="card text-center py-12">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No Active Workout Plan
            </h3>
            <p className="text-gray-600 mb-6">
              Generate your first personalized workout plan to get started!
            </p>
            <button onClick={() => setShowGenerateModal(true)} className="btn-primary">
              Generate Workout Plan
            </button>
          </div>
        )}

        {/* Generate Plan Modal */}
        {showGenerateModal && (
          <GeneratePlanModal
            params={generateParams}
            setParams={setGenerateParams}
            isGenerating={isGenerating}
            onGenerate={handleGeneratePlan}
            onClose={() => setShowGenerateModal(false)}
          />
        )}
      </div>
    </div>
  );
}

// Helper Components
function WorkoutPlanDisplay({ plan }: { plan: WorkoutPlan }) {
  // Display weeks and days with collapsible sections
  // Show exercises for each day
}

function GeneratePlanModal({ params, setParams, isGenerating, onGenerate, onClose }) {
  // Modal for generating new plan
}
```

**Validation:**
- Dashboard loads profile and plan correctly
- No profile redirects to onboarding
- No active plan shows generate button
- Generate plan flow works (including 10-30s loading)
- Plan display shows all weeks and days correctly
- Exercises display with all details

---

### Phase 6: Additional Components (Optional/Stretch)

#### Step 6.1: WorkoutPlanDisplay Component
**File:** `frontend/src/components/WorkoutPlanDisplay.tsx`

Extract workout plan rendering logic into reusable component.

**Features:**
- Collapsible weeks
- Collapsible days within weeks
- Exercise cards with proper formatting
- Rest time in seconds → minutes conversion
- Print-friendly layout (stretch)

---

#### Step 6.2: Chat Section (Stretch Goal)
**File:** `frontend/src/components/ChatSection.tsx`

Simple chat interface within DashboardPage.

**Features:**
- Input field for question
- Submit button
- Display AI response
- Call `chatApi.sendMessage({ q, sport: profile.primary_sport })`
- Loading state while AI responds
- Show multiple Q&A pairs (optional)

---

## Testing Checklist

### Manual Testing Steps:

**Homepage Tests:**
- [ ] Visit `http://localhost:3000/`
- [ ] Backend status indicator shows green (backend running)
- [ ] Backend status indicator shows red (backend stopped)
- [ ] "Get Started" button navigates to `/onboarding`
- [ ] Responsive on mobile (< 768px)

**Onboarding Tests:**
- [ ] All 4 steps render correctly
- [ ] Progress bar updates per step
- [ ] Validation works (try invalid inputs)
- [ ] Previous button disabled on step 1
- [ ] Next button advances steps
- [ ] Multi-select checkboxes work (goals, equipment)
- [ ] Dynamic arrays work (injuries, health_conditions)
- [ ] Submit on step 4 calls API
- [ ] Success redirects to `/dashboard`
- [ ] Error displays with ErrorMessage component
- [ ] Form state persists when going back/forward

**Dashboard Tests:**
- [ ] Loads profile data correctly
- [ ] Displays profile summary card
- [ ] Shows active workout plan (if exists)
- [ ] Weeks and days display correctly
- [ ] Exercises show all details (sets, reps, rest, notes)
- [ ] "Generate New Plan" button opens modal
- [ ] Generate plan modal accepts inputs
- [ ] Generate plan shows loading (10-30s)
- [ ] New plan displays after generation
- [ ] No profile redirects to onboarding
- [ ] No active plan shows "Generate first plan" message
- [ ] Error handling works (disconnect backend)

**Edge Cases:**
- [ ] No profile: Visit `/dashboard` directly → redirects to onboarding
- [ ] Backend down: All pages show appropriate errors
- [ ] Long plan names: UI doesn't break
- [ ] Many exercises: Scrolling works
- [ ] Form validation: All required fields enforced

---

## File Checklist

**Files to Create:**
- [ ] `frontend/src/types/index.ts` (TypeScript types)
- [ ] `frontend/src/components/LoadingSpinner.tsx`
- [ ] `frontend/src/components/ErrorMessage.tsx`
- [ ] `frontend/src/pages/HomePage.tsx`
- [ ] `frontend/src/pages/OnboardingPage.tsx`
- [ ] `frontend/src/pages/DashboardPage.tsx`

**Files to Modify:**
- [ ] `frontend/src/App.tsx` (add router)

**Optional Files (Stretch):**
- [ ] `frontend/src/components/WorkoutPlanDisplay.tsx`
- [ ] `frontend/src/components/WorkoutDayCard.tsx`
- [ ] `frontend/src/components/ExerciseList.tsx`
- [ ] `frontend/src/components/ChatSection.tsx`
- [ ] `frontend/src/components/GeneratePlanModal.tsx`

---

## Success Criteria

The frontend is complete when:
1. ✅ User can see the homepage and verify backend connection
2. ✅ User can complete full onboarding flow (4 steps)
3. ✅ Profile data is saved to backend correctly
4. ✅ Dashboard displays profile summary
5. ✅ Dashboard displays active workout plan with all weeks/days/exercises
6. ✅ User can generate new workout plan
7. ✅ Loading states work correctly (spinners, disabled buttons)
8. ✅ Error handling works gracefully
9. ✅ Navigation between pages works
10. ✅ UI is responsive (mobile and desktop)
11. ✅ No console errors
12. ✅ TypeScript compiles without errors

---

## Notes

**Implementation Tips:**
- Start with types first (prevents TypeScript errors)
- Build components bottom-up (LoadingSpinner, ErrorMessage first)
- Test each page individually before moving to next
- Use browser DevTools Network tab to verify API calls
- Check backend logs if API calls fail

**Common Pitfalls:**
- Forgetting to handle 404 for no profile/no active plan
- Not showing loading state during 10-30s plan generation
- Not validating form inputs before submission
- Forgetting to redirect after successful onboarding
- Not parsing `plan_structure` JSON correctly

**Design Consistency:**
- Use `.btn-primary` and `.btn-secondary` classes
- Use `.card` class for containers
- Use `.input` class for form fields
- Follow Tailwind's spacing scale (4, 6, 8, 12, etc.)
- Keep typography sizes consistent

---

## Commit Strategy

After completing implementation, create commits following atomic pattern:

1. `feat(frontend): add TypeScript types and interfaces`
2. `feat(frontend): add LoadingSpinner and ErrorMessage components`
3. `feat(frontend): add router configuration to App.tsx`
4. `feat(frontend): implement HomePage with backend health check`
5. `feat(frontend): implement OnboardingPage with multi-step form`
6. `feat(frontend): implement DashboardPage with workout plan display`
7. `docs: add frontend testing notes and success criteria`

---

**Ready for Execution!**
