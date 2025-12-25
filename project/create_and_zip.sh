#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="fastapi-blog"
ZIP_NAME="fastapi-blog.zip"

rm -rf "$ROOT_DIR" "$ZIP_NAME"
mkdir -p "$ROOT_DIR/app"

# README.md (markdown file)
cat > "$ROOT_DIR/README.md" <<'EOF'
# Simple FastAPI Blog (готовый проект)

Простой проект блога на FastAPI + SQLite. Готовые файлы — скопируйте в репозиторий, установите зависимости и запустите.

Требования
- Python 3.10+ (рекомендуется)
- pip

Установка и запуск (локально)
1. Клонируйте/скопируйте файлы в папку проекта.
2. Создайте виртуальное окружение и активируйте его:
   - python -m venv .venv
   - source .venv/bin/activate  (или `.venv\Scripts\activate` на Windows)
3. Установите зависимости:
   - pip install -r requirements.txt
4. Запустите приложение:
   - uvicorn app.main:app --reload
5. Откройте Swagger UI: http://127.0.0.1:8000/docs

API
- GET / -> приветственное сообщение
- GET /posts -> список постов
- POST /posts -> создать пост (JSON: title, content)
- GET /posts/{id} -> получить пост по id
- PUT /posts/{id} -> обновить пост
- DELETE /posts/{id} -> удалить пост

База данных
- SQLite файл `app.db` будет создан автоматически в корне проекта.
- При первом старте в базу добавляются 2 демо-поста.

Docker (опционально)
- Соберите образ и запустите контейнер:
  - docker build -t fastapi-blog .
  - docker run -p 8000:8000 fastapi-blog

Файлы проекта:
- app/ (код приложения)
- requirements.txt
- Dockerfile
- docker-compose.yml
- .gitignore

Автор: подготовлено автоматически
EOF

# .gitignore
cat > "$ROOT_DIR/.gitignore" <<'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.venv/
venv/
env/
*.db
app.db
*.sqlite3
.idea/
.vscode/
EOF

# requirements.txt
cat > "$ROOT_DIR/requirements.txt" <<'EOF'
fastapi==0.95.2
uvicorn[standard]==0.22.0
SQLAlchemy==2.0.20
pydantic==1.10.12
EOF

# Dockerfile
cat > "$ROOT_DIR/Dockerfile" <<'EOF'
# Простая сборка образа для запуска приложения
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# docker-compose.yml
cat > "$ROOT_DIR/docker-compose.yml" <<'EOF'
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - PYTHONUNBUFFERED=1
EOF

# app/__init__.py
cat > "$ROOT_DIR/app/__init__.py" <<'EOF'
# Пакет приложения
EOF

# app/database.py
cat > "$ROOT_DIR/app/database.py" <<'EOF'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# connect_args required only for sqlite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
EOF

# app/models.py
cat > "$ROOT_DIR/app/models.py" <<'EOF'
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
EOF

# app/schemas.py
cat > "$ROOT_DIR/app/schemas.py" <<'EOF'
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
EOF

# app/crud.py
cat > "$ROOT_DIR/app/crud.py" <<'EOF'
from sqlalchemy.orm import Session
from . import models, schemas

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()

def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post: schemas.PostUpdate):
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    if post.title is not None:
        db_post.title = post.title
    if post.content is not None:
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
EOF

# app/deps.py
cat > "$ROOT_DIR/app/deps.py" <<'EOF'
from .database import SessionLocal
from typing import Generator

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
EOF

# app/routes.py
cat > "$ROOT_DIR/app/routes.py" <<'EOF'
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
EOF

# app/main.py
cat > "$ROOT_DIR/app/main.py" <<'EOF'
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
EOF

# Создаём zip
pushd "$ROOT_DIR" >/dev/null
# ничего
popd >/dev/null

zip -r "$ZIP_NAME" "$ROOT_DIR" >/dev/null

echo "Создан архив: $ZIP_NAME"
echo
echo "Чтобы загрузить на transfer.sh и получить ссылку (внимание: внешний сервис), выполните одну из команд:"
echo "  curl --upload-file ./$ZIP_NAME https://transfer.sh/$ZIP_NAME"
echo
echo "Или используйте scp / ваш файловый хостинг. Если хотите, могу сгенерировать base64-строку архива здесь."