# User Stories — Mid-Course Project

## Feature 1: Due dates + overdue filter

**Story 1 — Set a due date when creating a task**
As a user, I want to optionally set a due date when creating a task, so I can track deadlines.
- Acceptance criteria:
  - `due_date` is optional on create.
  - Accepts ISO date format (`YYYY-MM-DD`).
  - Invalid date format returns 422.

**Story 2 — Update a task's due date**
As a user, I want to edit a task's due date, so I can adjust deadlines as plans change.
- Acceptance criteria:
  - PATCH supports updating `due_date` independently of other fields.
  - Invalid format on update returns 422, same as create.

**Story 3 — See overdue tasks flagged on the board**
As a user, I want overdue tasks visually marked, so I can spot what's late at a glance.
- Acceptance criteria:
  - A task is overdue if `due_date` is before today AND status is not Done.
  - Overdue tasks show a visible pill/indicator on their card.
  - Overdue is computed by the backend, not stored as a separate field — corrected AI assumption: initial draft suggested storing an `is_overdue` boolean directly on the task, which would go stale between requests; overdue must be computed at read-time instead.

**Story 4 — Filter the board to only overdue tasks**
As a user, I want to filter to overdue tasks only, so I can prioritize what's late.
- Acceptance criteria:
  - `GET /tasks?overdue=true` returns only overdue tasks.
  - Filter can combine with existing status/priority filters.

## Feature 2: Tags / labels

**Story 1 — Add tags when creating a task**
As a user, I want to add tags to a task, so I can categorize work beyond status/priority.
- Acceptance criteria:
  - `tags` is an optional list of strings on create.
  - Each tag is trimmed; empty/whitespace-only tags are rejected with 422.

**Story 2 — Edit a task's tags**
As a user, I want to update a task's tags, so my categorization stays current.
- Acceptance criteria:
  - PATCH supports replacing the `tags` list.
  - Updating tags does not affect unrelated fields (title, status, etc.).

**Story 3 — See tags on task cards**
As a user, I want to see tags as chips on each card, so I can identify categories without opening the task.
- Acceptance criteria:
  - Each tag renders as a small chip/pill on the card.
  - Cards with no tags show no chips (not an empty placeholder chip) — corrected AI assumption: initial draft suggested always rendering an "Untagged" chip, which adds visual noise for the common case of no tags.

**Story 4 — Filter tasks by tag**
As a user, I want to filter the board by a specific tag, so I can focus on one category of work.
- Acceptance criteria:
  - `GET /tasks?tag=<value>` returns only tasks containing that tag.
  - No matches returns 200 with an empty list, not 404.
