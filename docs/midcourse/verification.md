# Verification — Mid-Course Project

## Baseline check (before feature work)

Ran the existing pytest suite before any changes, per ADR-001's Module 1-3 backend.

```
20 passed in 0.06s
```

All 20 pre-existing tests passed. This confirmed a clean starting point before adding due dates and tags.

## Backend test results (after both features)

```
32 passed in 0.08s
```

Breakdown:
- 20 original tests (unchanged, still passing)
- 6 new due-date tests (create with due date, invalid format, overdue detection, Done never overdue, overdue filter, PATCH due date)
- 6 new tags tests (create with tags, empty tag rejected, PATCH tags, tags don't affect unrelated fields, tag filter with matches, tag filter no matches)

This is 12 new tests total, exceeding the 4-new-test minimum required by the brief.

## Manual browser checks

Verified in the browser with the backend running locally:

- New Task modal shows Due date and Tags fields
- Creating a task with a past due date and non-Done status shows a red "Overdue: [date]" pill on the card
- Creating a task with tags shows blue tag chips on the card
- Marking an overdue task as Done removes the overdue pill (consistent with the backend rule that Done tasks are never overdue)
- Typing into the tag filter box narrows the board to matching tasks
- Checking "Overdue only" narrows the board to overdue tasks
- Editing a task prefills due date and tags correctly in the modal

## Behavior contract — before refactor

| ID | Behavior | Pass/Fail |
|----|----------|-----------|
| 1 | Three status columns render with correct counts | PASS |
| 2 | Cards sort by priority (High→Medium→Low) inside each column | PASS |
| 3 | Loading state appears before tasks load | PASS |
| 4 | Empty columns remain visible with placeholder | PASS |
| 5 | Error state appears when backend is stopped | PASS |
| 6 | Valid drag sends PATCH and updates the board | PASS |
| 7 | Invalid drag/server 422 reverts and shows message | PASS |
| 8 | New Task and Edit modal flows work (title trim, due date, tags, 422 handling, dismissal) | PASS |

## Refactor performed

Extracted a `createPill(className, text)` helper function in `frontend/index.html` and used it to replace three duplicated blocks of span-creation code (priority badge, assignee tag, due/overdue pill) inside `renderCard()`. No URLs, class names, status values, or logic were changed — this was a pure deduplication refactor, selected and scoped to one function.

## Behavior contract — after refactor

| ID | Behavior | Pass/Fail |
|----|----------|-----------|
| 1 | Three status columns render with correct counts | PASS |
| 2 | Cards sort by priority (High→Medium→Low) inside each column | PASS |
| 3 | Loading state appears before tasks load | PASS |
| 4 | Empty columns remain visible with placeholder | PASS |
| 5 | Error state appears when backend is stopped | PASS |
| 6 | Valid drag sends PATCH and updates the board | PASS |
| 7 | Invalid drag/server 422 reverts and shows message | PASS |
| 8 | New Task and Edit modal flows work (title trim, due date, tags, 422 handling, dismissal) | PASS |

Full pytest suite also re-run after the refactor and confirmed still passing (32/32), since the refactor was frontend-only.

## Break Test evidence

### Break Test 1 — Due dates (`test_task_with_past_due_date_but_done_is_not_overdue`)

- **Broke:** Removed the `status == TaskStatus.DONE` check from the `overdue` computed property in `app/models.py`.
- **Result:** Test failed — `assert True is False`. With the check removed, a Done task with a past due date incorrectly returned `overdue: True`.
- **Restored:** Added the check back.
- **Re-run:** Test passed again.
- **Conclusion:** The test is meaningful — it correctly catches this specific regression.

### Break Test 2 — Tags (`test_create_task_with_empty_tag_returns_422`)

- **Broke:** Removed the empty/whitespace check from the `tags` field validator in `TaskCreate`.
- **Result:** Test failed — `assert 201 == 422`. With the check removed, a task with a blank tag was created successfully instead of being rejected.
- **Restored:** Added the check back.
- **Re-run:** Test passed again.
- **Conclusion:** The test is meaningful — it correctly catches this specific regression.