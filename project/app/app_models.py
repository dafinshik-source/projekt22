from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    ingredients = Column(Text, nullable=False)   # Markdown / plain text list
    instructions = Column(Text, nullable=False)  # Steps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
