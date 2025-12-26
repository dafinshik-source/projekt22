from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session
from . import schemas, crud
from .deps import get_db

router = APIRouter()

@router.get("/posts", response_model=List[schemas.PostRead])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)

@router.post("/posts", response_model=schemas.PostRead, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post)

@router.get("/posts/{post_id}", response_model=schemas.PostRead)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.put("/posts/{post_id}", response_model=schemas.PostRead)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    updated = crud.update_post(db, post_id, post)
    if updated is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated

@router.delete("/posts/{post_id}", response_model=schemas.PostRead)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_post(db, post_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return deleted
