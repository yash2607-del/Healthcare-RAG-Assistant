# Healthcare RAG Assistant

This project is a Conversational Retrieval-Augmented Generation (RAG) assistant designed for diagnostic test query routing, retrieval, and answering. It enables users to ask about test availability, pricing, methodologies, and general diagnostic information, powered by a local Large Language Model (Llama 3 via Ollama) and a local semantic search engine.

## Architecture

The system consists of three main components:
1. **Frontend**: A responsive web application built with React, styled with vanilla CSS supporting light/dark modes.
2. **Backend**: A FastAPI server running the conversational RAG chain.
3. **Data & Storage**: An Excel-based diagnostics catalog ingested into a Chroma vector database using semantic embeddings and cross-encoder rerankers.

---

## Tech Stack

### Frontend
- React
- Vite
- Custom CSS variables (light/dark theme toggle support)

### Backend
- Python
- FastAPI & Uvicorn
- LangChain / LangChain Ollama
- ChromaDB (vector database)
- Sentence Transformers (BAAI/bge-base-en-v1.5)
- Cross-Encoder Reranker (BAAI/bge-reranker-base)

### Local LLM
- Ollama
- Llama 3 (8B Parameter Model)

---

## Prerequisites

Ensure you have the following installed on your machine:
- Node.js (version 18 or later)
- Python (version 3.10 or later)
- Ollama

---

## Setup Instructions

### 1. Ollama Configuration
Ensure the Ollama service is running and pull the Llama 3 model:
```bash
ollama serve
ollama pull llama3
```

### 2. Backend Setup
Navigate to the server directory, set up the virtual environment, install dependencies, and ingest the database:
```bash
cd Server

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate # On Windows

# Install dependencies
pip install -r requirements.txt

# Ingest excel data into vector database
python vectordb/chroma_client.py

# Start FastAPI server
python app.py
```
The backend server will run on `http://localhost:8000`.

### 3. Frontend Setup
Navigate to the client directory, install dependencies, and run the development server:
```bash
cd client
npm install
npm run dev
```
The frontend application will be hosted on `http://localhost:5173`.

---

## Key Features
- **Smart Query Routing**: Outgoing queries are dynamically classified into "diagnostics" (requires database retrieval) or "chitchat" (general greeting/conversational queries) to minimize computational overhead.
- **Advanced Context Retrieval**: Retrieves search results using cosine similarity, which are then re-ordered by relevance using a Cross-Encoder reranker.
- **Local Execution**: All data processing, vector searches, and LLM inferences are completed locally for data privacy and low latency.
- **Conversational Memory**: Retains session-based chat history to support contextual follow-up questions.
