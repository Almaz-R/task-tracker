import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from models import Base, Task  # Импортируем наши модели (чертежи таблиц)

app = FastAPI()

# Получаем настройки из переменных окружения (из docker-compose.yml)
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Формируем строку подключения
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

# Создаем движок SQLAlchemy
engine = create_engine(DATABASE_URL)

# Это «магия», которая создает таблицы в БД при запуске приложения, если их еще нет
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Task Tracker is connected to DB and running!"}

@app.post("/tasks")
def create_task(task_name: str):
    # Пока оставляем заглушку, но теперь мы уверены, что БД подключена и таблицы созданы
    return {"status": "success", "task": task_name, "db_connected": True}