/**
 * OnboardingPage Component
 *
 * Multi-step form for collecting user profile data
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { profileApi } from '../lib/api';
import ErrorMessage from '../components/ErrorMessage';
import type {
  OnboardingFormData,
  OnboardingStep,
} from '../types';
import {
  EXPERIENCE_LEVEL_OPTIONS,
  FITNESS_GOALS_OPTIONS,
  EQUIPMENT_OPTIONS,
  TRAINING_LOCATION_OPTIONS,
  GENDER_OPTIONS,
} from '../types';

const STEP_CONFIGS = [
  { step: 1, title: 'Basic Information', description: 'Tell us about yourself' },
  {
    step: 2,
    title: 'Experience & Sport',
    description: 'Your training background',
  },
  {
    step: 3,
    title: 'Goals & Limitations',
    description: 'What you want to achieve',
  },
  {
    step: 4,
    title: 'Availability & Equipment',
    description: 'Your training setup',
  },
];

export default function OnboardingPage() {
  const [currentStep, setCurrentStep] = useState<OnboardingStep>(1);
  const [formData, setFormData] = useState<OnboardingFormData>({
    // User Info
    full_name: '',

    // Basic Info
    age: 0,
    gender: 'Male',
    height_cm: 0,
    weight_kg: 0,

    // Experience
    experience_level: 'beginner',
    primary_sport: '',
    years_training: 0,

    // Goals & Limitations
    fitness_goals: [],
    injuries: [],
    health_conditions: [],

    // Availability
    available_days_per_week: 0,
    preferred_session_duration: 0,
    training_location: 'home',

    // Equipment
    has_gym_membership: false,
    available_equipment: [],
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const updateFormData = (field: keyof OnboardingFormData, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    const validation = validateStep(currentStep);
    if (validation.isValid) {
      setError(null);
      setCurrentStep((prev) => Math.min(4, prev + 1) as OnboardingStep);
    } else {
      setError(validation.error || 'Please fill all required fields');
    }
  };

  const handlePrevious = () => {
    setError(null);
    setCurrentStep((prev) => Math.max(1, prev - 1) as OnboardingStep);
  };

  const handleSubmit = async () => {
    const validation = validateStep(4);
    if (!validation.isValid) {
      setError(validation.error || 'Please fill all required fields');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      // Filter out fields with 0 values (should be null/undefined for Optional fields)
      const cleanedData: any = {};
      Object.entries(formData).forEach(([key, value]) => {
        if (value === 0) {
          // Skip numeric fields with 0 value
          return;
        }
        if (Array.isArray(value) && value.length === 0) {
          // Skip empty arrays
          return;
        }
        if (value === '') {
          // Skip empty strings
          return;
        }
        // Ensure years_training is always an integer
        if (key === 'years_training' && typeof value === 'number') {
          cleanedData[key] = Math.floor(value);
        } else {
          cleanedData[key] = value;
        }
      });

      await profileApi.submitOnboarding(cleanedData);

      // Clear chat history for new user
      localStorage.removeItem('coachx_chat_history');

      navigate('/dashboard');
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          'Failed to submit profile'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const validateStep = (
    step: OnboardingStep
  ): { isValid: boolean; error?: string } => {
    switch (step) {
      case 1:
        if (!formData.full_name.trim())
          return { isValid: false, error: 'Name is required' };
        if (formData.age < 13 || formData.age > 100)
          return { isValid: false, error: 'Age must be between 13 and 100' };
        if (formData.height_cm < 100 || formData.height_cm > 250)
          return {
            isValid: false,
            error: 'Height must be between 100 and 250 cm',
          };
        if (formData.weight_kg < 30 || formData.weight_kg > 300)
          return {
            isValid: false,
            error: 'Weight must be between 30 and 300 kg',
          };
        return { isValid: true };

      case 2:
        if (!formData.primary_sport.trim())
          return { isValid: false, error: 'Primary sport is required' };
        if (formData.years_training < 0 || formData.years_training > 50)
          return {
            isValid: false,
            error: 'Years training must be between 0 and 50',
          };
        return { isValid: true };

      case 3:
        if (formData.fitness_goals.length === 0)
          return {
            isValid: false,
            error: 'Please select at least one fitness goal',
          };
        return { isValid: true };

      case 4:
        if (
          formData.available_days_per_week < 1 ||
          formData.available_days_per_week > 7
        )
          return {
            isValid: false,
            error: 'Available days must be between 1 and 7',
          };
        if (
          formData.preferred_session_duration < 15 ||
          formData.preferred_session_duration > 180
        )
          return {
            isValid: false,
            error: 'Session duration must be between 15 and 180 minutes',
          };
        if (formData.available_equipment.length === 0)
          return {
            isValid: false,
            error: 'Please select at least one equipment option (or "none")',
          };
        return { isValid: true };

      default:
        return { isValid: true };
    }
  };

  const currentStepConfig = STEP_CONFIGS[currentStep - 1];

  return (
    <div className="min-h-screen bg-black py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Progress Indicator */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-300">
              Step {currentStep} of 4
            </span>
            <span className="text-sm text-gray-400">
              {Math.round((currentStep / 4) * 100)}% Complete
            </span>
          </div>
          <div className="w-full bg-gray-800 rounded-full h-2">
            <div
              className="bg-red-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${(currentStep / 4) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Form Card */}
        <div className="card">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-white">
              {currentStepConfig.title}
            </h2>
            <p className="text-gray-400 mt-1">
              {currentStepConfig.description}
            </p>
          </div>

          {error && <ErrorMessage error={error} onRetry={() => setError(null)} />}

          {/* Step Content */}
          {currentStep === 1 && (
            <Step1BasicInfo formData={formData} updateFormData={updateFormData} />
          )}
          {currentStep === 2 && (
            <Step2Experience formData={formData} updateFormData={updateFormData} />
          )}
          {currentStep === 3 && (
            <Step3Goals formData={formData} updateFormData={updateFormData} />
          )}
          {currentStep === 4 && (
            <Step4Availability
              formData={formData}
              updateFormData={updateFormData}
            />
          )}

          {/* Navigation Buttons */}
          <div className="flex justify-between mt-8 pt-6 border-t border-gray-800">
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

// ============================================================================
// Step 1: Basic Information
// ============================================================================

function Step1BasicInfo({
  formData,
  updateFormData,
}: {
  formData: OnboardingFormData;
  updateFormData: (field: keyof OnboardingFormData, value: any) => void;
}) {
  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Name <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          value={formData.full_name}
          onChange={(e) => updateFormData('full_name', e.target.value)}
          className="input"
          placeholder="Your full name"
          required
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Age <span className="text-red-500">*</span>
          </label>
          <input
            type="number"
            value={formData.age || ''}
            onChange={(e) => updateFormData('age', Number(e.target.value))}
            min="13"
            max="100"
            className="input"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Gender <span className="text-red-500">*</span>
          </label>
          <select
            value={formData.gender}
            onChange={(e) => updateFormData('gender', e.target.value)}
            className="input"
            required
          >
            {GENDER_OPTIONS.map((gender) => (
              <option key={gender} value={gender}>
                {gender}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Height (cm) <span className="text-red-500">*</span>
          </label>
          <input
            type="number"
            value={formData.height_cm || ''}
            onChange={(e) =>
              updateFormData('height_cm', Number(e.target.value))
            }
            min="100"
            max="250"
            className="input"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Weight (kg) <span className="text-red-500">*</span>
          </label>
          <input
            type="number"
            value={formData.weight_kg || ''}
            onChange={(e) =>
              updateFormData('weight_kg', Number(e.target.value))
            }
            min="30"
            max="300"
            className="input"
            required
          />
        </div>
      </div>
    </div>
  );
}

// ============================================================================
// Step 2: Experience & Sport
// ============================================================================

function Step2Experience({
  formData,
  updateFormData,
}: {
  formData: OnboardingFormData;
  updateFormData: (field: keyof OnboardingFormData, value: any) => void;
}) {
  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Primary Sport <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          value={formData.primary_sport}
          onChange={(e) => updateFormData('primary_sport', e.target.value)}
          className="input"
          placeholder="e.g., Boxing, Running, Weightlifting"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Experience Level <span className="text-red-500">*</span>
        </label>
        <select
          value={formData.experience_level}
          onChange={(e) => updateFormData('experience_level', e.target.value)}
          className="input"
          required
        >
          {EXPERIENCE_LEVEL_OPTIONS.map((level) => (
            <option key={level} value={level}>
              {level.charAt(0).toUpperCase() + level.slice(1)}
            </option>
          ))}
        </select>
        <p className="text-xs text-gray-500 mt-1">
          Beginner: &lt;1 year • Intermediate: 1-3 years • Advanced: 3+ years
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Years Training <span className="text-red-500">*</span>
        </label>
        <input
          type="number"
          value={formData.years_training || ''}
          onChange={(e) =>
            updateFormData('years_training', parseInt(e.target.value) || 0)
          }
          min="0"
          max="50"
          step="1"
          className="input"
          required
        />
      </div>
    </div>
  );
}

// ============================================================================
// Step 3: Goals & Limitations
// ============================================================================

function Step3Goals({
  formData,
  updateFormData,
}: {
  formData: OnboardingFormData;
  updateFormData: (field: keyof OnboardingFormData, value: any) => void;
}) {
  const toggleGoal = (goal: string) => {
    const current = formData.fitness_goals;
    if (current.includes(goal)) {
      updateFormData(
        'fitness_goals',
        current.filter((g) => g !== goal)
      );
    } else {
      updateFormData('fitness_goals', [...current, goal]);
    }
  };

  const addInjury = () => {
    const injury = prompt('Enter injury description:');
    if (injury && injury.trim()) {
      updateFormData('injuries', [...formData.injuries, injury.trim()]);
    }
  };

  const removeInjury = (index: number) => {
    updateFormData(
      'injuries',
      formData.injuries.filter((_, i) => i !== index)
    );
  };

  const addHealthCondition = () => {
    const condition = prompt('Enter health condition:');
    if (condition && condition.trim()) {
      updateFormData('health_conditions', [
        ...formData.health_conditions,
        condition.trim(),
      ]);
    }
  };

  const removeHealthCondition = (index: number) => {
    updateFormData(
      'health_conditions',
      formData.health_conditions.filter((_, i) => i !== index)
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Fitness Goals <span className="text-red-500">*</span>
        </label>
        <div className="space-y-2">
          {FITNESS_GOALS_OPTIONS.map((goal) => (
            <label key={goal} className="flex items-center">
              <input
                type="checkbox"
                checked={formData.fitness_goals.includes(goal)}
                onChange={() => toggleGoal(goal)}
                className="mr-2 h-4 w-4 text-primary-600 rounded"
              />
              <span className="text-sm text-gray-700">
                {goal.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
              </span>
            </label>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Injuries (Optional)
        </label>
        {formData.injuries.length > 0 && (
          <div className="space-y-2 mb-2">
            {formData.injuries.map((injury, index) => (
              <div
                key={index}
                className="flex items-center justify-between bg-gray-100 p-2 rounded"
              >
                <span className="text-sm text-gray-700">{injury}</span>
                <button
                  onClick={() => removeInjury(index)}
                  className="text-red-600 hover:text-red-700 text-sm"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
        <button
          onClick={addInjury}
          className="text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          + Add Injury
        </button>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Health Conditions (Optional)
        </label>
        {formData.health_conditions.length > 0 && (
          <div className="space-y-2 mb-2">
            {formData.health_conditions.map((condition, index) => (
              <div
                key={index}
                className="flex items-center justify-between bg-gray-100 p-2 rounded"
              >
                <span className="text-sm text-gray-700">{condition}</span>
                <button
                  onClick={() => removeHealthCondition(index)}
                  className="text-red-600 hover:text-red-700 text-sm"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
        <button
          onClick={addHealthCondition}
          className="text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          + Add Health Condition
        </button>
      </div>
    </div>
  );
}

// ============================================================================
// Step 4: Availability & Equipment
// ============================================================================

function Step4Availability({
  formData,
  updateFormData,
}: {
  formData: OnboardingFormData;
  updateFormData: (field: keyof OnboardingFormData, value: any) => void;
}) {
  const toggleEquipment = (equipment: string) => {
    const current = formData.available_equipment;
    if (current.includes(equipment)) {
      updateFormData(
        'available_equipment',
        current.filter((e) => e !== equipment)
      );
    } else {
      updateFormData('available_equipment', [...current, equipment]);
    }
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Available Days per Week <span className="text-red-500">*</span>
          </label>
          <input
            type="number"
            value={formData.available_days_per_week || ''}
            onChange={(e) =>
              updateFormData('available_days_per_week', Number(e.target.value))
            }
            min="1"
            max="7"
            className="input"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Session Duration (minutes) <span className="text-red-500">*</span>
          </label>
          <input
            type="number"
            value={formData.preferred_session_duration || ''}
            onChange={(e) =>
              updateFormData(
                'preferred_session_duration',
                Number(e.target.value)
              )
            }
            min="15"
            max="180"
            step="15"
            className="input"
            required
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Training Location <span className="text-red-500">*</span>
        </label>
        <select
          value={formData.training_location}
          onChange={(e) => updateFormData('training_location', e.target.value)}
          className="input"
          required
        >
          {TRAINING_LOCATION_OPTIONS.map((location) => (
            <option key={location} value={location}>
              {location.charAt(0).toUpperCase() + location.slice(1)}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={formData.has_gym_membership}
            onChange={(e) =>
              updateFormData('has_gym_membership', e.target.checked)
            }
            className="mr-2 h-4 w-4 text-primary-600 rounded"
          />
          <span className="text-sm font-medium text-gray-700">
            I have a gym membership
          </span>
        </label>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Available Equipment <span className="text-red-500">*</span>
        </label>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {EQUIPMENT_OPTIONS.map((equipment) => (
            <label key={equipment} className="flex items-center">
              <input
                type="checkbox"
                checked={formData.available_equipment.includes(equipment)}
                onChange={() => toggleEquipment(equipment)}
                className="mr-2 h-4 w-4 text-primary-600 rounded"
              />
              <span className="text-sm text-gray-700">
                {equipment.replace(/_/g, ' ').replace(/\b\w/g, (l) =>
                  l.toUpperCase()
                )}
              </span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
}
