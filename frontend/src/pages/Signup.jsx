// src/pages/Signup.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Signup = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
    name: "",
    profile_picture: "",
    role: "student",
  });

  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ 
      ...formData, 
      [e.target.name]: e.target.value 
    });
  };

  const extractErrorMessage = (error) => {
    // Handle different error response formats
    if (typeof error === 'string') return error;
    if (error?.msg) return error.msg;
    if (error?.message) return error.message;
    if (error?.detail) return error.detail;
    return "An unknown error occurred";
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  setError("");
  setIsLoading(true);

  try {
    // ✅ Signup and get the token directly
    const signupResponse = await axios.post(
      `http://localhost:8000/api/v1/auth/signup/email`, 
      formData,
      {
        headers: {
          "Content-Type": "application/json"
        }
      }
    );

    const token = signupResponse.data.access_token; // ✅
    if (token) {
      localStorage.setItem('token', token); // ✅
      navigate("/dashboard"); // ✅
    } else {
      throw new Error("Token not returned on signup");
    }
  } catch (err) {
    const errorData = err.response?.data;
    setError(extractErrorMessage(errorData));
  } finally {
    setIsLoading(false);
  }
};


  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold text-center text-[#206f6a] mb-6">Create your account</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <p className="text-red-600 text-sm">
              {typeof error === 'object' ? JSON.stringify(error) : error}
            </p>
          )}

          <input
            type="email"
            name="email"
            required
            placeholder="Email"
            className="w-full px-4 py-2 border rounded-md"
            value={formData.email}
            onChange={handleChange}
            autoComplete="email"
          />

          <input
            type="password"
            name="password"
            required
            placeholder="Password"
            className="w-full px-4 py-2 border rounded-md"
            value={formData.password}
            onChange={handleChange}
            autoComplete="new-password"
          />

          <input
            type="text"
            name="name"
            placeholder="Full Name"
            className="w-full px-4 py-2 border rounded-md"
            value={formData.name}
            onChange={handleChange}
            autoComplete="name"
          />

          <input
            type="url"
            name="profile_picture"
            placeholder="Profile Picture URL"
            className="w-full px-4 py-2 border rounded-md"
            value={formData.profile_picture}
            onChange={handleChange}
          />

          <select
            name="role"
            value={formData.role}
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-md"
          >
            <option value="student">Student</option>
            <option value="instructor">Instructor</option>
            <option value="admin">Admin</option>
          </select>

          <button
            type="submit"
            className={`w-full bg-[#206f6a] text-white py-2 rounded-md hover:bg-[#1a5c58] ${
              isLoading ? "opacity-75 cursor-not-allowed" : ""
            }`}
            disabled={isLoading}
          >
            {isLoading ? "Processing..." : "Sign Up"}
          </button>
        </form>

        <p className="mt-4 text-sm text-center">
          Already have an account?{" "}
          <a href="/login" className="text-[#206f6a] font-medium">
            Log in
          </a>
        </p>
      </div>
    </div>
  );
};

export default Signup;