# Healthcare RAG Assistant

## Introduction

An AI-powered healthcare assistant designed to provide accurate and contextual information from a trusted healthcare knowledge base. The system uses Retrieval-Augmented Generation (RAG) to understand user queries, retrieve relevant information, and generate grounded responses.

## Project Objective

The objective is to simplify access to healthcare and diagnostic information by replacing traditional keyword-based searching with an intelligent conversational interface that can understand natural-language queries and provide relevant information from verified company data.

## Key Features

- Natural language query understanding
- RAG-based information retrieval
- Semantic search
- PDF and Excel document support
- Relevant context retrieval and reranking
- Context-aware conversations
- Test and package information retrieval
- Diagnostic centre information retrieval
- Pricing and related diagnostic information
- Fallback handling for unsupported queries
- Fast AI-powered responses

## Technology Stack

- **Frontend:** React, Tailwind CSS
- **Backend:** Python, FastAPI
- **RAG:** LangChain
- **LLM:** Llama via Groq API
- **Embeddings:** BGE Embeddings
- **Reranking:** BGE Cross-Encoder
- **Vector Database:** ChromaDB
- **Version Control:** Git, GitHub

## Dataset

The knowledge base is built using healthcare and diagnostic information provided by the lords pathology , including structured Excel data and PDF documents.

The dataset contains information such as:

- Diagnostic test details
- Test pricing
- Test packages
- Sample requirements
- Diagnostic centre information
- Reporting and processing information
- Policy related documents 

## Future Scope

- User authentication and Role-Based Access Control
- Department-wise knowledge access
- Multilingual support
- Voice-based assistant
- Appointment and test booking integration
- Integration with additional healthcare systems
