from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

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
