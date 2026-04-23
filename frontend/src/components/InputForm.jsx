// components/InputForm.jsx
import { useState } from "react";

const InputForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    interest: "",
    city: "Pune",
    budget: 1000,
    event_type: "Both"
  });

  const cities = [
    "Mumbai", "Pune", "Nagpur", "Navi Mumbai", 
    "Aurangabad", "Nanded", "Sangli", "Kolhapur", "Nashik"
  ];

  const eventTypes = ["Solo", "Team", "Both"];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === "budget" ? Number(value) : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.interest.trim()) {
      onSubmit(formData);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-4">
        <h2 className="text-xl font-bold text-white flex items-center">
          <span className="text-2xl mr-2">🎉</span>
          Find Your Perfect Event
        </h2>
        <p className="text-blue-100 text-sm mt-1">
          Tell us what you're looking for and we'll recommend the best events
        </p>
      </div>
      
      <form onSubmit={handleSubmit} className="p-6 space-y-5">
        {/* Interest Field */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            💡 What are you interested in?
          </label>
          <input
            type="text"
            name="interest"
            value={formData.interest}
            onChange={handleChange}
            placeholder="e.g., robotics, coding, hackathon, workshop, design..."
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
            required
          />
          <p className="text-xs text-gray-500 mt-1">
            Enter keywords like "robotics competition", "coding hackathon", "AI workshop"
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* City Selection */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              📍 City
            </label>
            <select
              name="city"
              value={formData.city}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {cities.map(city => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>

          {/* Budget Field */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              💰 Budget (₹)
            </label>
            <input
              type="number"
              name="budget"
              value={formData.budget}
              onChange={handleChange}
              min="0"
              step="100"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Event Type */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              👥 Event Type
            </label>
            <select
              name="event_type"
              value={formData.event_type}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {eventTypes.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || !formData.interest.trim()}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-700 hover:to-purple-700 transition transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Finding Events...
            </span>
          ) : (
            "🔍 Get Recommendations"
          )}
        </button>
      </form>
    </div>
  );
};

export default InputForm;