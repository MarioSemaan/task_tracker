# app/storage.py
"""In-memory persistence layer for the Task Tracker.

This module is the single source of truth for how tasks are stored.
There is no database: `_tasks` is a plain dict that lives for the
lifetime of the running process (see docs/adr/ADR-001-backend-architecture.md
for why). All CRUD functions read from or write to this one dict, and
`_reset()` exists purely so tests can start from a clean slate.
"""
from typing import Optional
from uuid import uuid4
from datetime import datetime
from .models import TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority

_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a new task.

    Args:
        payload: A validated TaskCreate. Pydantic has already enforced
            the title length/blank rules and applied defaults
            (status=ToDo, priority=Medium, description="") before this
            function is called.

    Returns:
        TaskResponse: The newly stored task, with a generated UUID
        `id` and `created_at`/`updated_at` both set to the current
        local time.
    """
    now = datetime.now()
    task_id = str(uuid4())
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return task


def get_all_tasks(status=None, priority=None) -> list[TaskResponse]:
    """Return all stored tasks, optionally filtered by status/priority.

    Args:
        status: If given, only tasks with this exact status are kept.
        priority: If given, only tasks with this exact priority are
            kept. Combined with `status` using AND when both are set.

    Returns:
        list[TaskResponse]: Matching tasks in insertion order, or an
        empty list if none match. Never raises for "no results" —
        that is a 200 with an empty list at the API layer, not a 404.
    """
    tasks = list(_tasks.values())
    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Look up a single task by id.

    Args:
        task_id: The task's UUID.

    Returns:
        Optional[TaskResponse]: The matching task, or None if no task
        with this id exists. Callers (app/main.py) are responsible for
        turning a None result into a 404 — this function never raises.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Apply a partial update to an existing task.

    Args:
        task_id: The task's UUID.
        payload: A validated TaskUpdate. Only fields explicitly set on
            the payload (`exclude_unset=True`) are applied; unset
            fields leave the stored task untouched. Note: this
            function does not itself validate status transitions —
            app/main.py calls `business_rules.validate_status_transition`
            before calling this function whenever `payload.status` is set.

    Returns:
        Optional[TaskResponse]: The task after the update, with
        `updated_at` refreshed to the current local time, or None if
        no task with this id exists.
    """
    task = _tasks.get(task_id)
    if not task:
        return None

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(task, field, value)
    task.updated_at = datetime.now()
    _tasks[task_id] = task
    return task


def delete_task(task_id: str) -> bool:
    """Delete a task by id.

    Args:
        task_id: The task's UUID.

    Returns:
        bool: True if a task with this id existed and was removed,
        False if no task with this id was found. app/main.py turns a
        False result into a 404.
    """
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    """Clear all stored tasks.

    Test-only helper. `tests/conftest.py` calls this in an autouse
    fixture before every test so tests never leak state into each
    other. Not used by the running application.
    """
    _tasks.clear()