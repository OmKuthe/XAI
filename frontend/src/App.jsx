// App.jsx
import { useState } from "react";
import Login from "./pages/Login";
import StudentDashboard from "./pages/StudentDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import OrganizerDashboard from "./pages/OrganizerDashboard";

function App() {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = (userData) => {
    setUser(userData);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setUser(null);
    setIsAuthenticated(false);
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  // Render appropriate dashboard based on role
  switch (user?.role) {
    case "admin":
      return <AdminDashboard user={user} onLogout={handleLogout} />;
    case "organizer":
      return <OrganizerDashboard user={user} onLogout={handleLogout} />;
    default:
      return <StudentDashboard user={user} onLogout={handleLogout} />;
  }
}

export default App;