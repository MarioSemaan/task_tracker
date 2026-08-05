from datetime import datetime, timezone

from fastapi import status, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import TaskCreate, TaskResponse, TaskStatus, TaskPriority, TaskUpdate
from app import storage
from app.business_rules import validate_status_transition

app = FastAPI(
    title="Task Tracker API",
    description="A minimal learning-project REST API for tracking tasks.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Args:
        payload: TaskCreate body. title is required (1-200 chars after
            stripping whitespace); description, status, priority, and
            assignee are optional and fall back to their defaults
            (status=ToDo, priority=Medium, description="").

    Returns:
        TaskResponse: The newly created task, including its generated
        id, created_at, and updated_at timestamps.

    Raises:
        HTTPException: 422 if title is missing/blank/too long, an enum
            value is invalid, or the payload contains an unknown field
            (models use extra="forbid").

    Example:
        POST /tasks {"title": "Write tests"} -> 201
        {"id": "...", "title": "Write tests", "status": "ToDo", ...}
    """
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered by status and/or priority.

    Args:
        status: Optional query param. If given, only tasks with this
            exact status are returned.
        priority: Optional query param. If given, only tasks with this
            exact priority are returned. Combined with status using AND
            when both are supplied.

    Returns:
        list[TaskResponse]: Matching tasks, or an empty list if none
        match (this is not a 404 case).

    Example:
        GET /tasks?status=Done&priority=High -> 200 [...]
    """
    return storage.get_all_tasks(status=status, priority=priority)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Fetch a single task by id.

    Args:
        task_id: The task's UUID (path parameter).

    Returns:
        TaskResponse: The matching task.

    Raises:
        HTTPException: 404 if no task with this id exists.

    Example:
        GET /tasks/{id} -> 200 {"id": "...", "title": "...", ...}
        GET /tasks/does-not-exist -> 404 {"detail": "Task with id ... not found"}
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Partially update a task.

    Args:
        task_id: The task's UUID (path parameter).
        payload: TaskUpdate body. At least one field must be set; only
            the fields provided are changed (unset fields are left
            untouched). If status is provided, it must be a legal
            transition from the task's current status per
            business_rules.VALID_TRANSITIONS
            (ToDo->InProgress, InProgress->Done, Done->InProgress).

    Returns:
        TaskResponse: The task after the update, with updated_at
        refreshed.

    Raises:
        HTTPException: 404 if the task does not exist. 422 if the
            payload is empty, contains an unknown field, or requests a
            status transition that is not in VALID_TRANSITIONS
            (including a same-status "transition", e.g. ToDo -> ToDo).

    Example:
        PATCH /tasks/{id} {"status": "InProgress"} -> 200
        PATCH /tasks/{id} {"status": "Done"} on a ToDo task -> 422
    """
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing.status, payload.status)

    updated_task = storage.update_task(task_id, payload)
    if updated_task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return updated_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str):
    """Delete a task by id.

    Args:
        task_id: The task's UUID (path parameter).

    Returns:
        None. On success the response has no body.

    Raises:
        HTTPException: 404 if no task with this id exists.

    Example:
        DELETE /tasks/{id} -> 204 (no body)
        DELETE /tasks/does-not-exist -> 404 {"detail": "Task with id ... not found"}
    """
    deleted = storage.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")


@app.get("/health")
def health_check() -> dict:
    """
    Simple liveness check.

    Returns a fixed status field and the current UTC timestamp in
    ISO 8601 format so you can confirm the server is up and responding.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }