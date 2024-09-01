from pydantic.v1 import BaseSettings


class KafkaSettings(BaseSettings):
    bootstrap_servers: str

    class Config:
        env_prefix = 'KAFKA_'
        env_file = ".env"


kafka_settings = KafkaSettings()
