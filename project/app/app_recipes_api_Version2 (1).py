from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session
from . import schemas, crud
from .deps import get_db

router = APIRouter(prefix="/api/recipes", tags=["recipes_api"])

@router.get("/", response_model=List[schemas.RecipeRead])
def api_list_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_recipes(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.RecipeRead, status_code=status.HTTP_201_CREATED)
def api_create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, recipe)

@router.get("/{recipe_id}", response_model=schemas.RecipeRead)
def api_get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = crud.get_recipe(db, recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe

@router.put("/{recipe_id}", response_model=schemas.RecipeRead)
def api_update_recipe(recipe_id: int, recipe: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    updated = crud.update_recipe(db, recipe_id, recipe)
    if updated is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated

@router.delete("/{recipe_id}", response_model=schemas.RecipeRead)
def api_delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_recipe(db, recipe_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return deleted