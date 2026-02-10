import { useState } from "react";
import axios from "axios";

const Login = ({ setToken }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // Hardcode fallback for local development if env var is missing/empty
  const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
  console.log("Using API URL:", API_URL);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/api-token-auth/`, {
        username,
        password,
      });
      const token = response.data.token;
      setToken(token);
      localStorage.setItem("token", token);
      setError("");
    } catch (err) {
      setError(err.response?.data?.error || "Invalid credentials");
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: "400px", width: "100%", margin: "0 auto" }}>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h2 style={{ color: 'var(--primary)', fontSize: '2rem' }}>Chemical Equipment Parameter Visualizer</h2>
        <p style={{ color: 'var(--text-muted)' }}>Sign in to your account</p>
      </div>

      <form onSubmit={handleLogin}>
        <div style={{ marginBottom: "1.5rem" }}>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your username"
          />
        </div>
        <div style={{ marginBottom: "1.5rem" }}>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
          />
        </div>

        {error && (
          <div style={{
            background: '#fee2e2',
            color: '#b91c1c',
            padding: '0.75rem',
            borderRadius: '0',
            marginBottom: '1.5rem',
            fontSize: '0.875rem'
          }}>
            {error}
          </div>
        )}

        <button
          type="submit"
          className="btn-primary"
          style={{ width: "100%", padding: "0.75rem", fontSize: "1rem" }}
        >
          Sign In
        </button>
      </form>
    </div>
  );
};

export default Login;
