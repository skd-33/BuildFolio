from typing import Literal
from pydantic import BaseModel, Field

Status = Literal["confirmed", "inferred", "unknown"]

class Fact(BaseModel):
    value: str
    status: Status = "inferred"
    source: str = ""

class ProjectKnowledge(BaseModel):
    summary: str = ""
    problem: str = ""
    solution: str = ""
    hardware: list[Fact] = Field(default_factory=list)
    software: list[Fact] = Field(default_factory=list)
    architecture: list[Fact] = Field(default_factory=list)
    challenges: list[Fact] = Field(default_factory=list)
    future_improvements: list[Fact] = Field(default_factory=list)
