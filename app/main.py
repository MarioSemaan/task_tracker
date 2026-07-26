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
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
    tag: str | None = None,
) -> list[TaskResponse]:
    return storage.get_all_tasks(status=status, priority=priority, overdue=overdue, tag=tag)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
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