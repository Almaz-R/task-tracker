import os
import json
import structlog
import logging
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from aiokafka import AIOKafkaProducer
from prometheus_fastapi_instrumentator import Instrumentator

# Настройка логирования в JSON для вывода в stdout
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)
logger = structlog.get_logger()

# Инициализируем приложение
app = FastAPI(root_path=os.getenv("ROOT_PATH", ""))

# Инструментируем приложение
Instrumentator().instrument(app).expose(app)

# Настройки подключения
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BROKER")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)


producer = None


@app.on_event("startup")
async def startup_event():
    global producer
    logger.info("app_startup_started")
    Base.metadata.create_all(bind=engine)
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    logger.info("app_startup_complete")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("app_shutdown_started")
    await producer.stop()
    logger.info("app_shutdown_complete")


@app.post("/tasks")
async def create_task(task_name: str):
    logger.info("create_task_request_received", task_name=task_name)

    db = SessionLocal()
    try:
        new_task = Task(task_name=task_name)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        logger.info("task_saved_to_db", task_id=new_task.id)

        message = {"task_id": new_task.id, "task_name": task_name}
        await producer.send_and_wait("task-created", json.dumps(message).encode("utf-8"))
        logger.info("task_sent_to_kafka", task_id=new_task.id)

        return {"status": "success", "task_id": new_task.id}
    except Exception as e:
        logger.error("task_creation_failed", error=str(e))
        raise
    finally:
        db.close()