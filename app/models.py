from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

    
class Roll(Base):
    __tablename__ = "rolls"

    id = Column(Integer, primary_key=True)
    length = Column(Integer, index=True)
    weight = Column(Float, index=True)
    dateadd = Column(DateTime(timezone=True), server_default=func.now())
    dateremove = Column(DateTime, index=True)
