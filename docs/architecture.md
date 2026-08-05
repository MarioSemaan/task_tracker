# Architecture

*Final doc, combining the accurate parts of Strategies A/B/C — see
docs/architecture-A.md, -B.md, -C.md for the raw comparison.*

## System overview
FastAPI + Pydantic REST API for tracking tasks, with a plain HTML/JS
Kanban frontend. No database — task data lives in an in-memory Python
dict for the lifetime of the process (see ADR-001 for why).

## Backend structure
- `app/main.py` — FastAPI app, CORS config, route handlers (`POST
  /tasks`, `GET /tasks`, `GET /tasks/{id}`, `PATCH /tasks/{id}`,
  `DELETE /tasks/{id}`, `GET /health`)
- `app/models.py` — Pydantic request/response models; `extra="forbid"`
  on every model; custom title validator (1–200 chars, stripped)
- `app/storage.py` — the in-memory `_tasks` dict and its CRUD
  functions; `_reset()` exists specifically to give tests a clean slate
- `app/business_rules.py` — `VALID_TRANSITIONS` and
  `validate_status_transition`, the single source of truth for which
  status changes are legal (see docs/decisions/status-transition-rules.md)

## Frontend structure
`frontend/index.html` — a single self-contained file with inline
CSS/JS, no build step, no framework. Talks to the API directly via
`fetch` calls to `http://localhost:8000`.

## Data flow
1. Client sends a request (frontend `fetch`, curl, or the Swagger UI).
2. FastAPI routes it to the matching handler in `app/main.py`.
3. Pydantic validates the body against the relevant model — unknown
   fields, missing required fields, and invalid enum values are all
   rejected with 422 before any handler code runs.
4. For `PATCH` requests that change `status`, `validate_status_transition`
   checks the requested change against `VALID_TRANSITIONS` and raises a
   422 if it's not allowed.
5. `app/storage.py` mutates the in-memory dict and returns the updated
   record.
6. FastAPI serializes the `TaskResponse` model back to JSON.

## Testing and verification
`tests/test_tasks.py` (pytest + FastAPI's `TestClient`) covers create,
list/filter, get, patch (including the transition rules), and delete,
including 404/422 edge cases. Run with `python -m pytest -v` — see
CLAUDE.md for why the bare `pytest` command fails here.

## Known limits
No auth, no database/persistence, no multi-user support — all
deliberate scope decisions for a learning project (ADR-001), not gaps
that were missed.

## Context-strategy comparison log

| Strategy | Most accurate? | Most invented/generic? | Most honest about gaps? |
|---|---|---|---|
| A — minimal | No — assumed a database and layered structure this project doesn't have | Yes | No — presented guesses as fact |
| B — structured | Yes, most complete | Somewhat verbose | Partial |
| C — targeted | Yes, most precise on what it covered | No | Yes — explicitly flagged what it hadn't read |

**Rule:** for correctness-sensitive work (security review, business-rule
review, anything going in front of a grader or teammate who'll act on
it), use Strategy C — targeted context with an explicit
honesty-about-gaps instruction — because a wrong confident answer costs
more than an incomplete honest one.
