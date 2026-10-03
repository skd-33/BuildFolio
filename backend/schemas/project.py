from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from backend.schemas.task import TaskOut
from backend.schemas.component import ComponentOut
from backend.schemas.portfolio import PortfolioOut

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "planning"
    technologies: Optional[str] = None
    deadline: Optional[str] = None
    budget: float = 0.0
    github_url: Optional[str] = None
    kicad_url: Optional[str] = None
    fusion_url: Optional[str] = None
    arduino_url: Optional[str] = None
    docs_url: Optional[str] = None
    demo_url: Optional[str] = None

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Project name must not be empty or whitespace-only')
        return v.strip()

    @field_validator('budget')
    @classmethod
    def budget_must_not_be_negative(cls, v):
        if v < 0:
            raise ValueError('Budget must be >= 0')
        return v

class ProjectCreate(ProjectBase):
    initial_tasks: Optional[List[str]] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    technologies: Optional[str] = None
    deadline: Optional[str] = None
    budget: Optional[float] = None
    github_url: Optional[str] = None
    kicad_url: Optional[str] = None
    fusion_url: Optional[str] = None
    arduino_url: Optional[str] = None
    docs_url: Optional[str] = None
    demo_url: Optional[str] = None

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Project name must not be empty or whitespace-only')
        return v.strip() if v is not None else v

    @field_validator('budget')
    @classmethod
    def budget_must_not_be_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError('Budget must be >= 0')
        return v

class ProjectOut(ProjectBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Computed metrics
    progress: float = 0.0
    total_spent: float = 0.0
    remaining_budget: float = 0.0
    task_count: int = 0
    completed_task_count: int = 0
    component_count: int = 0
    
    tasks: Optional[List[TaskOut]] = None
    components: Optional[List[ComponentOut]] = None
    portfolio: Optional[PortfolioOut] = None

    model_config = ConfigDict(from_attributes=True)
