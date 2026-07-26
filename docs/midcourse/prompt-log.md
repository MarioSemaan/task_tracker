# Prompt Log — Mid-Course Project
## Feature 1: Due dates + overdue filter

### F1-P1 — Design decision (mini-ADR)

**Prompt category:** Planning / design decision

```
I'm extending my FastAPI Task Tracker (in-memory Pydantic store, no database,
per ADR-001) with a due_date feature.

Recommend:
1. What format/type due_date should be stored as.
2. Whether "overdue" should be a stored field or computed at read-time.

Constraints:
- Must stay consistent with the in-memory, no-database architecture in ADR-001.
- Do not write code yet — decision only, with reasoning.
```


**AI response / what I did with it:** Recommended `due_date` as an ISO date string validated by Pydantic, and `overdue` computed at read-time via a property rather than stored, since a stored boolean could go stale without an explicit recalculation trigger. Accepted as-is — this became the `mini-adr.md` decision.

---

### F1-P2 — Implementation

**Prompt category:** Feature implementation / scoped diff


```
Add an optional due_date field (type date) to TaskCreate, TaskUpdate, and
TaskResponse in app/models.py.

Add a computed `overdue` property on TaskResponse that returns False if
due_date is None or status is Done, otherwise True if due_date is before
today.

Add an overdue query filter to GET /tasks.

Constraints:
- Do not change existing status-transition or priority logic.
- Return the full updated app/models.py, app/storage.py, and app/main.py.
```

**AI response / what I did with it:** Produced the three-file diff using Pydantic's native `date` type for automatic format validation. Accepted in full — all 20 existing tests still passed unchanged after applying it.

---

### F1-P3 — Test generation

**Prompt category:** Test design + generation

```
Brainstorm edge cases for the due_date/overdue feature, then generate pytest
tests for:
- valid due date
- invalid format
- overdue detection when not Done
- overdue is false when Done
- filtering by overdue=true
- PATCH updating due_date without affecting other fields

Use the existing client/created_task fixture pattern from tests/test_tasks.py.
```

**AI response / what I did with it:** Generated 6 tests. One test (Done tasks are never overdue) needed a correction before running: the AI's first draft assumed a direct ToDo→Done transition was allowed, but the actual `business_rules.py` only permits the sequential ToDo→InProgress→Done path — this was caught and fixed before running the test.

---

### F1-P4 — Break Test

**Prompt category:** Test verification / deliberate breakage

```
I added this pytest test and it currently passes:
test_task_with_past_due_date_but_done_is_not_overdue

Tell me the smallest temporary source-code change that should make this
test fail if the test is meaningful.

Constraints:
- Do not modify or weaken the test.
- Reminder to restore the source after the failure check.
```

**AI response / what I did with it:** Suggested temporarily removing the `status == TaskStatus.DONE` check from the `overdue` computed property. Ran the test with the break applied — it failed with `assert True is False`, confirming the test catches the regression. Restored the original code and re-ran to confirm it passed again.


---

## Feature 2: Tags / labels

### F2-P1 — Design decision (mini-ADR)

**Prompt category:** Planning / design decision

```
Recommend whether tags should be a list field or a comma-separated string
on the Task model, with validation for empty/whitespace tags. Consider
that this must stay consistent with the in-memory Pydantic architecture
(no database) from ADR-001.
```


**AI response / what I did with it:** Recommended `List[str]`, validated per-item (trim + reject blank), over a comma-separated string, since a list validates each tag independently and avoids parsing/serialization logic on every read/write. Accepted as-is, documented in `mini-adr.md`.


---

### F2-P2 — Implementation

**Prompt category:** Feature implementation / scoped diff

```
Add an optional tags: list[str] field (default []) to TaskCreate,
TaskUpdate, and TaskResponse in app/models.py.

Add a field validator that trims each tag and rejects empty/whitespace-only
tags with a validation error.

Add a tag query parameter to GET /tasks that filters tasks containing an
exact match.

Constraints:
- Do not change due-date or status-transition logic.
- Return the full updated app/models.py, app/storage.py, and app/main.py.
```

**AI response / what I did with it:** Produced the scoped diff across the same three files, reusing the pattern established for due dates. Accepted in full — all 26 tests (20 original + 6 due-date) still passed unchanged.

---

### F2-P3 — Test generation

**Prompt category:** Test design + generation

```
Generate pytest tests for:
- creating with tags
- rejecting an empty tag
- updating tags without affecting other fields
- filtering by tag with matches
- filtering by tag with no matches

Use the same fixture pattern as the due-date tests in tests/test_tasks.py.
```

**AI response / what I did with it:** Generated 6 tests following the same pattern. Accepted all 6 without edits.

---

### F2-P4 — Break Test

**Prompt category:** Test verification / deliberate breakage

```
I added this pytest test and it currently passes:
test_create_task_with_empty_tag_returns_422

Tell me the smallest temporary change to break it, if it's meaningful.

Constraints:
- Do not modify or weaken the test.
- Reminder to restore the source after the failure check.
```

**AI response / what I did with it:** Suggested removing the `if not trimmed: raise ValueError(...)` check from the `TaskCreate` tags validator. Broke it, re-ran — test failed with `assert 201 == 422`, confirming it catches the regression. Restored the original validator and confirmed the test passed again.
