from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
import re

class PortfolioSectionBase(BaseModel):
    section_type: str
    title: Optional[str] = None
    content: Optional[str] = None
    order_index: int = 0
    is_visible: bool = True

class PortfolioSectionCreate(PortfolioSectionBase):
    pass

class PortfolioSectionOut(PortfolioSectionBase):
    id: int
    portfolio_id: int

    model_config = ConfigDict(from_attributes=True)

class PortfolioMediaBase(BaseModel):
    media_url: str
    media_type: str = "image"
    title: Optional[str] = None
    caption: Optional[str] = None
    display_order: int = 0

class PortfolioMediaCreate(PortfolioMediaBase):
    pass

class PortfolioMediaOut(PortfolioMediaBase):
    id: int
    portfolio_id: int

    model_config = ConfigDict(from_attributes=True)

class PortfolioUpdate(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    problem: Optional[str] = None
    solution: Optional[str] = None
    technologies: Optional[str] = None
    architecture_data: Optional[str] = None
    status: Optional[str] = None
    is_published: Optional[bool] = None
    theme: Optional[str] = None

    @field_validator('slug')
    @classmethod
    def slug_must_be_valid(cls, v):
        if v is not None:
            v = v.strip().lower()
            if not v:
                raise ValueError('Slug must not be empty')
            if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$', v):
                raise ValueError('Slug must contain only lowercase letters, numbers, and hyphens')
        return v

class PortfolioOut(BaseModel):
    id: int
    project_id: int
    slug: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    problem: Optional[str] = None
    solution: Optional[str] = None
    technologies: Optional[str] = None
    architecture_data: Optional[str] = None
    status: str
    is_published: bool
    theme: str
    published_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    sections: List[PortfolioSectionOut] = []
    media: List[PortfolioMediaOut] = []

    model_config = ConfigDict(from_attributes=True)

class PublicPortfolioOut(BaseModel):
    id: int
    project_id: int
    slug: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    problem: Optional[str] = None
    solution: Optional[str] = None
    technologies: Optional[str] = None
    architecture_data: Optional[str] = None
    status: str
    is_published: bool
    theme: str
    published_at: Optional[datetime] = None

    # Project metadata
    project_name: str
    project_description: Optional[str] = None
    author_username: str
    author_display_name: Optional[str] = None
    github_url: Optional[str] = None
    kicad_url: Optional[str] = None
    fusion_url: Optional[str] = None
    arduino_url: Optional[str] = None
    docs_url: Optional[str] = None
    demo_url: Optional[str] = None

    # Sections & Media
    sections: List[PortfolioSectionOut] = []
    media: List[PortfolioMediaOut] = []
    
    # Progress & BOM snapshot
    progress_percentage: float = 0.0
    total_spent: float = 0.0
    component_count: int = 0
