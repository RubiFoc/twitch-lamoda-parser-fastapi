from pydantic.v1 import BaseSettings


class TwitchSettings(BaseSettings):
    client_id: str
    client_secret: str

    class Config:
        env_prefix = "TWITCH_"
        env_file = "../.env"


twitch_settings = TwitchSettings()
