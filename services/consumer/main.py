import asyncio
import json
import os
from aiokafka import AIOKafkaConsumer


async def consume():
    # Читаем переменные из окружения K8s
    kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka-service:9092')
    kafka_topic = os.getenv('KAFKA_TOPIC', 'task-created')
    group_id = os.getenv('KAFKA_GROUP_ID', 'consumer-group')

    print(f"DEBUG: Initializing consumer with servers={kafka_servers}, topic={kafka_topic}, group={group_id}")

    consumer = AIOKafkaConsumer(
        kafka_topic,
        bootstrap_servers=kafka_servers,
        group_id=group_id,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    await consumer.start()
    print("DEBUG: Consumer fully started and waiting for messages...")

    try:
        async for msg in consumer:
            print(f"DEBUG: Got raw message from partition {msg.partition} at offset {msg.offset}")
            task = msg.value
            print(f"DEBUG: Parsed task data: {task}", flush=True)

            # Логика обработки
            await asyncio.sleep(1)

            print(f"DEBUG: Task {task} processed successfully")
    except Exception as e:
        print(f"ERROR: Exception during consumption: {e}")
    finally:
        print("DEBUG: Stopping consumer...")
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())