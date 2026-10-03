from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.models.task import Task
from backend.schemas.task import TaskCreate, TaskUpdate, TaskOut
from backend.middleware.auth import get_current_user
from backend.services.project_service import get_project_by_id

router = APIRouter(tags=["tasks"])

@router.get("/api/projects/{project_id}/tasks", response_model=List[TaskOut])
def list_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db.query(Task).filter(Task.project_id == project_id).order_by(Task.order_index).all()

@router.post("/api/projects/{project_id}/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: int,
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # If order_index not explicitly provided, put it at end
    current_count = db.query(Task).filter(Task.project_id == project_id).count()
    order_idx = data.order_index if data.order_index > 0 else current_count

    task = Task(
        project_id=project_id,
        name=data.name,
        description=data.description,
        status=data.status or "Pending",
        order_index=order_idx
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.put("/api/tasks/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = get_project_by_id(db, task.project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=403, detail="Not authorized to edit this task")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

@router.delete("/api/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = get_project_by_id(db, task.project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully", "id": task_id}
