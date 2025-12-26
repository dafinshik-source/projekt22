from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Post schemas (оставлены прежними)
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostRead(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Recipe schemas
class RecipeBase(BaseModel):
    title: str
    ingredients: str
    instructions: str

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    ingredients: Optional[str] = None
    instructions: Optional[str] = None

class RecipeRead(RecipeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
