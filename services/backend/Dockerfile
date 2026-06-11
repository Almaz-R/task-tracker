FROM python:3.11-slim
WORKDIR /app
# Копируем requirements.txt
COPY requirements.txt .
# Используем --upgrade, чтобы гарантированно применить версии из requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# Копируем остальной код
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]