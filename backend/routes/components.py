from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.models.component import Component
from backend.schemas.component import ComponentCreate, ComponentUpdate, ComponentOut, CostSummaryOut
from backend.middleware.auth import get_current_user
from backend.services.project_service import get_project_by_id
from backend.services.cost_service import calculate_cost_summary

router = APIRouter(tags=["components"])

@router.get("/api/projects/{project_id}/components", response_model=List[ComponentOut])
def list_components(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db.query(Component).filter(Component.project_id == project_id).all()

@router.post("/api/projects/{project_id}/components", response_model=ComponentOut, status_code=status.HTTP_201_CREATED)
def create_component(
    project_id: int,
    data: ComponentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    qty = max(1, data.quantity)
    unit_p = max(0.0, data.unit_price)
    tot_p = round(qty * unit_p, 2)

    component = Component(
        project_id=project_id,
        name=data.name,
        category=data.category or "general",
        quantity=qty,
        unit_price=unit_p,
        total_price=tot_p,
        purchase_link=data.purchase_link,
        notes=data.notes
    )
    db.add(component)
    db.commit()
    db.refresh(component)
    return component

@router.put("/api/components/{component_id}", response_model=ComponentOut)
def update_component(
    component_id: int,
    data: ComponentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    project = get_project_by_id(db, component.project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=403, detail="Not authorized to edit this component")

    update_dict = data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(component, field, value)

    # Recalculate total_price
    component.total_price = round(component.quantity * component.unit_price, 2)

    db.commit()
    db.refresh(component)
    return component

@router.delete("/api/components/{component_id}", status_code=status.HTTP_200_OK)
def delete_component(
    component_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    project = get_project_by_id(db, component.project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=403, detail="Not authorized to delete this component")

    db.delete(component)
    db.commit()
    return {"message": "Component deleted successfully", "id": component_id}

@router.get("/api/projects/{project_id}/costs", response_model=CostSummaryOut)
def get_cost_summary(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    components = db.query(Component).filter(Component.project_id == project_id).all()
    summary = calculate_cost_summary(project.budget, components)
    return CostSummaryOut(**summary)
