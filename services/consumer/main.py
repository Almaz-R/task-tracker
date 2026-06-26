import asyncio
import json
import os
import structlog
from aiokafka import AIOKafkaConsumer

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)
logger = structlog.get_logger()


async def consume():
    kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka-service:9092")
    kafka_topic = os.getenv("KAFKA_TOPIC", "task-created")
    group_id = os.getenv("KAFKA_GROUP_ID", "consumer-group")

    logger.info("consumer_init", servers=kafka_servers, topic=kafka_topic, group_id=group_id)

    consumer = AIOKafkaConsumer(
        kafka_topic,
        bootstrap_servers=kafka_servers,
        group_id=group_id,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    await consumer.start()
    logger.info("consumer_started")

    try:
        async for msg in consumer:
            task = msg.value
            task_id = task.get("task_id")
            task_name = task.get("task_name")

            logger.info(
                "task_processing_started",
                task_id=task_id,
                task_name=task_name,
                partition=msg.partition
            )

            await asyncio.sleep(1)

            logger.info(
                "task_processed_successfully",
                task_id=task_id,
                task_name=task_name
            )

    except Exception as e:
        logger.error("consumer_exception", error=str(e))
    finally:
        logger.info("consumer_stopping")
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())