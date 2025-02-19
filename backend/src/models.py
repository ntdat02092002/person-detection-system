from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class ImageResult(Base):
    __tablename__ = "image_results"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime(timezone=True), server_default=func.now())
    count = Column(Integer, default=0)
    image_path = Column(String, index=True)