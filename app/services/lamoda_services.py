import json

from fastapi import HTTPException

from core.mongo import MongoService
from models.lamoda import Product
from services.redis_service import redis_service
from utils.serializer import serialize

mongo_service = MongoService()


class LamodaService:
    async def get_all_categories(self, cache_key=None):
        cached_data = await redis_service.get(cache_key)

        if cached_data:
            return {"Categories": json.loads(cached_data)}

        collections = mongo_service.get_collections()
        categories = []
        for collection in collections:
            if 'lamoda' in collection:
                categories.append(collection.split('_')[1])
        return categories


    async def get_category(self, category: str, skip: int = 0, limit: int = 60, cache_key=None):
        cached_data = await redis_service.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

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

        response = {
            "category": category,
            "total": total_documents,
            "total_pages": total_pages,
            "current_page": (skip // limit) + 1,
            "items": product_list,
            "next_page": f"/categories/{category}?skip={next_skip}&limit={limit}" if next_skip is not None else None,
            "prev_page": f"/categories/{category}?skip={prev_skip}&limit={limit}" if prev_skip is not None else None
        }
        return response

    async def get_product(self, category: str, id, cache_key=None):
        cached_data = await redis_service.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

        query = {"_id": id}
        product = mongo_service.get_documents("lamoda_" + category, query)
        await redis_service.set_with_ttl(cache_key, json.dumps(product.dict()), 900)  # 15 минут
        return product


    async def create_product(self, category, name, price, brand, link):
        product = Product(name=name, price=price, brand=brand, link=link)
        mongo_service.insert_document(collection_name="lamoda_" + category, document=product)

        # Очистка кэша для этой категории
        cache_keys = await redis_service.keys(f"product_{category}_*")
        if cache_keys:
            await redis_service.delete(*cache_keys)
