from pydantic import BaseModel


class Task(BaseModel):
    category_url: str


class Product(BaseModel):
    name: str
    price: float
    brand: str
    link: str
