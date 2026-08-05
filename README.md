# Task Tracker API

A learning-project REST API for tracking tasks, built with Python,
FastAPI, and Pydantic, with a vanilla HTML/JS Kanban-style frontend.

The API supports full task CRUD (create, list with filtering, get,
partial update, delete) plus enforced status transitions (ToDo →
InProgress ↔ Done). There is no database, authentication, or
persistence beyond the process lifetime — see [ADR-001](docs/adr/ADR-001-backend-architecture.md)
for why an in-memory store was chosen for this project's scope.

## Architecture

Per ADR-001, this project uses **FastAPI + Pydantic with an in-memory
dict-based store** — no database, no ORM. This keeps setup to a single
`pip install` and a single run command, with no persistence machinery
beyond what a learning project needs. See ADR-001 for the full
reasoning and trade-offs (data does not persist across restarts), and
[docs/decisions/status-transition-rules.md](docs/decisions/status-transition-rules.md)
for why status transitions are restricted the way they are.

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

2. Install dependencies (this also installs `pytest`/`httpx` for testing):
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the example environment file (not currently read by the app —
   kept for forward compatibility if config needs grow):

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

## Running the tests

Use `python -m pytest`, not bare `pytest` — running the console-script
form of pytest directly does not reliably add the project root to
`sys.path`, and `app` fails to import. `python -m pytest` runs Python
with the current directory on `sys.path`, which fixes this.

```bash
python -m pytest -v
```

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

```
http://localhost:8000/docs
```

## Running with Docker

```bash
docker build -t task-tracker:dev .
docker run --rm -d -p 8000:8000 --name tt-dev task-tracker:dev
curl -i http://localhost:8000/health
docker exec tt-dev whoami   # should print "app", not "root"
docker stop tt-dev
```

The image uses a multi-stage build (a `builder` stage that installs
dependencies, and a slim `runtime` stage that copies only the built
virtualenv and application code), runs as a non-root user, and does
not bake in `.env`, `.git`, or any secrets — see `.dockerignore`.

## AI-assisted development

- `CLAUDE.md` — project memory for Claude Code (terminal agent) work: stack, commands, business rules, do-not rules.
- `AGENTS.md` — guardrails for Codex App (desktop review/planning agent) work.
- [docs/decisions/](docs/decisions/) — technical decision notes, including the status-transition rules and the (unimplemented) comments-feature plan critique.
- `docs/release-evidence.md`, `docs/final-ai-review.md`, `docs/security-review.md`, `docs/governance-worksheet.md`, `docs/ai-usage.md`, `docs/ai-playbook.md` — Module 4/5 evidence and final-project evidence.
- [docs/tool-fit-reflection.md](docs/tool-fit-reflection.md) — Module 4 X1 tool-fit reflection comparing Copilot, Cursor, Claude Code, and Codex App by task scope.

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates
- Existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and/or pull request.
- Docker image builds and runs with `/health` returning 200.
- AI review, security, and ownership evidence is in `docs/`.

### How to run locally
```bash
python -m venv venv
# On Windows PowerShell: venv\Scripts\Activate.ps1
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### How to run tests
```bash
python -m pytest -v
```

### How to run with Docker
```bash
docker build -t task-tracker:dev .
docker run -d -p 8000:8000 --name tt-dev task-tracker:dev
curl http://localhost:8000/health
```

### Evidence files
- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`
- `docs/security-review.md`
- `docs/governance-worksheet.md`
- `docs/ai-usage.md`

### AI assistance summary
AI helped draft or review: CI configuration, Dockerfile design, documentation templates, and security reviews.
I verified the work by: running the local pytest suite, checking the live `/health` endpoint, doing manual diff review, and running the Docker container.
One AI suggestion I rejected or corrected: rejected an AI proposal to add JWT authentication middleware, since it was out of scope; also corrected an AI-drafted CORS finding that incorrectly claimed a wildcard `*` origin when the code actually uses a specific localhost whitelist plus `"null"`.
