/**
 * WorkoutPlanPage Component
 *
 * Displays the full detailed workout plan
 */

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { workoutApi } from "../lib/api";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorMessage from "../components/ErrorMessage";
import type { WorkoutPlan } from "../types";

export default function WorkoutPlanPage() {
  const [plan, setPlan] = useState<WorkoutPlan | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedWeeks, setExpandedWeeks] = useState<Set<string>>(
    new Set(["week_1"])
  );
  const [expandedDays, setExpandedDays] = useState<Set<string>>(new Set());
  const navigate = useNavigate();

  useEffect(() => {
    loadPlan();
  }, []);

  const loadPlan = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const planData = await workoutApi.getActivePlan();
      setPlan(planData);
    } catch (err: any) {
      if (err.response?.status === 404) {
        setError(
          "No active workout plan found. Generate one from the dashboard."
        );
      } else {
        setError(
          err.response?.data?.detail ||
            err.message ||
            "Failed to load workout plan"
        );
      }
    } finally {
      setIsLoading(false);
    }
  };

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

  if (isLoading) {
    return <LoadingSpinner size="lg" message="Loading your workout plan..." />;
  }

  if (error || !plan) {
    return (
      <div className="min-h-screen bg-black py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <button
            onClick={() => navigate("/dashboard")}
            className="mb-6 text-gray-400 hover:text-white flex items-center gap-2"
          >
            ← Back to Dashboard
          </button>
          {error && <ErrorMessage error={error} onRetry={loadPlan} />}
          {!error && !plan && (
            <div className="card text-center py-12">
              <h3 className="text-xl font-semibold text-white mb-4">
                No Workout Plan Found
              </h3>
              <button
                onClick={() => navigate("/dashboard")}
                className="btn-primary"
              >
                Go to Dashboard
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  const weeks = Object.keys(plan.plan_structure).sort();

  return (
    <div className="min-h-screen bg-black py-8 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header with Logo */}
        <div className="mb-6">
          <button
            onClick={() => navigate("/dashboard")}
            className="mb-4 text-gray-400 hover:text-white flex items-center gap-2"
          >
            ← Back to Dashboard
          </button>

          <div className="flex items-center gap-4 mb-4">
            <img src="/coachx.svg" alt="CoachX Logo" className="h-10 w-auto" />
            <h1 className="text-3xl font-bold text-white">{plan.title}</h1>
          </div>

          {plan.description && (
            <p className="text-gray-400">{plan.description}</p>
          )}
          <div className="flex gap-4 text-sm text-gray-500 mt-2">
            <span>{plan.duration_weeks} weeks</span>
            <span>•</span>
            <span>
              Created {new Date(plan.created_at).toLocaleDateString()}
            </span>
          </div>
        </div>

        {/* Workout Plan */}
        <div className="space-y-4">
          {weeks.map((week) => {
            const weekNumber = week.replace("week_", "");
            const days = plan.plan_structure[week];
            const isWeekExpanded = expandedWeeks.has(week);

            return (
              <div
                key={week}
                className="border border-gray-800 rounded-lg overflow-hidden"
              >
                {/* Week Header */}
                <button
                  onClick={() => toggleWeek(week)}
                  className="w-full flex items-center justify-between p-4 bg-gray-900 hover:bg-gray-800 transition-colors"
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
                  <div className="p-4 space-y-3 bg-black">
                    {days.map((day, dayIndex) => {
                      const dayId = `${week}_${dayIndex}`;
                      const isDayExpanded = expandedDays.has(dayId);

                      return (
                        <div
                          key={dayId}
                          className="border border-gray-800 rounded-lg overflow-hidden"
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
                              <p className="text-sm text-gray-400">
                                {day.focus}
                              </p>
                              <p className="text-xs text-gray-500">
                                {day.duration_minutes || day.duration_min}{" "}
                                minutes
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
                              {day.warmup && (
                                <div>
                                  <p className="text-xs font-medium text-gray-500 uppercase">
                                    Warmup
                                  </p>
                                  <p className="text-sm text-gray-300">
                                    {day.warmup}
                                  </p>
                                </div>
                              )}

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
                                        {exercise.rest_seconds && (
                                          <span>
                                            Rest: {exercise.rest_seconds}s
                                          </span>
                                        )}
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
                              {day.cooldown && (
                                <div>
                                  <p className="text-xs font-medium text-gray-500 uppercase">
                                    Cooldown
                                  </p>
                                  <p className="text-sm text-gray-300">
                                    {day.cooldown}
                                  </p>
                                </div>
                              )}
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
      </div>
    </div>
  );
}
