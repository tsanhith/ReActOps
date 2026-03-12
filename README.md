# ReActOps

An intelligent IT operations assistant that uses a **ReAct (Reason+Act) loop**, **BM25 retrieval**, and **Groq LLM** to help engineers troubleshoot incidents faster.

## Features

- 🔍 **BM25 retrieval** over runbooks, logs, and past tickets.
- 🤖 **ReAct agent** with tool calling (search_runbooks, query_logs, search_tickets).
- ✅ **Validation** of runbook freshness (coming soon).
- 🔄 **Self-reflection** to improve answers (coming soon).
- 📊 **RAGAS evaluation** for answer quality (coming soon).
- 🛡️ **Safe stopping** to prevent infinite loops.
- 🚀 **FastAPI backend** with `/ask` and `/health` endpoints.
- 🧪 **Unit and integration tests**.

## Tech Stack

- Python, FastAPI, Uvicorn. 
- Groq API (OpenAI-compatible). 
- BM25 (rank_bm25). 
- Pytest for testing. 
- Docker (optional, for deployment). 

## Getting Started

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`.
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux).
4. Install dependencies: `pip install -r requirements.txt`.
5. Generate mock data: `python generate_mock_data.py`.
6. Set up your Groq API key in `.env` (see `.env.example`).
7. Run the server: `uvicorn reactops.main:app --reload`.
8. Visit `http://localhost:8000/docs` to test the API.
