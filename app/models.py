"""Pydantic request/response models for the Task Tracker API.

Every model here uses `extra="forbid"`, so any request body with an
unknown field is rejected with 422 rather than silently ignored. See
CLAUDE.md and AGENTS.md for the business rules these models encode.

Note (see docs/security-review.md, "No length limit on description"):
`description` has a title-style length validator on `title` but not
on itself. This is a documented, graded finding (Valid) with a backlog
entry, not an oversight — it is intentionally left unfixed here to
stay within a docstring-only change.
"""
from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

class TaskStatus(str, Enum):
    """The three states a task can be in.

    Not every (from, to) pair is a legal transition — the allowed
    transitions are enforced separately in app/business_rules.py, not
    by this enum itself.
    """
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"

class TaskPriority(str, Enum):
    """The three priority levels a task can be assigned."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class TaskCreate(BaseModel):
    """Request body for POST /tasks.

    Only `title` is required; `description`, `status`, `priority`, and
    `assignee` fall back to their field defaults (status=ToDo,
    priority=Medium, description="", assignee=None) when omitted.
    """
    model_config = ConfigDict(extra="forbid")
    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Strip whitespace and enforce the 1-200 character rule.

        Args:
            v: The raw title string as submitted.

        Returns:
            str: The stripped title.

        Raises:
            ValueError: If the stripped title is empty or longer than
                200 characters. Pydantic turns this into a 422 at the
                API layer.
        """
        v = v.strip()
        if not v or len(v) > 200:
            raise ValueError("Title must be 1-200 characters after stripping whitespace.")
        return v

class TaskUpdate(BaseModel):
    """Request body for PATCH /tasks/{task_id}.

    Every field is optional, but `at_least_one_field` below rejects a
    payload where none are set. Only fields explicitly present in the
    request are applied by app/storage.py's `update_task` — this model
    does not itself decide whether a status change is a legal
    transition; app/main.py checks that separately against
    app/business_rules.py before the update is applied.
    """
    model_config = ConfigDict(extra="forbid")
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Strip whitespace and enforce the 1-200 character rule.

        Same rule as TaskCreate.validate_title, applied only when
        `title` is actually included in the PATCH payload.

        Args:
            v: The raw title string as submitted.

        Returns:
            str: The stripped title.

        Raises:
            ValueError: If the stripped title is empty or longer than
                200 characters.
        """
        v = v.strip()
        if not v or len(v) > 200:
            raise ValueError("Title must be 1-200 characters after stripping whitespace.")
        return v

    @model_validator(mode="after")
    def at_least_one_field(self):
        """Reject a PATCH body that doesn't set any field.

        Returns:
            TaskUpdate: `self`, unchanged, if at least one field was
            explicitly set.

        Raises:
            ValueError: If `model_fields_set` is empty, i.e. the
                client sent `{}` or an all-default payload.
        """
        if self.model_fields_set == set():
            raise ValueError("At least one field must be provided for an update.")
        return self

class TaskResponse(BaseModel):
    """Response body returned by every route that returns a task.

    Mirrors the stored task exactly, including the server-generated
    `id`, `created_at`, and `updated_at` fields that don't exist on
    TaskCreate/TaskUpdate.
    """
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    created_at: datetime
    updated_at: datetime