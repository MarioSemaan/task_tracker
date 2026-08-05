# FILE: app/business_rules.py
"""Business rules for task status transitions.

This module is the single source of truth for which status transitions
are allowed. Keeping the rule here (instead of inline in main.py) means
the API layer, tests, and any future CLI/worker code all check the same
rule instead of re-implementing it.
"""
from fastapi import HTTPException, status
from app.models import TaskStatus

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    """Raise a 422 if a status change is not an allowed transition.

    Args:
        current: The task's status before the update.
        new: The status requested in the PATCH payload.

    Raises:
        HTTPException: 422 Unprocessable Entity if (current, new) is not
            a member of VALID_TRANSITIONS. This includes same-status
            "transitions" (e.g. ToDo -> ToDo), which are treated as
            invalid rather than a silent no-op.
    """
    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({f"{f.value}->{t.value}" for f, t in VALID_TRANSITIONS})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )
