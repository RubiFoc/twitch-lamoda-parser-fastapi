from pydantic.v1 import BaseSettings


class FastAPISettings(BaseSettings):
    host: str
    port: int
    debug: bool

    class Config:
        env_prefix = "FASTAPI_"
        env_file = ".env"


fastapi_settings = FastAPISettings()
