import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { setToken } from "../utils/auth"; // or localStorage.setItem("token", token)

const OAuthCallback = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true); // for showing "Logging you in..."

  useEffect(() => {
    const timeout = setTimeout(() => {
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get("token");

      if (token) {
        setToken(token);
        navigate("/dashboard");
      } else {
        // Token not found even after delay
        navigate("/login");
      }

      setLoading(false);
    }, 300); // give 300ms buffer for URL/token processing

    return () => clearTimeout(timeout);
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center text-xl font-semibold text-[#206f6a]">
      {loading ? "Logging you in via Google..." : "Redirecting..."}
    </div>
  );
};

export default OAuthCallback;
