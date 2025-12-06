/**
 * TypeScript Type Definitions for CoachX Frontend
 *
 * These types match the backend API response schemas
 */

// ============================================================================
// User Profile Types
// ============================================================================

export interface UserProfile {
  id: number;
  user_id: number;
  full_name: string;
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

// ============================================================================
// Onboarding Form Types
// ============================================================================

export interface OnboardingFormData {
  // User Info
  full_name: string;

  // Basic Info
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

export type OnboardingStep = 1 | 2 | 3 | 4;

export interface FormStepConfig {
  step: OnboardingStep;
  title: string;
  description: string;
}

// ============================================================================
// Workout Plan Types
// ============================================================================

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
  warmup?: string;
  exercises: Exercise[];
  cooldown?: string;
  duration_minutes?: number;
  duration_min?: number;  // Backend uses this field
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

// ============================================================================
// API Response Types
// ============================================================================

export interface ProfileStatusResponse {
  profile_exists: boolean;
  profile_completion_percentage: number;
  message: string;
}

export interface HealthCheckResponse {
  status: string;
  timestamp: string;
}

export interface MessageResponse {
  message: string;
}

export interface ChatResponse {
  answer: string;
  sport?: string;
  context_used: number;
  timestamp: string;
}

// ============================================================================
// Workout Plan Generation Types
// ============================================================================

export interface GeneratePlanParams {
  duration_weeks: number;
  custom_notes?: string;
}

// ============================================================================
// Form Validation Types
// ============================================================================

export interface ValidationError {
  field: string;
  message: string;
}

// ============================================================================
// Fitness Goals Options (for multi-select)
// ============================================================================

export const FITNESS_GOALS_OPTIONS = [
  'muscle_gain',
  'weight_loss',
  'strength',
  'endurance',
  'flexibility',
  'sport_performance',
] as const;

export type FitnessGoal = typeof FITNESS_GOALS_OPTIONS[number];

// ============================================================================
// Equipment Options (for multi-select)
// ============================================================================

export const EQUIPMENT_OPTIONS = [
  'dumbbells',
  'barbell',
  'kettlebells',
  'resistance_bands',
  'pull_up_bar',
  'bench',
  'cardio_machines',
  'none',
] as const;

export type Equipment = typeof EQUIPMENT_OPTIONS[number];

// ============================================================================
// Training Location Options
// ============================================================================

export const TRAINING_LOCATION_OPTIONS = [
  'home',
  'gym',
  'outdoor',
  'hybrid',
] as const;

export type TrainingLocation = typeof TRAINING_LOCATION_OPTIONS[number];

// ============================================================================
// Gender Options
// ============================================================================

export const GENDER_OPTIONS = ['Male', 'Female', 'Other'] as const;

export type Gender = typeof GENDER_OPTIONS[number];

// ============================================================================
// Experience Level Options
// ============================================================================

export const EXPERIENCE_LEVEL_OPTIONS = [
  'beginner',
  'intermediate',
  'advanced',
] as const;

export type ExperienceLevel = typeof EXPERIENCE_LEVEL_OPTIONS[number];
