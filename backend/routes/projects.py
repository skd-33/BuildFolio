from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from backend.middleware.auth import get_current_user
from backend.services.project_service import (
    get_user_projects,
    get_project_by_id,
    create_project,
    update_project,
    delete_project,
    get_project_with_metrics
)

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("", response_model=List[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_projects(db, current_user.id)

@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def new_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = create_project(db, current_user.id, data)
    return get_project_with_metrics(project)

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return get_project_with_metrics(project)

@router.put("/{project_id}", response_model=ProjectOut)
def edit_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    updated = update_project(db, project, data)
    return get_project_with_metrics(updated)

@router.delete("/{project_id}", status_code=status.HTTP_200_OK)
def remove_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    delete_project(db, project)
    return {"message": "Project deleted successfully", "id": project_id}
