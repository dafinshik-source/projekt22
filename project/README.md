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