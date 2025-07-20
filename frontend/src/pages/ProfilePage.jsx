import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { FiUser, FiMail, FiCalendar, FiEdit, FiSave } from 'react-icons/fi';

const ProfilePage = () => {
  const { user: authUser, logout } = useAuth();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    profile_picture: ''
  });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/auth/me', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        setUser(response.data);
        setFormData({
          name: response.data.name,
          email: response.data.email,
          profile_picture: response.data.profile_picture || ''
        });
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load profile');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleEditProfile = async () => {
    try {
      const response = await axios.put(
        'http://localhost:8000/api/v1/auth/me',
        formData,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      );
      setUser(response.data);
      setEditMode(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update profile');
    }
  };

  if (loading) return <div className="text-center py-8">Loading profile...</div>;
  if (error) return <div className="text-center py-8 text-red-600">{error}</div>;
  if (!user) return <div className="text-center py-8">No user data found</div>;

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        {/* Profile Header */}
        <div className="bg-[#206f6a] p-6 text-white">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-20 h-20 rounded-full bg-white flex items-center justify-center">
                {user.profile_picture ? (
                  <img 
                    src={user.profile_picture} 
                    alt="Profile" 
                    className="w-full h-full rounded-full object-cover"
                  />
                ) : (
                  <FiUser className="text-[#206f6a] text-3xl" />
                )}
              </div>
              <div>
                {editMode ? (
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="text-2xl font-bold bg-white text-gray-800 p-1 rounded"
                  />
                ) : (
                  <h1 className="text-2xl font-bold">{user.name}</h1>
                )}
                <p className="text-[#c2e0dd] capitalize">{user.role.toLowerCase()}</p>
              </div>
            </div>
            {editMode ? (
              <button 
                onClick={handleEditProfile}
                className="flex items-center px-4 py-2 bg-white text-[#206f6a] rounded-md hover:bg-gray-100"
              >
                <FiSave className="mr-2" /> Save Changes
              </button>
            ) : (
              <button 
                onClick={() => setEditMode(true)}
                className="flex items-center px-4 py-2 bg-white text-[#206f6a] rounded-md hover:bg-gray-100"
              >
                <FiEdit className="mr-2" /> Edit Profile
              </button>
            )}
          </div>
        </div>

        {/* Profile Details */}
        <div className="p-6 grid md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-800">Personal Information</h2>
            
            <div className="flex items-start space-x-4">
              <FiMail className="text-[#206f6a] mt-1" />
              <div className="w-full">
                <p className="text-sm text-gray-500">Email</p>
                {editMode ? (
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    className="w-full p-2 border rounded"
                  />
                ) : (
                  <p className="text-gray-800">{user.email}</p>
                )}
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <FiCalendar className="text-[#206f6a] mt-1" />
              <div>
                <p className="text-sm text-gray-500">Last Login</p>
                <p className="text-gray-800">Just now</p>
              </div>
            </div>

            {editMode && (
              <div className="flex items-start space-x-4">
                <FiUser className="text-[#206f6a] mt-1" />
                <div className="w-full">
                  <p className="text-sm text-gray-500">Profile Picture URL</p>
                  <input
                    type="text"
                    value={formData.profile_picture}
                    onChange={(e) => setFormData({...formData, profile_picture: e.target.value})}
                    className="w-full p-2 border rounded"
                    placeholder="Enter image URL"
                  />
                </div>
              </div>
            )}
          </div>

          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-800">Account Actions</h2>
            
            <button 
              onClick={logout}
              className="w-full flex items-center justify-between p-4 border rounded-lg hover:bg-red-50 text-red-600"
            >
              <span>Logout</span>
            </button>
          </div>
        </div>

        {/* Stats Section (if needed) */}
        {user.role === 'INSTRUCTOR' && (
          <div className="border-t p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Teaching Statistics</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-[#f5f9f9] p-4 rounded-lg">
                <p className="text-sm text-gray-500">Reports Reviewed</p>
                <p className="text-2xl font-bold text-[#206f6a]">142</p>
              </div>
              <div className="bg-[#f5f9f9] p-4 rounded-lg">
                <p className="text-sm text-gray-500">Students Mentored</p>
                <p className="text-2xl font-bold text-[#206f6a]">23</p>
              </div>
              <div className="bg-[#f5f9f9] p-4 rounded-lg">
                <p className="text-sm text-gray-500">Courses Taught</p>
                <p className="text-2xl font-bold text-[#206f6a]">5</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfilePage;