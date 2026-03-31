from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    category = Column(String(50))
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    image_url = Column(String(255), nullable=True)
    status = Column(String(20), default="aberto")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="reports")
    comments = relationship("Comment", back_populates="report")