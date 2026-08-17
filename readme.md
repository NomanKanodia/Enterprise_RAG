# Document Search and Question Answering System

A RAG-based application that allows users to upload documents and ask questions about their content. The system retrieves relevant document chunks using semantic search and generates grounded answers using Google Gemini.

## Features

- Upload PDF, DOCX, and TXT documents
- Parse and process uploaded documents
- Split documents into smaller chunks
- Generate embeddings using Sentence Transformers
- Store and search embeddings using FAISS
- Retrieve relevant document content for user queries
- Generate grounded answers using Google Gemini
- Provide document and page-level sources
- React-based frontend with FastAPI backend

## Tech Stack

- **Frontend:** React, Vite
- **Backend:** FastAPI, Python
- **Embeddings:** Sentence Transformers
- **Vector Store:** FAISS
- **LLM:** Google Gemini
- **Document Processing:** PyMuPDF
- **Chunking:** LangChain Text Splitters
