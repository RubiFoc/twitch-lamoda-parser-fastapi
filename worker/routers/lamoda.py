from fastapi import APIRouter, HTTPException

from core.mongo import MongoService
from models.lamoda import Task, Product
from utils.serializer import serialize
from services.kafka import KafkaService

router = APIRouter(prefix="/lamoda")
mongo_service = MongoService()


@router.post("/parse")
async def start_parsing(task: Task):
    kafka = KafkaService()
    await kafka.send_message("parse", "core.lamoda_parser@parse_lamoda@" + task.category_url)
    return {"message": "Parsed successfully!"}


@router.get("/categories")
async def get_all_categories():
    categories = []
    collections = mongo_service.get_collections()
    for collection in collections:
        if 'lamoda' in collection:
            categories.append(collection.split('_')[1])
    return {"Categories": categories}


@router.get("/categories/{category}")
async def get_category(category: str, skip: int = 0, limit: int = 60):
    query = {}
    category_query = 'lamoda_' + category

    total_documents = mongo_service.count_documents(category_query, query)
    total_pages = (total_documents // limit) + (1 if total_documents % limit != 0 else 0)

    if skip >= total_documents:
        raise HTTPException(status_code=404, detail="Page not found")

    products = mongo_service.get_documents(category_query, query, skip=skip, limit=limit)
    product_list = serialize(products)

    next_skip = skip + limit if skip + limit < total_documents else None
    prev_skip = skip - limit if skip - limit >= 0 else None

    return {
        "category": category,
        "total": total_documents,
        "total_pages": total_pages,
        "current_page": (skip // limit) + 1,
        "items": product_list,
        "next_page": f"/categories/{category}?skip={next_skip}&limit={limit}" if next_skip is not None else None,
        "prev_page": f"/categories/{category}?skip={prev_skip}&limit={limit}" if prev_skip is not None else None
    }


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
    mongo_service.update_document("lamoda_" + category, query, update)
    return {"message": "Product updated successfully"}


@router.get("/products/{category}/{id}")
async def get_product(category: str, id: str):
    query = {"_id": id}
    product = mongo_service.get_documents("lamoda_" + category, query)
    return product.dict()


@router.post("/products/{category}")
async def create_product(category: str, name: str, price: float, brand: str, link: str):
    category = "lamoda_" + category
    product = Product(name=name, price=price, brand=brand, link=link)
    mongo_service.insert_document(collection_name=category, document=product)
    return {"message": "Product created successfully!"}
