import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { setToken } from "../utils/auth";

export default function OAuthCallback() {
  const navigate = useNavigate();

  useEffect(() => {
    const url = new URLSearchParams(window.location.search);
    const token = url.get("token");

    if (token) {
      setToken(token);
      navigate("/dashboard");
    } else {
      alert("Login failed.");
      navigate("/login");
    }
  }, []);

  return <p>Redirecting...</p>;
}
