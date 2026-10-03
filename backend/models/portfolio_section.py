from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class PortfolioSection(Base):
    __tablename__ = "portfolio_sections"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False, index=True)
    section_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)  # JSON or markdown text
    order_index = Column(Integer, default=0)
    is_visible = Column(Boolean, default=True)

    portfolio = relationship("Portfolio", back_populates="sections")
