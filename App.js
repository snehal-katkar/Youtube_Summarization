import { useState } from "react";

// ✅ Replace this with your real backend URL in production
const BACKEND_URL = "http://127.0.0.1:8000/api";

function App() {
  const [url, setUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSummary("");
    setError("");

    if (!url.trim()) {
      setError("Please enter a YouTube URL.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${BACKEND_URL}/summarize/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (response.ok) {
        setSummary(data.summary || "No summary returned.");
      } else {
        setError(data.error || "Failed to fetch summary.");
      }
    } catch (err) {
      setError("Network error. Could not connect to the backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif", maxWidth: "600px", margin: "auto" }}>
      <h1>YouTube Summarizer</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: "1rem" }}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Paste YouTube link"
          style={{ width: "100%", padding: "0.5rem", marginBottom: "0.5rem" }}
        />
        <button type="submit" disabled={loading} style={{ padding: "0.5rem 1rem" }}>
          {loading ? "Summarizing..." : "Summarize"}
        </button>
      </form>

      {summary && (
        <div style={{ marginTop: "1rem", backgroundColor: "#f0f0f0", padding: "1rem", borderRadius: "5px" }}>
          <strong>Summary:</strong>
          <p>{summary}</p>
        </div>
      )}

      {error && (
        <div style={{ marginTop: "1rem", color: "red" }}>
          <strong>Error:</strong> {error}
        </div>
      )}
    </div>
  );
}

export default App;
