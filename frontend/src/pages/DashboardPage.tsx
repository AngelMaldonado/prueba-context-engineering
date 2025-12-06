/**
 * DashboardPage Component
 *
 * Dashboard showing user profile and active workout plan
 */

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { profileApi, workoutApi } from "../lib/api";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import ChatSection from "../components/ChatSection";
import type { UserProfile, WorkoutPlan, GeneratePlanParams } from "../types";

export default function DashboardPage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [activePlan, setActivePlan] = useState<WorkoutPlan | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [generateParams, setGenerateParams] = useState<GeneratePlanParams>({
    duration_weeks: 1,
    custom_notes: "",
  });
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Fetch profile
      const profileData = await profileApi.getProfile();
      setProfile(profileData);

      // Fetch active plan (404 is OK if no plan exists)
      try {
        const planData = await workoutApi.getActivePlan();
        setActivePlan(planData);
      } catch (planError: any) {
        if (planError.response?.status !== 404) {
          throw planError;
        }
      }
    } catch (err: any) {
      if (err.response?.status === 404) {
        // No profile, redirect to onboarding
        navigate("/onboarding");
      } else {
        setError(
          err.response?.data?.detail ||
            err.message ||
            "Failed to load dashboard"
        );
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
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Failed to generate workout plan"
      );
    } finally {
      setIsGenerating(false);
    }
  };

  const handleResetProfile = async () => {
    if (!confirm("Are you sure you want to reset your profile? This will delete all your data including workout plans and chat history.")) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      await profileApi.resetProfile();
      // Clear localStorage
      localStorage.removeItem("coachx_chat_history");
      // Redirect to home page
      navigate("/");
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Failed to reset profile"
      );
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <LoadingSpinner size="lg" message="Loading your dashboard..." />;
  }

  if (!profile) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="text-center">
          <p className="text-gray-600 mb-4">No profile found</p>
          <button
            onClick={() => navigate("/onboarding")}
            className="btn-primary"
          >
            Complete Onboarding
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black py-4 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Logo and Header */}
        <div className="mb-6 flex flex-col md:flex-row justify-between items-start md:items-center">
          <div className="flex items-center gap-4">
            <img src="/coachx.svg" alt="CoachX Logo" className="h-12 w-auto" />
            <div>
              <h1 className="text-2xl font-bold text-white">
                {profile.full_name} - {profile.primary_sport}
              </h1>
              <p className="text-sm text-gray-400 mt-1">
                {profile.available_days_per_week} days/week
              </p>
            </div>
          </div>
          <div className="flex gap-2 mt-3 md:mt-0">
            <button
              onClick={() => setShowGenerateModal(true)}
              className="btn-primary"
            >
              Generate Workout Plan
            </button>
            <button
              onClick={handleResetProfile}
              className="px-4 py-2 bg-gray-800 text-gray-300 rounded hover:bg-gray-700 text-sm"
              title="Reset profile and start over"
            >
              Reset
            </button>
          </div>
        </div>

        {error && <ErrorMessage error={error} onRetry={loadDashboardData} />}

        {/* Main Layout: Chat First (Primary), Plan Second (Collapsible) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* AI CHAT - PRIMARY FEATURE (2/3 width on large screens) */}
          <div className="lg:col-span-2 order-1">
            <div className="card">
              <div className="mb-4 border-b border-gray-800 pb-3">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                  AI Training Coach
                </h2>
                <p className="text-sm text-gray-400 mt-1">
                  Ask me anything about your training, nutrition, technique, or
                  recovery
                </p>
              </div>
              <ChatSection
                userSport={profile?.primary_sport}
                onPlanUpdate={loadDashboardData}
              />
            </div>
          </div>

          {/* WORKOUT PLAN - SECONDARY (1/3 width, collapsible) */}
          <div className="lg:col-span-1 order-2">
            {activePlan ? (
              <div className="card">
                <div className="mb-4 border-b border-gray-800 pb-3">
                  <h3 className="text-lg font-bold text-white">Current Plan</h3>
                  <p className="text-sm text-gray-400 mt-1">
                    {activePlan.title}
                  </p>
                </div>
                <WorkoutPlanSummary plan={activePlan} />
                <button
                  onClick={() => navigate("/workout-plan")}
                  className="btn-secondary w-full mt-4"
                >
                  View Full Plan
                </button>
              </div>
            ) : (
              <div className="card text-center py-8">
                <div className="text-5xl mb-3">📋</div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  No Active Plan
                </h3>
                <p className="text-sm text-gray-400 mb-4">
                  Generate your first workout plan
                </p>
                <button
                  onClick={() => setShowGenerateModal(true)}
                  className="btn-primary w-full"
                >
                  Generate Plan
                </button>
              </div>
            )}

            {/* Quick Profile Stats */}
            <div className="card mt-6">
              <h3 className="text-sm font-semibold text-gray-400 uppercase mb-3">
                Quick Stats
              </h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Age</span>
                  <span className="text-white font-medium">{profile.age}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Height</span>
                  <span className="text-white font-medium">
                    {profile.height_cm} cm
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Weight</span>
                  <span className="text-white font-medium">
                    {profile.weight_kg} kg
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Location</span>
                  <span className="text-white font-medium capitalize">
                    {profile.training_location}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

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

// ============================================================================
// WorkoutPlanSummary Component - Compact sidebar view
// ============================================================================

function WorkoutPlanSummary({ plan }: { plan: WorkoutPlan }) {
  const weeks = Object.keys(plan.plan_structure).sort();
  const firstWeek = weeks[0];
  const days = plan.plan_structure[firstWeek];

  return (
    <div className="space-y-3">
      <div className="text-sm text-gray-400">
        <span className="font-medium text-white">{plan.duration_weeks}</span>{" "}
        week plan
        {" • "}
        <span className="font-medium text-white">{days.length}</span> days/week
      </div>

      <div className="space-y-2">
        <p className="text-xs font-semibold text-gray-500 uppercase">
          This Week
        </p>
        {days.map((day, idx) => (
          <div
            key={idx}
            className="bg-gray-900 p-3 rounded border border-gray-800"
          >
            <div className="flex justify-between items-start mb-1">
              <span className="font-medium text-white text-sm">{day.day}</span>
              <span className="text-xs text-gray-500">
                {day.duration_minutes || day.duration_min}min
              </span>
            </div>
            <p className="text-xs text-gray-400">{day.focus}</p>
            <p className="text-xs text-gray-500 mt-1">
              {day.exercises.length} exercises
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

// ============================================================================
// WorkoutPlanDisplay Component - Full detailed view
// ============================================================================
// @ts-ignore - Unused component kept for future use
// eslint-disable-next-line @typescript-eslint/no-unused-vars
function WorkoutPlanDisplay({ plan }: { plan: WorkoutPlan }) {
  const [expandedWeeks, setExpandedWeeks] = useState<Set<string>>(
    new Set(["week_1"])
  );
  const [expandedDays, setExpandedDays] = useState<Set<string>>(new Set());

  const toggleWeek = (week: string) => {
    const newExpanded = new Set(expandedWeeks);
    if (newExpanded.has(week)) {
      newExpanded.delete(week);
    } else {
      newExpanded.add(week);
    }
    setExpandedWeeks(newExpanded);
  };

  const toggleDay = (dayId: string) => {
    const newExpanded = new Set(expandedDays);
    if (newExpanded.has(dayId)) {
      newExpanded.delete(dayId);
    } else {
      newExpanded.add(dayId);
    }
    setExpandedDays(newExpanded);
  };

  const weeks = Object.keys(plan.plan_structure).sort();

  return (
    <div className="space-y-4">
      {weeks.map((week) => {
        const weekNumber = week.replace("week_", "");
        const days = plan.plan_structure[week];
        const isWeekExpanded = expandedWeeks.has(week);

        return (
          <div
            key={week}
            className="border border-gray-200 rounded-lg overflow-hidden"
          >
            {/* Week Header */}
            <button
              onClick={() => toggleWeek(week)}
              className="w-full flex items-center justify-between p-4 bg-gray-800 hover:bg-gray-700 transition-colors"
            >
              <h3 className="text-lg font-semibold text-white">
                Week {weekNumber}
              </h3>
              <svg
                className={`h-5 w-5 text-gray-400 transition-transform ${
                  isWeekExpanded ? "transform rotate-180" : ""
                }`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>

            {/* Week Content */}
            {isWeekExpanded && (
              <div className="p-4 space-y-3">
                {days.map((day, dayIndex) => {
                  const dayId = `${week}_${dayIndex}`;
                  const isDayExpanded = expandedDays.has(dayId);

                  return (
                    <div
                      key={dayId}
                      className="border border-gray-200 rounded-lg overflow-hidden"
                    >
                      {/* Day Header */}
                      <button
                        onClick={() => toggleDay(dayId)}
                        className="w-full flex items-center justify-between p-3 bg-gray-900 hover:bg-gray-800 transition-colors"
                      >
                        <div className="text-left">
                          <h4 className="font-semibold text-white">
                            {day.day}
                          </h4>
                          <p className="text-sm text-gray-400">{day.focus}</p>
                          <p className="text-xs text-gray-500">
                            {day.duration_minutes || day.duration_min} minutes
                          </p>
                        </div>
                        <svg
                          className={`h-4 w-4 text-gray-400 transition-transform ${
                            isDayExpanded ? "transform rotate-180" : ""
                          }`}
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 9l-7 7-7-7"
                          />
                        </svg>
                      </button>

                      {/* Day Content */}
                      {isDayExpanded && (
                        <div className="p-4 bg-black space-y-3">
                          {/* Warmup */}
                          <div>
                            <p className="text-xs font-medium text-gray-500 uppercase">
                              Warmup
                            </p>
                            <p className="text-sm text-gray-300">
                              {day.warmup}
                            </p>
                          </div>

                          {/* Exercises */}
                          <div>
                            <p className="text-xs font-medium text-gray-500 uppercase mb-2">
                              Exercises
                            </p>
                            <div className="space-y-2">
                              {day.exercises.map((exercise, exIndex) => (
                                <div
                                  key={exIndex}
                                  className="bg-gray-900 p-3 rounded border border-gray-700"
                                >
                                  <h5 className="font-medium text-white">
                                    {exercise.name}
                                  </h5>
                                  <div className="flex flex-wrap gap-4 mt-1 text-sm text-gray-400">
                                    <span>Sets: {exercise.sets}</span>
                                    <span>Reps: {exercise.reps}</span>
                                    <span>Rest: {exercise.rest_seconds}s</span>
                                  </div>
                                  {exercise.notes && (
                                    <p className="text-xs text-gray-500 mt-1 italic">
                                      {exercise.notes}
                                    </p>
                                  )}
                                </div>
                              ))}
                            </div>
                          </div>

                          {/* Cooldown */}
                          <div>
                            <p className="text-xs font-medium text-gray-500 uppercase">
                              Cooldown
                            </p>
                            <p className="text-sm text-gray-300">
                              {day.cooldown}
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

// ============================================================================
// GeneratePlanModal Component
// ============================================================================

function GeneratePlanModal({
  params,
  setParams,
  isGenerating,
  onGenerate,
  onClose,
}: {
  params: GeneratePlanParams;
  setParams: (params: GeneratePlanParams) => void;
  isGenerating: boolean;
  onGenerate: () => void;
  onClose: () => void;
}) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div className="bg-gray-900 border border-gray-800 rounded-lg max-w-md w-full p-6">
        <h3 className="text-xl font-bold text-white mb-4">
          Generate New Workout Plan
        </h3>

        {isGenerating ? (
          <div className="py-8">
            <LoadingSpinner
              size="md"
              message="Generating your personalized plan..."
            />
            <p className="text-center text-sm text-gray-400 mt-4">
              This may take 10-30 seconds
            </p>
          </div>
        ) : (
          <>
            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Duration (weeks)
                </label>
                <input
                  type="number"
                  value={params.duration_weeks}
                  onChange={(e) =>
                    setParams({
                      ...params,
                      duration_weeks: Number(e.target.value),
                    })
                  }
                  min="1"
                  max="2"
                  className="input"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Between 1 and 2 weeks
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Custom Notes (optional)
                </label>
                <textarea
                  value={params.custom_notes}
                  onChange={(e) =>
                    setParams({ ...params, custom_notes: e.target.value })
                  }
                  rows={3}
                  className="input resize-none"
                  placeholder="Any specific requests or preferences..."
                />
              </div>
            </div>

            <div className="flex justify-end space-x-3">
              <button onClick={onClose} className="btn-secondary">
                Cancel
              </button>
              <button onClick={onGenerate} className="btn-primary">
                Generate Plan
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
