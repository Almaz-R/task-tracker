import os
from fastapi import FastAPI
from sqlalchemy import create_engine # Пример библиотеки для работы с БД

app = FastAPI()

# Получаем настройки из переменных окружения (заданных в docker-compose)
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Строка подключения к БД
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

@app.get("/")
def read_root():
    return {"message": "Task Tracker Backend is up and running!"}

@app.post("/tasks")
def create_task(task_name: str):
    # Здесь позже будет код для записи в Postgres через DATABASE_URL
    return {"status": "success", "task": task_name, "db_connected": True}