// StudentDashboard.jsx
import { useState } from "react";
import InputForm from "../components/InputForm"
import EventCard from "../components/EventCard";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorBoundary from "../components/ErrorBoundary";
import Header from "../components/Header";
import Footer from "../components/Footer";

const StudentDashboard = ({ user, onLogout }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [userPreferences, setUserPreferences] = useState(null);
  const [showResults, setShowResults] = useState(false);

  const handleSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    setShowResults(false);
    setUserPreferences(formData); 
    
    try {
      const response = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          interest: formData.interest,
          city: formData.city,
          budget: Number(formData.budget),
          event_type: formData.event_type
        }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        setRecommendations(data.recommendations);
        setShowResults(true);
      } else {
        setError(data.error || "Failed to get recommendations");
      }
    } catch (err) {
      console.error("Fetch error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (eventId, feedback) => {
    try {
      await fetch("http://127.0.0.1:5000/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          event_id: eventId, 
          feedback, 
          preferences: userPreferences 
        })
      });
    } catch (err) {
      console.error("Feedback error:", err);
    }
  };

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
        <Header />
        
        <main className="container mx-auto px-4 py-8 max-w-7xl">
          {/* Input Form Section */}
          <div className="mb-10">
            <InputForm onSubmit={handleSubmit} loading={loading} />
          </div>

          {/* Loading State */}
          {loading && <LoadingSpinner />}
          
          {/* Error State */}
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg mb-6 shadow-md">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">Error</h3>
                  <p className="text-sm text-red-700 mt-1">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Results Section */}
          {showResults && !loading && !error && (
            <div className="animate-fadeIn">
              {/* User Preferences Summary */}
              <div className="bg-white rounded-xl shadow-md p-5 mb-8 border border-gray-100">
                <h2 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                  <span className="text-2xl mr-2">🎯</span>
                  Your Preferences
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div className="flex items-center space-x-2">
                    <span className="text-blue-500">💡</span>
                    <span className="text-gray-600">Interest:</span>
                    <span className="font-medium text-gray-800">{userPreferences?.interest}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-green-500">📍</span>
                    <span className="text-gray-600">City:</span>
                    <span className="font-medium text-gray-800">{userPreferences?.city}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-yellow-500">💰</span>
                    <span className="text-gray-600">Budget:</span>
                    <span className="font-medium text-gray-800">₹{userPreferences?.budget}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-purple-500">👥</span>
                    <span className="text-gray-600">Event Type:</span>
                    <span className="font-medium text-gray-800">{userPreferences?.event_type}</span>
                  </div>
                </div>
              </div>

              {/* Results Header */}
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center">
                  <span className="text-3xl mr-2">✨</span>
                  Top Recommendations for You
                </h2>
                <p className="text-gray-600">
                  Found {recommendations.length} events matching your preferences
                </p>
              </div>

              {/* Event Cards Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendations.map((event, index) => (
                  <EventCard 
                    key={event.id || index} 
                    event={event} 
                    rank={index + 1}
                    onFeedback={handleFeedback}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Empty State */}
          {!showResults && !loading && !error && (
            <div className="text-center py-16">
              <div className="text-gray-400 mb-6">
                <svg className="h-24 w-24 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-600 mb-2">
                Ready to Discover Amazing Events?
              </h3>
              <p className="text-gray-500 max-w-md mx-auto">
                Fill out the form above with your interests, location, and budget to get personalized event recommendations powered by AI.
              </p>
            </div>
          )}
        </main>

        <Footer />
      </div>
    </ErrorBoundary>
  );
}

export default StudentDashboard;