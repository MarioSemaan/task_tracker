# Architecture Document — Strategy B (Structured Context)

*Produced after providing CLAUDE.md/AGENTS.md content plus short
manual summaries of each file in `app/`.*

## System overview
FastAPI + Pydantic task tracker with an in-memory dict store (no
database), a plain HTML/JS frontend, CRUD + status-transition
endpoints, and a pytest suite using FastAPI's TestClient.

## Backend structure
- `app/main.py` — routes, CORS config, FastAPI app instance
- `app/models.py` — TaskCreate/TaskUpdate/TaskResponse, TaskStatus/TaskPriority enums
- `app/storage.py` — `_tasks` dict, add/get/update/delete functions, `_reset()` for test isolation
- `app/business_rules.py` — `VALID_TRANSITIONS` frozenset + `validate_status_transition`

## Frontend structure
`frontend/index.html` — single-file Kanban board, calls the API
directly via `fetch`, no build tooling or framework.

## Data flow
Request → FastAPI route → Pydantic validation (`extra="forbid"`,
custom title validator) → (for PATCH) `validate_status_transition`
check against `app/business_rules.py` → `app/storage.py` dict
mutation → `TaskResponse` serialization → JSON.

## Testing and verification
`tests/test_tasks.py` + `tests/conftest.py`, using FastAPI's
`TestClient`; `_reset_storage` autouse fixture clears `_tasks` between
tests. Run via `python -m pytest -v` (bare `pytest` fails — see
CLAUDE.md).

## Known limits
No database, no auth, no persistence across restarts (explicit
project-scope decisions per ADR-001, not oversights).

## Notes
More complete and more accurate than Strategy A because it had real
file summaries to draw on. Ran noticeably longer than Strategy A and
included some detail (e.g. restating every field in every model) that
didn't add much beyond what the code itself already makes obvious —
completeness came at the cost of being a bit dense to skim.
