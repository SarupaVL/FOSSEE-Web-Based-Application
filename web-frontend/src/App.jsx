import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post(
      "http://127.0.0.1:8000/api/upload/",
      formData
    );

    setSummary(response.data);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Chemical Equipment Visualizer</h2>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={uploadFile}>Upload</button>

      {summary && (
        <div>
          <p>Total Equipment: {summary.total_equipment}</p>
          <p>Avg Flowrate: {summary.average_flowrate}</p>
          <p>Avg Pressure: {summary.average_pressure}</p>
          <p>Avg Temperature: {summary.average_temperature}</p>
        </div>
      )}
    </div>
  );
}

export default App;
