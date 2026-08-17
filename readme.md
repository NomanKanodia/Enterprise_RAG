# Document Search and Question Answering System

An end-to-end, full-stack **Retrieval-Augmented Generation (RAG)** platform designed to ingest, process, index, and query unstructured multi-format documents with high precision, speed, and contextual accuracy. Built using a decoupled FastAPI backend, Google Gemini LLM API, FAISS vector indexing, and an interactive Vite-React frontend.

---

## Overview & Architecture

This platform provides an automated document processing and intelligent querying pipeline. It enables users to upload custom documents, transform them into optimized vector representations, and query them using natural language to obtain grounded answers backed by source content.

---

## Key Features

- **Multi-Format Parsing**: Built-in support for processing PDF, DOCX, and TXT files directly.
- **Customizable Chunking Strategies**: Configurable strategies powered by LangChain and custom chunkers to optimize context boundaries.
- **Fast Similarity Search**: FAISS index implementation for fast vector search and retrieval operations.
- **Google Gemini Integration**: Leverages Gemini models for intelligent contextual answer synthesis.
- **Automated Evaluation Suite**: Pre-configured testing framework (`test_rag_evaluation.py`, `test_retrieval_evaluation.py`, `test_answer_evaluation.py`) to benchmark retrieval precision and answer validity against standard question sets.
- **Modern User Interface**: Responsive React + Vite application for document uploads, interactive chat interfaces, and real-time query feedback.

---

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/                 # FastAPI router endpoints (chat, query, upload)
│   │   ├── chunking/            # Chunking strategies & implementations
│   │   ├── document/            # Document loading and file parsers (docx, pdf, txt)
│   │   ├── embeddings/          # Vector embedding services
│   │   ├── generation/          # Google Gemini LLM integration
│   │   ├── retrieval/           # Context retrieval logic
│   │   ├── schemas/             # Pydantic models for data validation
│   │   ├── services/            # Core business logic (RAG & Upload services)
│   │   ├── vectorstore/         # FAISS vector index & document store management
│   │   └── main.py              # Application entry point
│   ├── evaluation/              # Test datasets (questions.json, answer_checks.json)
│   ├── requirements.txt         # Backend Python dependencies
│   ├── test_rag.py              # Integration tests
│   ├── test_retrieval_evaluation.py
│   └── test_answer_evaluation.py
├── docs/                        # Architecture & API documentation
├── frontend/
│   ├── public/                  # SVG assets and icons
│   ├── src/                     # React application source code
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## Tech Stack

- **Backend Framework**: FastAPI, Pydantic, Uvicorn
- **Vector Search & ML**: FAISS, LangChain, Google Gemini API
- **Document Extractors**: PyPDF / pdfplumber, python-docx
- **Frontend Stack**: React, Vite, CSS / Tailwind CSS
- **Evaluation & Testing**: Pytest, Custom evaluation harnesses

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18+ and npm
- A Google Gemini API Key

---

### Backend Setup

1. Navigate to the backend folder:
    ```
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
    ```
   pip install -r requirements.txt
    ```

4. Configure environment variables:
   Copy `.env.example` to `.env` and add your Gemini API key:
   ```
   cp .env.example .env
   ```

   Add your API key inside `.env`:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. Launch the FastAPI server:
    ```
   uvicorn app.main:app --reload --port 8000
   ```

---

### Frontend Setup

1. Open a new terminal and navigate to the frontend folder:
    ```
   cd frontend
   ```

2. Install Node packages:
    ```
   npm install
   ```

3. Run the development server:
    ```
   npm run dev
   ```

---

## Evaluation & Benchmarking

Run the built-in evaluation utilities to measure retrieval quality and answer accuracy:

```
cd backend
```

# Test Gemini LLM connection

```
python test_llm.py
```

# Run RAG workflow test
```
python test_rag.py
```

# Evaluate retrieval precision
```
python test_retrieval_evaluation.py
```

# Evaluate answer generation quality
```
python test_answer_evaluation.py
```

---

## API Documentation

When the backend server is running, explore the API endpoints interactively at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
