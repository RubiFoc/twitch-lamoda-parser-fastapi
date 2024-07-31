from pydantic.v1 import BaseSettings


class RedisSettings(BaseSettings):
    host: str
    port: int
    db: int
    password: str

    class Config:
        env_prefix = 'REDIS_'
        env_file = '.env'


redis_settings = RedisSettings()