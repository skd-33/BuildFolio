from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models.user import User
from backend.models.portfolio import Portfolio
from backend.models.portfolio_section import PortfolioSection
from backend.models.portfolio_media import PortfolioMedia
from backend.schemas.portfolio import (
    PortfolioOut, PortfolioUpdate,
    PortfolioSectionCreate, PortfolioSectionOut,
    PortfolioMediaCreate, PortfolioMediaOut
)
from backend.middleware.auth import get_current_user
from backend.services.project_service import get_project_by_id
from backend.services.portfolio_service import (
    get_portfolio_by_project_id,
    update_portfolio,
)

router = APIRouter(tags=["portfolio"])

@router.get("/api/projects/{project_id}/portfolio", response_model=PortfolioOut)
def get_portfolio(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    portfolio = get_portfolio_by_project_id(db, project_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.put("/api/projects/{project_id}/portfolio", response_model=PortfolioOut)
def update_project_portfolio(
    project_id: int,
    data: PortfolioUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    portfolio = get_portfolio_by_project_id(db, project_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # If slug is changing, verify uniqueness (case-insensitive)
    if data.slug and data.slug != portfolio.slug:
        slug_lower = data.slug.strip().lower()
        existing = db.query(Portfolio).filter(
            func.lower(Portfolio.slug) == slug_lower
        ).first()
        if existing and existing.id != portfolio.id:
            raise HTTPException(status_code=400, detail="Custom slug is already taken")

    updated = update_portfolio(db, portfolio, data)
    return updated

@router.post("/api/projects/{project_id}/portfolio/sections", response_model=PortfolioSectionOut, status_code=status.HTTP_201_CREATED)
def add_portfolio_section(
    project_id: int,
    data: PortfolioSectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    portfolio = get_portfolio_by_project_id(db, project_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    section = PortfolioSection(
        portfolio_id=portfolio.id,
        section_type=data.section_type,
        title=data.title,
        content=data.content,
        order_index=data.order_index,
        is_visible=data.is_visible
    )
    db.add(section)
    db.commit()
    db.refresh(section)
    return section

@router.delete("/api/portfolio/sections/{section_id}", status_code=status.HTTP_200_OK)
def remove_portfolio_section(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    section = db.query(PortfolioSection).filter(PortfolioSection.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    portfolio = db.query(Portfolio).filter(Portfolio.id == section.portfolio_id).first()
    project = get_project_by_id(db, portfolio.project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=403, detail="Not authorized to delete this section")

    db.delete(section)
    db.commit()
    return {"message": "Section deleted successfully", "id": section_id}

@router.post("/api/projects/{project_id}/portfolio/media", response_model=PortfolioMediaOut, status_code=status.HTTP_201_CREATED)
def add_portfolio_media(
    project_id: int,
    data: PortfolioMediaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    portfolio = get_portfolio_by_project_id(db, project_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    media = PortfolioMedia(
        portfolio_id=portfolio.id,
        media_url=data.media_url,
        media_type=data.media_type,
        title=data.title,
        caption=data.caption,
        display_order=data.display_order
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    return media

@router.delete("/api/portfolio/media/{media_id}", status_code=status.HTTP_200_OK)
def remove_portfolio_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    media = db.query(PortfolioMedia).filter(PortfolioMedia.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    portfolio = db.query(Portfolio).filter(Portfolio.id == media.portfolio_id).first()
    project = get_project_by_id(db, portfolio.project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=403, detail="Not authorized to delete this media")

    db.delete(media)
    db.commit()
    return {"message": "Media deleted successfully", "id": media_id}
