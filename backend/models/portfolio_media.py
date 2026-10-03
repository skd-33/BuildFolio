from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class PortfolioMedia(Base):
    __tablename__ = "portfolio_media"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False, index=True)
    media_url = Column(String(500), nullable=False)
    media_type = Column(String(50), default="image")  # image, video, cover, diagram
    title = Column(String(255), nullable=True)
    caption = Column(Text, nullable=True)
    display_order = Column(Integer, default=0)

    portfolio = relationship("Portfolio", back_populates="media")
