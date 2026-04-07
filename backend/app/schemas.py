from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NewsBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
    category: Optional[str] = "Geral"

class NewsCreate(NewsBase):
    pass

class NewsOut(NewsBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class HeroBannerBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
    image_url: str
    link_url: Optional[str] = None
    is_active: bool = True

class HeroBannerCreate(HeroBannerBase):
    pass

class HeroBannerOut(HeroBannerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
