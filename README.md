# Task Tracker API

A learning-project Task Tracker with a Python/FastAPI backend (in-memory store, no database) and a vanilla JS Kanban frontend, built incrementally across Modules 1-3 with AI-assisted workflows, and extended for the mid-course project with due dates and tags.

## Features

- Task CRUD with status (`ToDo`, `InProgress`, `Done`) and priority (`Low`, `Medium`, `High`)
- Forward-only status transitions: `ToDo → InProgress → Done`
- Due dates with computed overdue detection and filtering
- Tags/labels with filtering
- Kanban board with drag-and-drop, priority sorting, and loading/empty/ready/error states
- Create/edit modal with client + server validation

## Prerequisites

- Python 3.10+
- pip

## Setup

1. Clone the repo and check out the `mid-course-project` branch:
   ```bash
   git clone https://github.com/<your-username>/task-tracker.git
   cd task-tracker
   git checkout mid-course-project
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

## Running the backend

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

- Swagger docs: `http://localhost:8000/docs`
- Health check: `curl http://localhost:8000/health`

## Running the frontend

With the backend running, open `frontend/index.html` directly in your browser, or serve it with a local static server (e.g. VS Code Live Server) at `http://localhost:5500`.

The frontend expects the backend at `http://localhost:8000` (see `API_BASE` in `frontend/index.html`).

## Running tests

```bash
python -m pytest -v
```

All 32 tests (20 original + 12 added for due dates and tags) should pass.

## Project documentation

See `docs/adr/ADR-001-backend-architecture.md` for the original architecture decision, and `docs/midcourse/` for the mid-course project documentation:

- `user-stories.md` — feature user stories and acceptance criteria
- `mini-adr.md` — design decisions for due dates and tags
- `prompt-log.md` — AI prompts used, with weak/improved comparisons
- `verification.md` — test results, manual checks, behavior contract, and Break Test evidence
- `reflection.md` — project reflection