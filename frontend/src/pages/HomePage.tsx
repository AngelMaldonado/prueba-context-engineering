/**
 * HomePage Component
 *
 * Landing page with hero section and backend health check
 */

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { healthApi } from "../lib/api";
import LoadingSpinner from "../components/LoadingSpinner";

export default function HomePage() {
  const [backendStatus, setBackendStatus] = useState<
    "loading" | "online" | "offline"
  >("loading");
  const navigate = useNavigate();

  useEffect(() => {
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      await healthApi.check();
      setBackendStatus("online");
    } catch (error) {
      console.error("Backend health check failed:", error);
      setBackendStatus("offline");
    }
  };

  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center px-4">
      {/* Hero Section */}
      <div className="max-w-3xl mx-auto text-center">
        <h1 className="text-6xl font-bold text-white mb-4">
          Coach<span className="text-red-600">X</span>
        </h1>
        <p className="text-xl text-gray-300 mb-2">
          Your AI-Powered Personal Training Assistant
        </p>
        <p className="text-lg text-gray-400 mb-8">
          Get personalized workout plans powered by AI and sports science
          research
        </p>

        <button
          onClick={() => navigate("/onboarding")}
          className="btn-primary text-lg px-8 py-3 transform hover:scale-105 transition-transform"
        >
          Get Started
        </button>
      </div>
    </div>
  );
}
