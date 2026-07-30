# Enterprise AI Knowledge Assistant

A production-ready AI Knowledge Assistant built with FastAPI, LangChain, FAISS, Google Gemini, and Sentence Transformers.

## Features

- PDF Upload
- Parent-Child Chunking
- FAISS Vector Search
- Hybrid Retrieval
- Query Expansion
- Re-ranking
- Context Compression
- Conversation Memory (SQLite)
- Source Attribution
- Streaming Responses
- Incremental FAISS Indexing
- Duplicate Detection
- CRUD Document Management
- Docker Support

---

## Tech Stack

- Python 3.12
- FastAPI
- LangChain
- LangGraph
- Google Gemini
- FAISS
- Sentence Transformers
- SQLite
- Docker

---

## Project Structure

```
app/
    llm/
    memory/
    models/
    prompt/
    rag/
    schemas/
    services/
    storage/
    utils/

uploads/
vector_db/
metadata/

main.py
Dockerfile
docker-compose.yml
requirements.txt
```

---

## Run Locally

```bash
pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Docker

```bash
docker compose up --build
```

---

## API Documentation

```
http://localhost:8000/docs
```

---

## Health Check

```
http://localhost:8000/health
```

---

## Future Improvements

- Redis Cache
- Authentication
- Kubernetes Deployment
- Monitoring
- CI/CD
- AWS Deployment