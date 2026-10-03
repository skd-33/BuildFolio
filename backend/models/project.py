from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from backend.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="planning")
    technologies = Column(Text, nullable=True)
    deadline = Column(String(50), nullable=True)
    budget = Column(Float, default=0.0)

    # CAD, code and document links
    github_url = Column(String(500), nullable=True)
    kicad_url = Column(String(500), nullable=True)
    fusion_url = Column(String(500), nullable=True)
    arduino_url = Column(String(500), nullable=True)
    docs_url = Column(String(500), nullable=True)
    demo_url = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan", order_by="Task.order_index")
    components = relationship("Component", back_populates="project", cascade="all, delete-orphan")
    portfolio = relationship("Portfolio", back_populates="project", uselist=False, cascade="all, delete-orphan")
