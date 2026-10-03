from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from backend.database import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=True)
    subtitle = Column(Text, nullable=True)
    problem = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)
    technologies = Column(Text, nullable=True)
    architecture_data = Column(Text, nullable=True)  # JSON string
    status = Column(String(20), default="draft")     # draft, published
    is_published = Column(Boolean, default=False)
    theme = Column(String(50), default="dark")
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="portfolio")
    sections = relationship("PortfolioSection", back_populates="portfolio", cascade="all, delete-orphan", order_by="PortfolioSection.order_index")
    media = relationship("PortfolioMedia", back_populates="portfolio", cascade="all, delete-orphan", order_by="PortfolioMedia.display_order")
