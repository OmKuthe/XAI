// components/EventCard.jsx
import { useState } from "react";

const EventCard = ({ event, rank, onFeedback }) => {
  const [showDetails, setShowDetails] = useState(false);
  const [feedbackGiven, setFeedbackGiven] = useState(false);
  const [imageError, setImageError] = useState(false);

  if (!event) return null;

  const matchScore = event.score || 0;
  const scoreColor = matchScore >= 70 ? "text-green-600" : matchScore >= 40 ? "text-yellow-600" : "text-orange-600";
  const scoreBgColor = matchScore >= 70 ? "bg-green-100" : matchScore >= 40 ? "bg-yellow-100" : "bg-orange-100";

  // Generate gradient based on rank
  const rankGradients = {
    1: "from-yellow-400 to-orange-500",
    2: "from-gray-400 to-gray-500",
    3: "from-orange-400 to-brown-500"
  };
  const rankGradient = rankGradients[rank] || "from-blue-400 to-purple-500";

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
      {/* Header with Rank Badge */}
      <div className={`bg-gradient-to-r ${rankGradient} px-4 py-3 relative`}>
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="bg-white bg-opacity-30 rounded-full w-8 h-8 flex items-center justify-center font-bold text-white">
              #{rank}
            </div>
            <span className="text-white text-sm font-medium">
              {event.event_type || "Event"}
            </span>
          </div>
          <div className={`${scoreBgColor} rounded-full px-3 py-1`}>
            <span className={`text-sm font-bold ${scoreColor}`}>
              {Math.round(matchScore)}% Match
            </span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-5">
        {/* Event Title */}
        <h3 className="text-xl font-bold text-gray-800 mb-2 line-clamp-2">
          {event.event}
        </h3>
        
        {/* College & Location */}
        <div className="flex items-center justify-between text-sm text-gray-600 mb-3">
          <div className="flex items-center space-x-1">
            <span>🏛️</span>
            <span className="font-medium">{event.college || "College"}</span>
          </div>
          <div className="flex items-center space-x-1">
            <span>📍</span>
            <span>{event.city}</span>
          </div>
        </div>

        {/* Description */}
        <p className="text-gray-600 text-sm mb-4 line-clamp-3">
          {event.description}
        </p>

        {/* Key Info Chips */}
        <div className="flex flex-wrap gap-2 mb-4">
          {event.category && (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              📂 {event.category}
            </span>
          )}
          {event.price === 0 ? (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
              🆓 Free
            </span>
          ) : (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
              💰 ₹{event.price}
            </span>
          )}
          {event.rating > 0 && (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
              ⭐ {event.rating}/5
            </span>
          )}
          {event.team_info && (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
              👥 {event.team_info}
            </span>
          )}
        </div>

        {/* Prize Info */}
        {event.prize_info && (
          <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg p-2 mb-4 text-sm">
            <span className="font-semibold text-orange-700">{event.prize_info}</span>
          </div>
        )}

        {/* XAI Explanation Button */}
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="w-full text-left text-sm text-blue-600 hover:text-blue-800 font-medium mb-3 focus:outline-none flex items-center justify-between"
        >
          <span>{showDetails ? "▼ Hide AI Explanation" : "▶ Why this recommendation?"}</span>
          <span className="text-xs">🤖 XAI</span>
        </button>

        {/* Detailed XAI Explanations */}
        {showDetails && (
          <div className="mt-3 space-y-3 text-sm border-t pt-3 animate-slideDown">
            {/* Positive Factors */}
            {event.explanation && event.explanation.length > 0 && (
              <div>
                <h4 className="font-semibold text-green-700 mb-2 flex items-center">
                  <span className="text-lg mr-1">✅</span> Why this?
                </h4>
                <ul className="space-y-1">
                  {event.explanation.map((exp, i) => (
                    <li key={i} className="text-gray-700 flex items-start">
                      <span className="mr-2 text-green-500">•</span>
                      <span>{exp}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Negative Factors */}
            {event.why_not && event.why_not.length > 0 && (
              <div>
                <h4 className="font-semibold text-orange-700 mb-2 flex items-center">
                  <span className="text-lg mr-1">⚠️</span> Considerations
                </h4>
                <ul className="space-y-1">
                  {event.why_not.map((concern, i) => (
                    <li key={i} className="text-gray-700 flex items-start">
                      <span className="mr-2 text-orange-500">•</span>
                      <span>{concern}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Additional Info */}
            {event.start_date && (
              <div className="flex items-center text-sm text-gray-500 mt-2 mb-2">
                <span className="mr-1">📅</span>
                <span>Date: {new Date(event.start_date).toLocaleDateString('en-IN', {
                  day: 'numeric',
                  month: 'long',
                  year: 'numeric'
                })}</span>
              </div>
            )}
          </div>
        )}

        {/* Registration Link */}
        {event.registration_link && event.registration_link !== "#" && (
          <a
            href={event.registration_link}
            target="_blank"
            rel="noopener noreferrer"
            className="block mt-4 text-center bg-gradient-to-r from-blue-500 to-purple-500 text-white py-2 rounded-lg hover:from-blue-600 hover:to-purple-600 transition text-sm font-medium"
          >
            Register Now →
          </a>
        )}

        {/* Feedback Buttons */}
        {!feedbackGiven && onFeedback && (
          <div className="mt-4 pt-3 border-t flex justify-end space-x-2">
            <button
              onClick={() => {
                onFeedback(event.id, 'helpful');
                setFeedbackGiven(true);
              }}
              className="text-xs px-3 py-1 bg-green-50 text-green-700 rounded-full hover:bg-green-100 transition"
            >
              👍 Helpful
            </button>
            <button
              onClick={() => {
                onFeedback(event.id, 'not_helpful');
                setFeedbackGiven(true);
              }}
              className="text-xs px-3 py-1 bg-red-50 text-red-700 rounded-full hover:bg-red-100 transition"
            >
              👎 Not Helpful
            </button>
          </div>
        )}

        {feedbackGiven && (
          <div className="mt-4 pt-3 border-t text-center text-xs text-gray-500">
            Thanks for your feedback! 🙏
          </div>
        )}
      </div>
    </div>
  );
};

export default EventCard;