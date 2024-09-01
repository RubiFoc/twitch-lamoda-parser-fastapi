import asyncio
import logging

from services.kafka import KafkaService

if __name__ == "__main__":
    kafka = KafkaService()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Consumer")


    async def consume_forever():
        logger.info("Starting")
        while True:
            await kafka.consume_messages("parse", 1)

    asyncio.run(consume_forever())
