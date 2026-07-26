# Task Tracker API

A minimal learning-project REST API for tracking tasks, built with
Python and FastAPI.

This is Module 1 of the project: it stands up the FastAPI application
and a health-check endpoint only. No task CRUD endpoints, database,
authentication, or frontend are included yet.

## Architecture

Per ADR-001, this project uses **FastAPI + Pydantic with an in-memory
dict-based store** — no database, no ORM. This keeps setup to a single
`pip install` and a single run command, with no persistence machinery
beyond what a learning project needs. See ADR-001 for the full
reasoning and trade-offs (data does not persist across restarts).

## Prerequisites

- Python 3.10 or later
- pip

## Setup

1. Create and activate a virtual environment:

   **Linux/macOS:**
```bash
   python3 -m venv venv
   source venv/bin/activate
```

   **Windows (PowerShell):**
```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Copy the example environment file:

   **Linux/macOS:**
```bash
   cp .env.example .env
```

   **Windows (PowerShell):**
```powershell
   Copy-Item .env.example .env
```

## Running the server

```bash
uvicorn app.main:app --reload --port 8000
```

The server will start at `http://localhost:8000`.

## Testing the health endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2026-07-25T12:00:00.000000+00:00"
}
```

## API documentation (Swagger UI)

With the server running, open your browser to: