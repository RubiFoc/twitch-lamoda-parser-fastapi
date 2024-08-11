import logging

from redis import asyncio as aioredis
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from app.config.kafka_settings import kafka_settings
from app.config.redis_settings import redis_settings


class KafkaService:
    def __init__(self):
        self.bootstrap_servers = kafka_settings.bootstrap_servers
        self.topic = kafka_settings.topic
        self.redis_host = redis_settings.host
        self.redis_port = redis_settings.port
        self.redis_db = redis_settings.db
        self.redis_password = redis_settings.password

        self.logger = logging.getLogger("KafkaService")
        logging.basicConfig(level=logging.INFO)

        self.redis = None
        self.producer = None
        self.consumer = None

    async def connect_redis(self):
        self.redis = await aioredis.create_redis_pool(
            (self.redis_host, self.redis_port),
            db=self.redis_db,
            password=self.redis_password
        )
        self.logger.info("Connected to Redis")

    async def set_cache(self, key: str, value: str, expire: int = 3600):
        await self.redis.set(key, value, expire=expire)
        self.logger.info(f"Set cache for key: {key}")

    async def get_cache(self, key: str):
        value = await self.redis.get(key, encoding='utf-8')
        self.logger.info(f"Got cache for key: {key}, value: {value}")
        return value

    async def connect_kafka_producer(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()
        self.logger.info("Connected to Kafka Producer")

    async def send_message(self, message: str):
        await self.producer.send_and_wait(self.topic, message.encode('utf-8'))
        self.logger.info(f"Sent message to Kafka topic {self.topic}")

    async def connect_kafka_consumer(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id="my_group"
        )
        await self.consumer.start()
        self.logger.info("Connected to Kafka Consumer")

    async def consume_messages(self):
        try:
            async for msg in self.consumer:
                self.logger.info(f"Consumed message: {msg.value.decode('utf-8')}")
        finally:
            await self.consumer.stop()
