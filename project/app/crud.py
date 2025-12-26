from typing import TYPE_CHECKING
from sqlalchemy.orm import Session
from . import models

if TYPE_CHECKING:
    from . import schemas

# ----- Posts (существующие функции) -----
def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()

def create_post(db: Session, post: "schemas.PostCreate"):
    db_post = models.Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post: "schemas.PostUpdate"):
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    if getattr(post, "title", None) is not None:
        db_post.title = post.title
    if getattr(post, "content", None) is not None:
        db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    db.delete(db_post)
    db.commit()
    return db_post

# ----- Recipes (новые функции) -----
def get_recipe(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

def get_recipes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Recipe).order_by(models.Recipe.created_at.desc()).offset(skip).limit(limit).all()

def create_recipe(db: Session, recipe: "schemas.RecipeCreate"):
    db_recipe = models.Recipe(title=recipe.title, ingredients=recipe.ingredients, instructions=recipe.instructions)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def update_recipe(db: Session, recipe_id: int, recipe: "schemas.RecipeUpdate"):
    db_recipe = get_recipe(db, recipe_id)
    if not db_recipe:
        return None
    if getattr(recipe, "title", None) is not None:
        db_recipe.title = recipe.title
    if getattr(recipe, "ingredients", None) is not None:
        db_recipe.ingredients = recipe.ingredients
    if getattr(recipe, "instructions", None) is not None:
        db_recipe.instructions = recipe.instructions
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def delete_recipe(db: Session, recipe_id: int):
    db_recipe = get_recipe(db, recipe_id)
    if not db_recipe:
        return None
    db.delete(db_recipe)
    db.commit()
    return db_recipe
