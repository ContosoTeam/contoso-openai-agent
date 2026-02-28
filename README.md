# Contoso OpenAI RAG Agent

An intelligent chatbot using Azure OpenAI Service with Retrieval-Augmented Generation (RAG) for enterprise document Q&A.

## Architecture
- **LangChain** for RAG pipeline orchestration
- **FastAPI** for REST API endpoints
- **Azure OpenAI** (GPT-4) for language model
- **Azure Cognitive Search** for vector store
- **Redis** for conversation memory

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API Endpoints
- `POST /chat` - Send a message to the chatbot
- `POST /upload` - Upload documents for RAG indexing
- `GET /conversations/{id}` - Get conversation history
- `DELETE /conversations/{id}` - Clear conversation

## License
MIT
