# Healthcare RAG Assistant

This project is a Conversational Retrieval-Augmented Generation (RAG) assistant designed for diagnostic test query routing, retrieval, and answering. It enables users to ask about test availability, pricing, methodologies, and general diagnostic information, powered by a local Large Language Model (Llama 3 via Ollama) and a local semantic search engine.

## Architecture

The system consists of three main components:
1. **Frontend**: A responsive web application built with React, styled with vanilla CSS supporting light/dark modes.
2. **Backend**: A FastAPI server running the conversational RAG chain.
3. **Data & Storage**: An Excel-based diagnostics catalog ingested into a Chroma vector database using semantic embeddings and cross-encoder rerankers.


## Tech Stack

### Frontend
- React.js

### Backend
- Python
- FastAPI
- LangChain
- ChromaDB (vector database)
- Sentence Transformers (BAAI/bge-base-en-v1.5)
- Cross-Encoder Reranker (BAAI/bge-reranker-base)
  

### Local LLM
- Ollama
- Llama 3 (8B Parameter Model)


## Key Features
- **Smart Query Routing**: Outgoing queries are dynamically classified into "diagnostics" (requires database retrieval) or "chitchat" (general greeting/conversational queries) to minimize computational overhead.
- **Advanced Context Retrieval**: Retrieves search results using cosine similarity, which are then re-ordered by relevance using a Cross-Encoder reranker.
- **Local Execution**: All data processing, vector searches, and LLM inferences are completed locally for data privacy and low latency.
- **Conversational Memory**: Retains session-based chat history to support contextual follow-up questions.
