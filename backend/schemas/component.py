from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator

class ComponentBase(BaseModel):
    name: str
    category: str = "general"
    quantity: int = 1
    unit_price: float = 0.0
    purchase_link: Optional[str] = None
    notes: Optional[str] = None

    @field_validator('quantity')
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Quantity must not be negative')
        return v

    @field_validator('unit_price')
    @classmethod
    def unit_price_must_not_be_negative(cls, v):
        if v < 0:
            raise ValueError('Unit price must not be negative')
        return v

class ComponentCreate(ComponentBase):
    pass

class ComponentUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    purchase_link: Optional[str] = None
    notes: Optional[str] = None

    @field_validator('quantity')
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('Quantity must not be negative')
        return v

    @field_validator('unit_price')
    @classmethod
    def unit_price_must_not_be_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError('Unit price must not be negative')
        return v

class ComponentOut(ComponentBase):
    id: int
    project_id: int
    total_price: float
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class CostSummaryOut(BaseModel):
    budget: float
    total_spent: float
    remaining_budget: float
    budget_used_percentage: float
    is_over_budget: bool
    over_budget_amount: float
    is_warning: bool
    component_count: int
