from pydantic.v1 import BaseSettings


class RedisSettings(BaseSettings):
    host: str
    port: int

    class Config:
        env_prefix = 'REDIS_'
        env_file = ".env"
        env_file_encoding = "utf-8"


redis_settings = RedisSettings()

