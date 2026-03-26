from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="revisor", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class RawNews(Base):
    __tablename__ = "raw_news"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    url = Column(Text, unique=True, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100))
    published_at = Column(TIMESTAMP(timezone=True))
    collected_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    generated_articles = relationship("GeneratedArticle", back_populates="raw_news", cascade="all, delete-orphan")

class GeneratedArticle(Base):
    __tablename__ = "generated_articles"
    id = Column(Integer, primary_key=True, index=True)
    raw_news_id = Column(Integer, ForeignKey("raw_news.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(20), default="draft", nullable=False)
    generated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    raw_news = relationship("RawNews", back_populates="generated_articles")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    action = Column(String(50), nullable=False)
    target_table = Column(String(50), nullable=False)
    target_id = Column(Integer, nullable=False)
    details = Column(JSON)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
