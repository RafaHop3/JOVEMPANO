from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class RawNewsBase(BaseModel):
    source: str
    title: str
    url: HttpUrl
    content: str
    author: Optional[str] = None
    published_at: Optional[datetime] = None

class RawNewsCreate(RawNewsBase):
    pass

class RawNews(RawNewsBase):
    id: int
    collected_at: datetime

    class Config:
        orm_mode = True

class GeneratedArticleSchema(BaseModel):
    title: str
    subtitle: str
    content: str
    tags: list[str]
    sources: list[str]
