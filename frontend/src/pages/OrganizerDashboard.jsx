// pages/OrganizerDashboard.jsx
import { useState } from "react";

const OrganizerDashboard = ({ user, onLogout }) => {
  const [myEvents, setMyEvents] = useState([
    { id: 1, name: "Annual Tech Fest", date: "2024-12-15", registrations: 45, capacity: 200, status: "Active" },
    { id: 2, name: "Coding Workshop", date: "2024-11-20", registrations: 78, capacity: 100, status: "Active" },
  ]);
  const [showCreateForm, setShowCreateForm] = useState(false);

  const handleCreateEvent = (eventData) => {
    // Handle event creation - API call would go here
    console.log("Creating event:", eventData);
    setShowCreateForm(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Organizer Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="container mx-auto px-4 py-4 max-w-7xl">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-xl font-bold text-gray-900">Organizer Dashboard</h1>
              <p className="text-gray-600 text-sm">Manage your events and track registrations</p>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">{user.email}</span>
              <button
                onClick={onLogout}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition text-sm"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-500 text-sm">Total Events</p>
            <p className="text-2xl font-bold text-gray-900">{myEvents.length}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-500 text-sm">Total Registrations</p>
            <p className="text-2xl font-bold text-gray-900">
              {myEvents.reduce((sum, event) => sum + event.registrations, 0)}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-500 text-sm">Active Events</p>
            <p className="text-2xl font-bold text-gray-900">
              {myEvents.filter(e => e.status === "Active").length}
            </p>
          </div>
        </div>

        {/* Create Event Button */}
        <div className="mb-6">
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          >
            {showCreateForm ? "Cancel" : "+ Create New Event"}
          </button>
        </div>

        {/* Create Event Form */}
        {showCreateForm && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Event</h3>
            <form onSubmit={(e) => {
              e.preventDefault();
              const formData = new FormData(e.target);
              handleCreateEvent(Object.fromEntries(formData));
            }}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Event Name</label>
                  <input type="text" name="name" required className="w-full px-3 py-2 border border-gray-300 rounded-md" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                  <select name="category" className="w-full px-3 py-2 border border-gray-300 rounded-md">
                    <option>Coding</option>
                    <option>Robotics</option>
                    <option>Workshop</option>
                    <option>Hackathon</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
                  <input type="text" name="city" required className="w-full px-3 py-2 border border-gray-300 rounded-md" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                  <input type="date" name="date" required className="w-full px-3 py-2 border border-gray-300 rounded-md" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Price (INR)</label>
                  <input type="number" name="price" className="w-full px-3 py-2 border border-gray-300 rounded-md" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Capacity</label>
                  <input type="number" name="capacity" className="w-full px-3 py-2 border border-gray-300 rounded-md" />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea name="description" rows="3" className="w-full px-3 py-2 border border-gray-300 rounded-md"></textarea>
                </div>
              </div>
              <div className="mt-4 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowCreateForm(false)} className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50">
                  Cancel
                </button>
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
                  Create Event
                </button>
              </div>
            </form>
          </div>
        )}

        {/* My Events Table */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">My Events</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Event Name</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Registrations</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Capacity</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {myEvents.map((event) => (
                  <tr key={event.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{event.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{event.date}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{event.registrations}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{event.capacity}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">{event.status}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <button className="text-blue-600 hover:text-blue-800 mr-3">Edit</button>
                      <button className="text-red-600 hover:text-red-800">Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrganizerDashboard;