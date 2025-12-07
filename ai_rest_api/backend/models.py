# app/models.py
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from .database import Base

# SQLAlchemy model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# Pydantic models for validation
class ItemCreate(BaseModel):
    name: str
    description: str

class ItemResponse(ItemCreate):
    id: int

    class Config:
        from_attributes = True
