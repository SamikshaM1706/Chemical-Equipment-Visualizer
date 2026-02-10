import { Card, CardContent, Typography, CircularProgress } from '@mui/material';
import React, { useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);


  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
  if (!file) return alert("Please select a CSV file.");

  setLoading(true);  // Show spinner

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await axios.post(
      "http://127.0.0.1:8000/api/upload/",
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );
    setSummary(res.data.summary);
  } catch (err) {
    console.error(err);
    alert("Upload failed!");
  } finally {
    setLoading(false); // Hide spinner
  }
};


  return (
    <div style={{ padding: "20px" }}>
      <h1>Chemical Equipment Parameter Visualizer</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload CSV</button>

      {summary && (
        <div style={{ marginTop: "30px" }}>
          <h2>Summary</h2>
          <div style={{ display: "flex", gap: "20px", flexWrap: "wrap", marginTop: "20px" }}>
  <Card sx={{ minWidth: 200, padding: 2, boxShadow: 3 }}>
    <CardContent>
      <Typography variant="h6">Total Equipment</Typography>
      <Typography>{summary.total_count}</Typography>
    </CardContent>
  </Card>

  <Card sx={{ minWidth: 200, padding: 2, boxShadow: 3 }}>
    <CardContent>
      <Typography variant="h6">Average Flowrate</Typography>
      <Typography>{summary.avg_flowrate}</Typography>
    </CardContent>
  </Card>

  <Card sx={{ minWidth: 200, padding: 2, boxShadow: 3 }}>
    <CardContent>
      <Typography variant="h6">Average Pressure</Typography>
      <Typography>{summary.avg_pressure}</Typography>
    </CardContent>
  </Card>

  <Card sx={{ minWidth: 200, padding: 2, boxShadow: 3 }}>
    <CardContent>
      <Typography variant="h6">Average Temperature</Typography>
      <Typography>{summary.avg_temperature}</Typography>
    </CardContent>
  </Card>
</div>


          <h3>Equipment Type Distribution</h3>
          <Bar
  data={{
    labels: Object.keys(summary.type_distribution),
    datasets: [
      {
        label: "Count",
        data: Object.values(summary.type_distribution),
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"],
      },
    ],
  }}
  options={{
    responsive: true,
    plugins: {
      legend: { position: "top" },
      tooltip: { enabled: true },
    },
  }}
/>

        </div>
      )}
    </div>
  );
}

export default App;
