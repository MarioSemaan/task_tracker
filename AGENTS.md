# AGENTS.md — Codex App Guardrails for Task Tracker

This file gives the Codex App desktop agent repo-specific context and
Module 5 operating boundaries. Keep it accurate — if it goes stale,
Codex will reason about a project that no longer exists.

## Stack and commands

- **Language / framework**: Python 3.11, FastAPI, Pydantic v2, Uvicorn
- **Testing**: pytest, httpx (via FastAPI's TestClient)
- **Frontend**: plain HTML/CSS/JS (`frontend/index.html`) — no build step, no framework
- **Storage**: in-memory Python dict (`app/storage.py`) — no database, no ORM (see docs/adr/ADR-001-backend-architecture.md)
- **Run API**: `uvicorn app.main:app --reload --port 8000`
- **Run tests**: `python -m pytest -v` — **not** bare `pytest` (bare pytest fails with `ModuleNotFoundError: No module named 'app'`)
- **Install deps**: `pip install -r requirements.txt` (includes pytest and httpx)

## Project rules

- Task statuses: `ToDo`, `InProgress`, `Done` — enforced transitions only (see `app/business_rules.py`)
- All models use `extra="forbid"` — unknown fields are rejected with 422
- `title` is required, 1–200 chars after `.strip()`; blank/whitespace-only titles are rejected with 422
- `POST /tasks` returns 201; `DELETE /tasks/{id}` returns 204 with no body; GET/PATCH on a missing id returns 404
- CORS: specific localhost whitelist (`http://localhost:5500`, `http://127.0.0.1:5500`, `http://localhost:5173`, `"null"`) — not a wildcard `*`
- No authentication, no database, no persistence across restarts — these are intentional course-scope decisions, not gaps

## Module 5 boundaries

- **Read-only default**: prefer read-only analysis and docs-first modifications
- **Docs first**: required deliverables live in `docs/` — unexpected edits to `app/` or `frontend/` should be flagged and rejected unless fixing a verified bug with explicit approval
- **No scope creep**: do not introduce databases, authentication, notifications, new product features, or deployment automation
- **Security and data**: never expose real secrets, tokens, `.env` values, or personal data in prompts

## Review expectations

- **Cite files**: every claim about project behavior must reference a real file and line — do not describe what a generic FastAPI project would do
- **Avoid invented structure**: if a directory, file, or pattern does not exist in this repo, say so rather than assuming it matches a common template
- **Ask before broad edits**: propose a plan and wait for approval before editing more than one file at a time
- **Explain proposed diffs**: before applying any change, describe in plain language what each changed line does and why it is needed
- **Grade findings before acting**: label AI-generated review and security findings as Valid/False Positive/Noise (security) or Useful/Noise/Wrong (code review) before any fix is applied
