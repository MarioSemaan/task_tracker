# Comments Feature — Plan Comparison (NOT implemented)

Per Module 5 Part 5.4: this is a planning exercise only. Nothing in
`app/` was changed for this document.

## Generic (ungrounded) plan — summary

Asked for a comments-feature plan without pointing the agent at any
repo files. It produced a reasonable-sounding generic plan: a
`Comment` model with `id`, `task_id`, `author`, `body`, `created_at`;
a nested router under `/tasks/{task_id}/comments`; suggested using
SQLAlchemy for persistence and Alembic for migrations; suggested JWT
for identifying the comment author.

Problems: this project has no database and no ORM (see ADR-001) and
no auth system at all — the generic plan assumed both, because it had
no way to know otherwise. It's coherent for "a typical FastAPI app,"
not for *this* app.

## Repo-grounded plan — summary

Same request, but requiring the agent to read `app/models.py`,
`app/storage.py`, `app/main.py`, `tests/test_tasks.py`, and
`AGENTS.md` first. Result: a plan that extends the existing in-memory
dict pattern (a second `_comments: dict[str, CommentResponse]` in
`storage.py`, following the same shape as `_tasks`), reuses the
`extra="forbid"` Pydantic pattern from `models.py`, and proposes
`author` as a plain required string (matching how `assignee` is
already handled as free text) rather than inventing an auth system.

## Field/behavior plan (grounded version)

| Field | Plan |
|---|---|
| `id` | `str(uuid4())`, matching `storage.add_task`'s existing pattern |
| `task_id` | Must reference an existing task id; a comment on a nonexistent task returns 404, mirroring `get_task`'s existing 404 behavior |
| `author` | Required string, 1-100 chars, reusing the `.strip()` + length-check validator pattern from `TaskCreate.validate_title` |
| `body` | Required string, 1-2000 chars, same validator pattern |
| `created_at` | Server-generated UTC datetime, matching `storage.add_task`'s `datetime.now()` call |

## Critique (as tech lead)

| Section | Label | Why |
|---|---|---|
| Storage design (extend the dict pattern) | Right | Matches the existing architecture exactly instead of introducing a database the ADR explicitly rejected. |
| 404 on comment-for-nonexistent-task | Right | Mirrors an existing, tested pattern (`get_task_by_id` returning `None` → 404) rather than inventing new error behavior. |
| `author` as free-text string | Right for this project's scope | There's no auth system, so a free-text author field is consistent with the project's current trust model — but this is the first thing that would need to change if auth were ever added. |
| Test plan | Missing | The grounded plan named the model/storage/route work but didn't propose concrete test names (e.g. `test_create_comment_on_missing_task_returns_404`) — it needs the same naming discipline as `tests/test_tasks.py` already has. |
| Frontend plan | Needs-Resequencing | The grounded plan sketched frontend comment-display UI before settling the API's exact response shape — should follow the project's usual order (model → storage → route → tests → frontend), same order ADR-001 and the existing code already follow. |
| Body length limit (2000 chars) | Right, but unverified | Reasonable default matching the `title` pattern's spirit, but not derived from any actual product requirement — flagged as an assumption, not a fact. |

## Comparison

- The generic plan would have led to real wasted work: implementing
  SQLAlchemy models and JWT auth this project doesn't have and
  explicitly avoids.
- The grounded plan is usable as a starting point specifically because
  it extends patterns that already exist and are already tested — a
  new contributor could implement it by copying `add_task`'s shape.
- A generic plan would still be "enough" for a from-scratch greenfield
  project with no existing conventions to match; it is not enough once
  a codebase already has an established storage and validation pattern
  to be consistent with.
