# CLAUDE.md — Project Memory for Claude Code

This file gives Claude Code (terminal agent) repo-specific context so
it does not treat this as a generic FastAPI project. Correct this
file by hand whenever the stack, commands, or rules below drift from
the real code — do not let it go stale.

## Stack
- Python 3.11, FastAPI, Pydantic v2, Uvicorn
- Testing: pytest, httpx (via FastAPI's TestClient)
- Frontend: plain HTML/CSS/JS (`frontend/index.html`), no build step, no framework
- Storage: in-memory Python dict (`app/storage.py`) — no database, no ORM (see ADR-001)

## Run and test commands
- Run the API: `uvicorn app.main:app --reload --port 8000`
- Run tests: `python -m pytest -v` — **not** bare `pytest`. Bare `pytest`
  fails with `ModuleNotFoundError: No module named 'app'` because the
  project root isn't reliably on `sys.path` without the `-m` flag.
- Install deps (includes pytest/httpx): `pip install -r requirements.txt`
- Docker build/run: `docker build -t task-tracker:dev .` then
  `docker run --rm -d -p 8000:8000 --name tt-dev task-tracker:dev`

## Architecture
- `app/main.py` — FastAPI app, route handlers, CORS config
- `app/models.py` — Pydantic models (TaskCreate, TaskUpdate, TaskResponse, enums)
- `app/storage.py` — in-memory dict store, CRUD functions, `_reset()` for tests
- `app/business_rules.py` — status-transition validation (single source of truth)
- `frontend/index.html` — Kanban board UI, calls the API directly
- `tests/test_tasks.py` — main pytest suite; `tests/conftest.py` has fixtures

## Business rules (do not guess — read app/business_rules.py)
- Allowed status transitions: `ToDo -> InProgress`, `InProgress -> Done`,
  `Done -> InProgress`. Anything else, including a same-status "transition"
  (e.g. `ToDo -> ToDo`), is rejected with 422.
- `title` is required, 1-200 chars after `.strip()`; blank/whitespace-only
  titles are rejected with 422.
- All models use `extra="forbid"` — unknown fields in a request body are
  rejected with 422, not silently ignored.
- POST /tasks returns 201. DELETE /tasks/{id} returns 204 with no body.
  GET/PATCH on a missing id returns 404, not 200 with a null body.

## UI states
- Kanban board with three columns matching TaskStatus: ToDo, InProgress, Done.
- Create/edit uses a modal form; invalid submissions should surface the
  API's 422 detail message rather than failing silently.

## CORS / local dev
- `allow_origins` is a specific whitelist: `http://localhost:5500`,
  `http://127.0.0.1:5500`, `http://localhost:5173`, and `"null"` (for
  `file://` frontend loads). It is **not** `*` — do not assume a wildcard
  when reasoning about CORS risk here.

## Do-not rules
- Do not add authentication, a database/ORM, or persistence beyond the
  in-memory store without explicit approval.
- Do not add new product features (comments, notifications, multi-user,
  etc.) — this repo is intentionally scope-limited for the course.
- Do not add deployment automation to CI; the workflow's job is to run
  tests, nothing more.
- Do not commit `.env`, secrets, tokens, or real personal/customer data.
- Do not silently rewrite business rules (e.g. status transitions) —
  flag a proposed change and require human approval before editing
  `app/business_rules.py`.
