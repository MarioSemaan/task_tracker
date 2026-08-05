# Architecture Document — Strategy C (Targeted Context)

*Produced with the agent restricted to three anchor files only:
`app/main.py`, `app/models.py`, `app/storage.py` — explicitly
instructed to say "not visible from the files I read" rather than
guess about anything else.*

## System overview
Based only on the three anchor files: a FastAPI app with five task
routes plus `/health`, Pydantic models with a custom title validator,
and a dict-backed storage module.

## Backend structure
- `app/main.py` — confirmed: routes, CORS middleware config
- `app/models.py` — confirmed: TaskCreate/TaskUpdate/TaskResponse
- `app/storage.py` — confirmed: `_tasks` dict and CRUD functions
- `app/business_rules.py` — **not visible from the files I read** — `app/main.py` imports `validate_status_transition` from it, so it clearly exists and is used, but its contents weren't provided in this context strategy.
- `frontend/`, `tests/` — **not visible from the files I read**

## Data flow
Route → Pydantic validation → storage function call. The exact status-
transition logic could not be described in detail since
`business_rules.py` wasn't in the provided context — only that
`update_task` calls something named `validate_status_transition`
before writing.

## Known limits
Explicitly declined to guess at test coverage, frontend behavior, or
deployment setup, since none of those files were provided.

## Notes
Noticeably shorter and more precise than A or B, and — importantly —
honest about its blind spots instead of filling them in with plausible
guesses. For a task like "review the status-transition business rule,"
Strategy C's honesty about not having read `business_rules.py` is more
useful than a confident-sounding guess would have been.
