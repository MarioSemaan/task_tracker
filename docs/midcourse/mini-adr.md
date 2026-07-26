# Mini-ADR — Mid-Course Feature Extensions

## Context

Extending the Task Tracker (see ADR-001) with two features: due dates + overdue filtering, and tags/labels. Both must fit the existing in-memory Pydantic store without introducing a database.

## Decision: Due dates

- `due_date` stored as an ISO date string (`YYYY-MM-DD`) on the Task model, optional field.
- Validated via Pydantic — invalid format returns 422 automatically.
- `overdue` is **not** stored on the task. It is computed at read-time: `due_date < today AND status != "Done"`.
  - Alternative considered: storing `is_overdue` as a persisted boolean, recalculated on every mutation. Rejected — this duplicates state that's trivially derivable, and risks going stale if the day changes without a task being touched (e.g. a task becomes overdue overnight with no PATCH triggering a recalculation).
- The overdue filter is implemented as a query parameter (`GET /tasks?overdue=true`), applied as a filter over the same computed logic, combinable with existing `status`/`priority` filters.

## Decision: Tags

- `tags` stored as `List[str]` on the Task model, optional, defaults to an empty list.
- Each tag is trimmed on input; empty/whitespace-only tags are rejected with 422.
- No enforced maximum count or length — kept simple for a learning project's scope.
- Alternative considered: comma-separated string field. Rejected — a list is more natural to validate per-item (trim, reject blanks) and avoids parsing/serialization logic on every read/write.
- Tag filtering implemented as `GET /tasks?tag=<value>`, returning tasks where the tag list contains an exact (case-sensitive) match. No matches returns 200 with `[]`, not 404, consistent with existing status/priority filter behavior.

## Consequences

- Both features stay consistent with ADR-001's in-memory, no-database approach — no migration or schema change needed.
- Overdue status will differ depending on "today," so tests must control or mock the current date rather than relying on wall-clock time at test-run time.
- Case-sensitive tag matching is a known limitation — flagged here rather than silently assumed; acceptable for this learning project's scope.
