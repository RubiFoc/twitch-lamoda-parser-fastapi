from pydantic.v1 import BaseSettings


class MongoSettings(BaseSettings):
    host: str
    port: int
    database: str

    class Config:
        env_prefix = 'MONGO_'
        env_file = ".env"


mongo_settings = MongoSettings()
