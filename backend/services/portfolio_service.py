from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from backend.models.portfolio import Portfolio
from backend.models.portfolio_section import PortfolioSection
from backend.models.portfolio_media import PortfolioMedia
from backend.models.project import Project
from backend.schemas.portfolio import PortfolioUpdate, PublicPortfolioOut
from backend.services.progress_service import calculate_progress_for_tasks

def get_portfolio_by_project_id(db: Session, project_id: int) -> Optional[Portfolio]:
    return db.query(Portfolio).filter(Portfolio.project_id == project_id).first()

def get_portfolio_by_slug(db: Session, slug: str) -> Optional[Portfolio]:
    return db.query(Portfolio).filter(Portfolio.slug == slug.lower().strip()).first()

def update_portfolio(db: Session, portfolio: Portfolio, data: PortfolioUpdate) -> Portfolio:
    update_data = data.model_dump(exclude_unset=True)
    
    # If is_published changed to True, set published_at
    if update_data.get("is_published") is True and not portfolio.is_published:
        portfolio.published_at = datetime.now(timezone.utc)
        portfolio.status = "published"
    elif update_data.get("is_published") is False:
        portfolio.status = "draft"

    for field, value in update_data.items():
        setattr(portfolio, field, value)
        
    db.commit()
    db.refresh(portfolio)
    return portfolio

def get_public_portfolio_view(db: Session, slug: str) -> Optional[PublicPortfolioOut]:
    portfolio = get_portfolio_by_slug(db, slug)
    if not portfolio or not portfolio.is_published:
        return None

    project = portfolio.project
    author = project.user
    tasks = project.tasks or []
    components = project.components or []

    progress = calculate_progress_for_tasks(tasks)
    total_spent = sum(c.total_price for c in components)

    return PublicPortfolioOut(
        id=portfolio.id,
        project_id=portfolio.project_id,
        slug=portfolio.slug,
        title=portfolio.title or project.name,
        subtitle=portfolio.subtitle,
        problem=portfolio.problem or project.description,
        solution=portfolio.solution,
        technologies=portfolio.technologies or project.technologies,
        architecture_data=portfolio.architecture_data,
        status=portfolio.status,
        is_published=portfolio.is_published,
        theme=portfolio.theme or "dark",
        published_at=portfolio.published_at,
        project_name=project.name,
        project_description=project.description,
        author_username=author.username,
        author_display_name=author.display_name or author.username,
        github_url=project.github_url,
        kicad_url=project.kicad_url,
        fusion_url=project.fusion_url,
        arduino_url=project.arduino_url,
        docs_url=project.docs_url,
        demo_url=project.demo_url,
        sections=portfolio.sections or [],
        media=portfolio.media or [],
        progress_percentage=progress,
        total_spent=round(total_spent, 2),
        component_count=len(components)
    )
