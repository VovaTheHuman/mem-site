from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

# SQLAlchemy модель (таблиця)
class MemeDB(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    image_url = Column(String)
    category = Column(String, index=True)
    created_at = Column(DateTime)

# Pydantic моделі
class MemeBase(BaseModel):
    title: str
    image_url: str
    category: str

class MemeCreate(MemeBase):
    pass

class Meme(MemeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
