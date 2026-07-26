# app/storage.py
from typing import Optional
from uuid import uuid4
from datetime import datetime
from .models import TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority

_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now()
    task_id = str(uuid4())
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return task


def get_all_tasks(
    status=None,
    priority=None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
    tasks = list(_tasks.values())
    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    if overdue is not None:
        tasks = [t for t in tasks if t.overdue == overdue]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
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
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    _tasks.clear()