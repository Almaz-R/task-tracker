import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

# Подключение (берем из переменных окружения)
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Модель таблицы (должна совпадать с той, что ты создал в DBeaver)
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)

@app.post("/tasks")
def create_task(task_name: str):
    db = SessionLocal()
    new_task = Task(task_name=task_name)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()
    return {"status": "success", "task_id": new_task.id}