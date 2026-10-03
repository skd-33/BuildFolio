from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "Pending"  # Pending, In Progress, Completed
    order_index: int = 0

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Task name must not be empty or whitespace-only')
        return v.strip()

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    order_index: Optional[int] = None

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Task name must not be empty or whitespace-only')
        return v.strip() if v is not None else v

class TaskOut(TaskBase):
    id: int
    project_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
