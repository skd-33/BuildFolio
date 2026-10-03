import re
from typing import List, Optional
from sqlalchemy.orm import Session

from backend.models.project import Project
from backend.models.task import Task
from backend.models.component import Component
from backend.models.portfolio import Portfolio
from backend.schemas.project import ProjectCreate, ProjectUpdate
from backend.services.progress_service import calculate_progress_for_tasks
from backend.services.cost_service import calculate_cost_summary

def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return slug or "project"

def get_project_with_metrics(project: Project) -> dict:
    tasks = project.tasks or []
    components = project.components or []
    
    progress = calculate_progress_for_tasks(tasks)
    cost_summary = calculate_cost_summary(project.budget, components)
    completed_tasks = sum(1 for t in tasks if (t.status or "").lower() == "completed")

    return {
        "id": project.id,
        "user_id": project.user_id,
        "name": project.name,
        "description": project.description,
        "status": project.status,
        "technologies": project.technologies,
        "deadline": project.deadline,
        "budget": project.budget,
        "github_url": project.github_url,
        "kicad_url": project.kicad_url,
        "fusion_url": project.fusion_url,
        "arduino_url": project.arduino_url,
        "docs_url": project.docs_url,
        "demo_url": project.demo_url,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "progress": progress,
        "total_spent": cost_summary["total_spent"],
        "remaining_budget": cost_summary["remaining_budget"],
        "task_count": len(tasks),
        "completed_task_count": completed_tasks,
        "component_count": len(components),
        "tasks": tasks,
        "components": components,
        "portfolio": project.portfolio
    }

def get_user_projects(db: Session, user_id: int) -> List[dict]:
    projects = db.query(Project).filter(Project.user_id == user_id).order_by(Project.created_at.desc()).all()
    return [get_project_with_metrics(p) for p in projects]

def get_project_by_id(db: Session, project_id: int, user_id: Optional[int] = None) -> Optional[Project]:
    query = db.query(Project).filter(Project.id == project_id)
    if user_id is not None:
        query = query.filter(Project.user_id == user_id)
    return query.first()

def create_project(db: Session, user_id: int, data: ProjectCreate) -> Project:
    project = Project(
        user_id=user_id,
        name=data.name,
        description=data.description,
        status=data.status or "planning",
        technologies=data.technologies,
        deadline=data.deadline,
        budget=data.budget or 0.0,
        github_url=data.github_url,
        kicad_url=data.kicad_url,
        fusion_url=data.fusion_url,
        arduino_url=data.arduino_url,
        docs_url=data.docs_url,
        demo_url=data.demo_url,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # Add initial tasks if specified
    if data.initial_tasks:
        for idx, task_name in enumerate(data.initial_tasks):
            if task_name and task_name.strip():
                t = Task(
                    project_id=project.id,
                    name=task_name.strip(),
                    status="Pending",
                    order_index=idx
                )
                db.add(t)

    # Initialize Portfolio for project
    base_slug = slugify(project.name)
    slug = f"{base_slug}-{project.id}"
    portfolio = Portfolio(
        project_id=project.id,
        slug=slug,
        title=project.name,
        subtitle=f"A showcase of {project.name}",
        problem=project.description,
        status="draft",
        is_published=False,
        theme="dark"
    )
    db.add(portfolio)
    db.commit()
    db.refresh(project)
    return project

def update_project(db: Session, project: Project, data: ProjectUpdate) -> Project:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project: Project) -> bool:
    db.delete(project)
    db.commit()
    return True
