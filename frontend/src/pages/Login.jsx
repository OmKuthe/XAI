// pages/Login.jsx
import { useState } from "react";
import Footer from "../components/Footer";

const Login = ({ onLogin }) => {
  const [selectedRole, setSelectedRole] = useState("student");
  const [loading, setLoading] = useState(false);

  // Predefined credentials for demonstration
  const credentials = {
    student: {
      email: "student@example.com",
      password: "student123",
      role: "student"
    },
    organizer: {
      email: "organizer@example.com",
      password: "organizer123",
      role: "organizer"
    },
    admin: {
      email: "admin@example.com",
      password: "admin123",
      role: "admin"
    }
  };

  const handleLogin = (role) => {
    setLoading(true);
    setSelectedRole(role);
    
    // Simulate API call
    setTimeout(() => {
      const userData = credentials[role];
      onLogin(userData);
      setLoading(false);
    }, 500);
  };

  const handleAutoFill = (role) => {
    setSelectedRole(role);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="container mx-auto px-4 py-6 max-w-7xl">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Event Discovery Platform</h1>
              <p className="text-gray-600 text-sm mt-1">Explainable AI for Personalized Event Recommendations</p>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-12 max-w-7xl">
        <div className="max-w-md mx-auto">
          {/* Login Card */}
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="bg-gray-900 px-6 py-4">
              <h2 className="text-xl font-semibold text-white">Access Platform</h2>
              <p className="text-gray-400 text-sm mt-1">Select your role to continue</p>
            </div>

            <div className="p-6">
              {/* Role Selection */}
              <div className="space-y-4">
                {/* Student Login */}
                <div 
                  className={`border rounded-lg p-4 cursor-pointer transition ${
                    selectedRole === "student" ? "border-blue-500 bg-blue-50" : "border-gray-200 hover:border-blue-300"
                  }`}
                  onClick={() => handleAutoFill("student")}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <svg className="w-5 h-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">Student</h3>
                        <p className="text-sm text-gray-600">Discover and register for events</p>
                      </div>
                    </div>
                    <div className="text-xs text-gray-500">Click to autofill</div>
                  </div>
                  
                  {selectedRole === "student" && (
                    <div className="mt-4 space-y-3 pt-3 border-t border-gray-200">
                      <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Email</label>
                        <input
                          type="email"
                          value={credentials.student.email}
                          readOnly
                          className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-600 text-sm"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Password</label>
                        <input
                          type="password"
                          value={credentials.student.password}
                          readOnly
                          className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-600 text-sm"
                        />
                      </div>
                      <button
                        onClick={() => handleLogin("student")}
                        disabled={loading}
                        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition font-medium disabled:opacity-50"
                      >
                        {loading && selectedRole === "student" ? "Signing in..." : "Sign in as Student"}
                      </button>
                    </div>
                  )}
                </div>

                {/* Organizer Login */}
                <div 
                  className={`border rounded-lg p-4 cursor-pointer transition ${
                    selectedRole === "organizer" ? "border-green-500 bg-green-50" : "border-gray-200 hover:border-green-300"
                  }`}
                  onClick={() => handleAutoFill("organizer")}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                        <svg className="w-5 h-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">Event Organizer</h3>
                        <p className="text-sm text-gray-600">Manage and promote your events</p>
                      </div>
                    </div>
                    <div className="text-xs text-gray-500">Click to autofill</div>
                  </div>
                  
                  {selectedRole === "organizer" && (
                    <div className="mt-4 space-y-3 pt-3 border-t border-gray-200">
                      <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Email</label>
                        <input
                          type="email"
                          value={credentials.organizer.email}
                          readOnly
                          className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-600 text-sm"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Password</label>
                        <input
                          type="password"
                          value={credentials.organizer.password}
                          readOnly
                          className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-600 text-sm"
                        />
                      </div>
                      <button
                        onClick={() => handleLogin("organizer")}
                        disabled={loading}
                        className="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition font-medium disabled:opacity-50"
                      >
                        {loading && selectedRole === "organizer" ? "Signing in..." : "Sign in as Organizer"}
                      </button>
                    </div>
                  )}
                </div>

                {/* Admin Login */}
                <div 
                  className={`border rounded-lg p-4 cursor-pointer transition ${
                    selectedRole === "admin" ? "border-purple-500 bg-purple-50" : "border-gray-200 hover:border-purple-300"
                  }`}
                  onClick={() => handleAutoFill("admin")}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                        <svg className="w-5 h-5 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">Administrator</h3>
                        <p className="text-sm text-gray-600">Full system access and control</p>
                      </div>
                    </div>
                    <div className="text-xs text-gray-500">Click to autofill</div>
                  </div>
                  
                  {selectedRole === "admin" && (
                    <div className="mt-4 space-y-3 pt-3 border-t border-gray-200">
                      <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Email</label>
                        <input
                          type="email"
                          value={credentials.admin.email}
                          readOnly
                          className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-600 text-sm"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Password</label>
                        <input
                          type="password"
                          value={credentials.admin.password}
                          readOnly
                          className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-600 text-sm"
                        />
                      </div>
                      <button
                        onClick={() => handleLogin("admin")}
                        disabled={loading}
                        className="w-full bg-purple-600 text-white py-2 rounded-md hover:bg-purple-700 transition font-medium disabled:opacity-50"
                      >
                        {loading && selectedRole === "admin" ? "Signing in..." : "Sign in as Admin"}
                      </button>
                    </div>
                  )}
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-gray-200">
                <p className="text-xs text-gray-500 text-center">
                  Demo credentials are pre-filled. Click on any role card to autofill, then sign in.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default Login;