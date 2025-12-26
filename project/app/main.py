from fastapi import FastAPI
from .database import engine, Base, SessionLocal
from . import models
from .routes import router as posts_router
from sqlalchemy.orm import Session

app = FastAPI(title="Simple FastAPI Blog")

app.include_router(posts_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Simple FastAPI Blog. Visit /docs for API docs."}

@app.on_event("startup")
def startup():
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)

    # Seed demo data если пусто
    db: Session = SessionLocal()
    try:
        count = db.query(models.Post).count()
        if count == 0:
            demo_posts = [
                models.Post(title="Hello, FastAPI", content="Это первый демонстрационный пост."),
                models.Post(title="Second post", content="Ещё один пример поста.")
            ]
            db.add_all(demo_posts)
            db.commit()
    finally:
        db.close()
