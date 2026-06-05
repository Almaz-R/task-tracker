FROM python:3.11-slim
WORKDIR /app
# Копируем из текущей папки (services/backend/)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Копируем всё содержимое папки (services/backend/)
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]