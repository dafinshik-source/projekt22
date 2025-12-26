from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .deps import get_db
from . import crud, schemas

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/", include_in_schema=False)
def site_index(request: Request, db: Session = Depends(get_db)):
    recipes = crud.get_recipes(db)
    return templates.TemplateResponse("index.html", {"request": request, "recipes": recipes})

@router.get("/recipes/{recipe_id}", include_in_schema=False)
def site_recipe_detail(request: Request, recipe_id: int, db: Session = Depends(get_db)):
    recipe = crud.get_recipe(db, recipe_id)
    if not recipe:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("recipe_detail.html", {"request": request, "recipe": recipe})

@router.get("/recipes/create", include_in_schema=False)
def site_recipe_create_form(request: Request):
    return templates.TemplateResponse("create_recipe.html", {"request": request})

@router.post("/recipes/create", include_in_schema=False)
async def site_recipe_create(request: Request, title: str = Form(...), ingredients: str = Form(...), instructions: str = Form(...), db: Session = Depends(get_db)):
    recipe_in = schemas.RecipeCreate(title=title, ingredients=ingredients, instructions=instructions)
    recipe = crud.create_recipe(db, recipe_in)
    return RedirectResponse(url=f"/recipes/{recipe.id}", status_code=303)