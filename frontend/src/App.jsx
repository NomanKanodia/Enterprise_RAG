import { useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const uploadDocument = async () => {
    if (!file) {
      setError("Please select a document first.");
      return;
    }

    setError("");
    setUploadStatus("Uploading...");
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed.");
      }

      setUploadStatus(
        `Uploaded successfully: ${data.document.original_filename}`
      );
    } catch (err) {
      setUploadStatus("");
      setError(err.message);
    }
  };

  const askQuestion = async () => {
    if (!query.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query,
          top_k: 5,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to get an answer.");
      }

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Enterprise Knowledge Assistant</h1>
          <p>
            Ask questions about your organization's documents using RAG.
          </p>
        </div>
      </header>

      <main className="container">

        <section className="card">
          <h2>Upload Document</h2>

          <div className="upload-row">
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={(e) => {
                setFile(e.target.files[0]);
                setUploadStatus("");
                setError("");
              }}
            />

            <button onClick={uploadDocument}>
              Upload
            </button>
          </div>

          {file && (
            <p className="selected-file">
              Selected: {file.name}
            </p>
          )}

          {uploadStatus && (
            <p className="success">
              {uploadStatus}
            </p>
          )}
        </section>

        <section className="card">
          <h2>Ask a Question</h2>

          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Example: What is the objective of the Travel Policy?"
            rows={4}
          />

          <button
            className="ask-button"
            onClick={askQuestion}
            disabled={loading}
          >
            {loading ? "Thinking..." : "Ask Question"}
          </button>
        </section>

        {error && (
          <section className="error">
            {error}
          </section>
        )}

        {answer && (
          <section className="card">
            <h2>Answer</h2>

            <div className="answer">
              {answer}
            </div>

            {sources.length > 0 && (
              <>
                <h3>Sources</h3>

                <div className="sources">
                  {sources.map((source, index) => (
                    <div className="source" key={index}>
                      <span>📄</span>

                      <div>
                        <strong>{source.document}</strong>
                        <p>
                          Page {source.page_number}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </section>
        )}

      </main>
    </div>
  );
}

export default App;