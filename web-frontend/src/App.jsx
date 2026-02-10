import { useState, useEffect } from "react";
import axios from "axios";
import Login from "./components/Login";
import History from "./components/History";
import Dashboard from "./components/Dashboard";
import Navbar from "./components/Navbar";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem("token");
    setSummary(null);
  };

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/api/upload/`,
        formData,
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );
      setSummary(response.data);
    } catch (error) {
      console.error("Upload failed", error);
      alert("Upload failed: " + (error.response?.data?.error || "Unknown error"));
    }
  };

  const chartData = summary ? {
    labels: Object.keys(summary.type_distribution),
    datasets: [
      {
        label: "Equipment Type Distribution",
        data: Object.values(summary.type_distribution),
        backgroundColor: "rgba(75, 192, 192, 0.6)",
      },
    ],
  } : null;

  if (!token) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', background: 'var(--background)' }}>
        <div className="card">
          <Login setToken={setToken} />
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', background: 'var(--background)' }}>
      <Navbar onLogout={handleLogout} />
      <div style={{ padding: '2rem 0' }}>
        <Dashboard
          summary={summary}
          chartData={chartData}
          onUpload={uploadFile}
          setFile={setFile}
          file={file}
        />
        <History token={token} />
      </div>
    </div>
  );
}

export default App;
