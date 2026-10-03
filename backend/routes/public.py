from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.portfolio import PublicPortfolioOut
from backend.services.portfolio_service import get_public_portfolio_view

router = APIRouter(prefix="/api/public", tags=["public"])

@router.get("/portfolio/{slug}", response_model=PublicPortfolioOut)
def get_public_portfolio(
    slug: str,
    db: Session = Depends(get_db)
):
    portfolio_view = get_public_portfolio_view(db, slug)
    if not portfolio_view:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Showcase portfolio not found or not published"
        )
    return portfolio_view
