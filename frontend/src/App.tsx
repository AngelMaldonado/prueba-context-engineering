/**
 * Main App Component with Router Configuration
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import OnboardingPage from './pages/OnboardingPage';
import DashboardPage from './pages/DashboardPage';
import WorkoutPlanPage from './pages/WorkoutPlanPage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/workout-plan" element={<WorkoutPlanPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
