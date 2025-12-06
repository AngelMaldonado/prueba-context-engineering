/**
 * API Client for CoachX Backend
 *
 * Connects to FastAPI backend running on localhost:8000
 */

import axios from 'axios';

// Base API URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 120 seconds for AI operations (plan generation can take time)
});

// Request interceptor for logging (dev only)
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('[API Error]', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// ============================================================================
// Profile API
// ============================================================================

export const profileApi = {
  /**
   * Get profile status (exists, completion %)
   */
  getStatus: async () => {
    const response = await apiClient.get('/api/profile/status');
    return response.data;
  },

  /**
   * Get full user profile
   */
  getProfile: async () => {
    const response = await apiClient.get('/api/profile');
    return response.data;
  },

  /**
   * Create or update profile with onboarding data
   */
  submitOnboarding: async (data: any) => {
    const response = await apiClient.post('/api/profile/onboarding', data);
    return response.data;
  },

  /**
   * Update profile
   */
  updateProfile: async (data: any) => {
    const response = await apiClient.put('/api/profile', data);
    return response.data;
  },

  /**
   * Reset profile and all data (for testing)
   */
  resetProfile: async () => {
    const response = await apiClient.delete('/api/profile');
    return response.data;
  },
};

// ============================================================================
// Workout Plans API
// ============================================================================

export const workoutApi = {
  /**
   * Generate new workout plan
   */
  generatePlan: async (params: {
    duration_weeks: number;
    custom_notes?: string;
  }) => {
    const response = await apiClient.post('/api/workouts/generate', params);
    return response.data;
  },

  /**
   * Get all workout plans
   */
  getAllPlans: async (includeCompleted: boolean = false) => {
    const response = await apiClient.get('/api/workouts', {
      params: { include_completed: includeCompleted },
    });
    return response.data;
  },

  /**
   * Get active workout plan
   */
  getActivePlan: async () => {
    const response = await apiClient.get('/api/workouts/active');
    return response.data;
  },

  /**
   * Get specific workout plan by ID
   */
  getPlan: async (planId: number) => {
    const response = await apiClient.get(`/api/workouts/${planId}`);
    return response.data;
  },

  /**
   * Activate a workout plan
   */
  activatePlan: async (planId: number) => {
    const response = await apiClient.post(`/api/workouts/${planId}/activate`);
    return response.data;
  },

  /**
   * Mark workout plan as completed
   */
  completePlan: async (planId: number) => {
    const response = await apiClient.post(`/api/workouts/${planId}/complete`);
    return response.data;
  },

  /**
   * Delete workout plan
   */
  deletePlan: async (planId: number) => {
    const response = await apiClient.delete(`/api/workouts/${planId}`);
    return response.data;
  },
};

// ============================================================================
// AI Chat API
// ============================================================================

export const chatApi = {
  /**
   * Send chat message to AI with conversation history
   */
  sendMessage: async (params: {
    q: string;
    sport?: string;
    top_k?: number;
    conversation_history?: Array<{ role: string; content: string }>;
  }) => {
    const response = await apiClient.post('/ai/chat', params);
    return response.data;
  },

  /**
   * Test Gemini connection
   */
  testConnection: async () => {
    const response = await apiClient.get('/ai/test');
    return response.data;
  },
};

// ============================================================================
// RAG System API (for testing/debugging)
// ============================================================================

export const ragApi = {
  /**
   * Get RAG system stats
   */
  getStats: async () => {
    const response = await apiClient.get('/rag/stats');
    return response.data;
  },

  /**
   * Query RAG system directly
   */
  query: async (params: {
    q: string;
    sport?: string;
    top_k?: number;
  }) => {
    const response = await apiClient.get('/rag/query', { params });
    return response.data;
  },
};

// ============================================================================
// Health Check
// ============================================================================

export const healthApi = {
  /**
   * Check if backend is healthy
   */
  check: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

// Default export
export default {
  profile: profileApi,
  workout: workoutApi,
  chat: chatApi,
  rag: ragApi,
  health: healthApi,
};
