from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str


class Channel(BaseModel):
    channel_name: str
    game_name: str

