from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Task Tracker Backend is up and running!"}

@app.post("/tasks")
def create_task(task_name: str):
    # Логика работы с Postgres и Kafka будет добавлена здесь
    return {"status": "success", "task": task_name}