from fastapi import APIRouter

from core.mongo import MongoService
from models.lamoda import Task, Product
from services.lamoda_services import LamodaService
from services.kafka import KafkaService

router = APIRouter(prefix="/lamoda")
mongo_service = MongoService()
lamoda_service = LamodaService()


@router.post("/parse")
async def start_parsing(task: Task):
    kafka = KafkaService()
    await kafka.send_message("parse", "core.lamoda_parser@parse_lamoda@" + task.category_url)
    return {"message": "Parsed successfully!"}


@router.get("/categories")
async def get_all_categories():
    categories = lamoda_service.get_all_categories()
    return {"Categories": categories}


@router.get("/categories/{category}")
async def get_category(category: str, skip: int = 0, limit: int = 60):
    response = lamoda_service.get_category(category, skip, limit)
    return response


@router.delete("/categories/{category}")
async def delete_category(category: str):
    category = "lamoda_" + category
    mongo_service.drop_collection(category)
    return {"message": "Deleted successfully!"}


@router.post("/categories")
async def create_category(category: str):
    category = "lamoda_" + category
    mongo_service.insert_document(collection_name=category, document={})
    return {"message": "Created successfully!"}


@router.put("/products")
async def update_product(id: str, category: str, query_to_update: Product):
    query = {"_id": id}
    update = {"$set": query_to_update.dict()}
    mongo_service.update_document("lamoda_"+category, query, update)
    return {"message": "Product updated successfully"}


@router.get("/products/{category}/{id}")
async def get_product(category: str, id: str):
    query = {"_id": id}
    product = mongo_service.get_documents("lamoda_"+category, query)
    return product.dict()


@router.post("/products/{category}")
async def create_product(category: str, name: str, price: float, brand: str, link: str):
    category = "lamoda_"+category
    product = Product(name=name, price=price, brand=brand, link=link)
    mongo_service.insert_document(collection_name=category, document=product)
    return {"message": "Product created successfully!"}