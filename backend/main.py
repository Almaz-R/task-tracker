import os
import json
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from aiokafka import AIOKafkaProducer

app = FastAPI()

# Настройки подключения к БД и Kafka
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BROKER")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)


# Глобальная переменная для продюсера Kafka
producer = None


@app.on_event("startup")
async def startup_event():
    global producer
    Base.metadata.create_all(bind=engine)
    # Инициализация Kafka продюсера
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()


@app.post("/tasks")
async def create_task(task_name: str):
    # 1. Сохраняем в БД
    db = SessionLocal()
    new_task = Task(task_name=task_name)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()

    # 2. Отправляем событие в Kafka
    message = {"task_id": new_task.id, "task_name": task_name}
    await producer.send_and_wait("task-created", json.dumps(message).encode("utf-8"))

    return {"status": "success", "task_id": new_task.id}