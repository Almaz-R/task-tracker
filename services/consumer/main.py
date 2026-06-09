import asyncio
import json
import os
from aiokafka import AIOKafkaConsumer


async def consume():
    # Читаем переменные из окружения K8s
    kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka-service:9092')
    kafka_topic = os.getenv('KAFKA_TOPIC', 'tasks')
    group_id = os.getenv('KAFKA_GROUP_ID', 'consumer-group')

    consumer = AIOKafkaConsumer(
        kafka_topic,
        bootstrap_servers=kafka_servers,
        group_id=group_id,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    await consumer.start()
    try:
        print(f"Consumer started on {kafka_servers}, topic: {kafka_topic}...")
        async for msg in consumer:
            task = msg.value
            print(f"Received task: {task}")
            # Здесь будет логика работы с БД
            await asyncio.sleep(1)
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())