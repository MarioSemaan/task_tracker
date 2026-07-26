from enum import Enum
from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, field_validator, model_validator, computed_field


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: list[str] = []

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v or len(v) > 200:
            raise ValueError("Title must be 1-200 characters after stripping whitespace.")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        cleaned = []
        for tag in v:
            trimmed = tag.strip()
            if not trimmed:
                raise ValueError("Tags must not be empty or whitespace-only.")
            cleaned.append(trimmed)
        return cleaned


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v or len(v) > 200:
            raise ValueError("Title must be 1-200 characters after stripping whitespace.")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is None:
            return v
        cleaned = []
        for tag in v:
            trimmed = tag.strip()
            if not trimmed:
                raise ValueError("Tags must not be empty or whitespace-only.")
            cleaned.append(trimmed)
        return cleaned

    @model_validator(mode="after")
    def at_least_one_field(self):
        if self.model_fields_set == set():
            raise ValueError("At least one field must be provided for an update.")
        return self


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date] = None
    tags: list[str] = []
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def overdue(self) -> bool:
        if self.due_date is None or self.status == TaskStatus.DONE:
            return False
        return self.due_date < date.today()