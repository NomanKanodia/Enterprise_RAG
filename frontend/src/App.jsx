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
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const uploadDocument = async () => {
    if (!file) {
      setError("Please select a document first.");
      return;
    }

    setError("");
    setUploadStatus("");
    setUploading(true);

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
        `${data.document.original_filename} indexed successfully.`
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
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

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && event.ctrlKey) {
      askQuestion();
    }
  };

  return (
    <div className="app">

      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">R</div>

            <div>
              <h1>Enterprise Knowledge Assistant</h1>
              <p>
                Ask questions about your organization's documents.
              </p>
            </div>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            RAG System Online
          </div>
        </div>
      </header>

      <main className="container">

        <section className="card upload-card">
          <div className="section-header">
            <div>
              <h2>Knowledge Base</h2>
              <p>
                Upload a PDF, DOCX, or TXT document to index it for retrieval.
              </p>
            </div>
          </div>

          <div className="upload-area">

            <div className="file-input-wrapper">
              <input
                id="file-upload"
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={(event) => {
                  setFile(event.target.files[0]);
                  setUploadStatus("");
                  setError("");
                }}
              />

              <label htmlFor="file-upload" className="file-label">
                <span className="upload-icon">↑</span>

                <span>
                  {file
                    ? file.name
                    : "Choose a document"}
                </span>
              </label>
            </div>

            <button
              className="primary-button"
              onClick={uploadDocument}
              disabled={uploading}
            >
              {uploading ? "Indexing..." : "Upload & Index"}
            </button>

          </div>

          {uploadStatus && (
            <div className="success-message">
              ✓ {uploadStatus}
            </div>
          )}
        </section>


        <section className="card question-card">

          <div className="section-header">
            <div>
              <h2>Ask a Question</h2>
              <p>
                The assistant answers using information retrieved from your documents.
              </p>
            </div>
          </div>

          <textarea
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Example: What is the objective of the Travel Policy?"
            rows={4}
          />

          <div className="question-footer">
            <span className="shortcut">
              Ctrl + Enter to ask
            </span>

            <button
              className="primary-button ask-button"
              onClick={askQuestion}
              disabled={loading}
            >
              {loading ? "Searching..." : "Ask Question"}
            </button>
          </div>

        </section>


        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}


        {answer && (
          <section className="card answer-card">

            <div className="section-header">
              <div>
                <h2>Answer</h2>
                <p>
                  Generated from retrieved document context.
                </p>
              </div>
            </div>

            <div className="answer">
              {answer}
            </div>


            {sources.length > 0 && (
              <div className="sources-section">

                <h3>Sources</h3>

                <div className="sources">

                  {sources.map((source, index) => (
                    <div className="source" key={index}>

                      <div className="source-icon">
                        📄
                      </div>

                      <div className="source-content">

                        <strong>
                          {source.document}
                        </strong>

                        <span>
                          Page {source.page_number}
                        </span>

                      </div>

                    </div>
                  ))}

                </div>

              </div>
            )}

          </section>
        )}

      </main>

      <footer className="footer">
        Enterprise RAG · FastAPI · FAISS · Gemini
      </footer>

    </div>
  );
}

export default App;