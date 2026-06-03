import asyncio
import json
from aiokafka import AIOKafkaConsumer

async def consume():
    consumer = AIOKafkaConsumer(
        'task-created',  # Топик, который мы слушаем
        bootstrap_servers='kafka-service:9092', # Внутреннее имя сервиса в K8s
        group_id="consumer-group",
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    await consumer.start()
    try:
        print("Consumer started...")
        async for msg in consumer:
            task = msg.value
            print(f"Received task: {task}")
            # Здесь будет логика обновления статуса в БД (PostgreSQL)
            await asyncio.sleep(1) # Имитация работы
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume())