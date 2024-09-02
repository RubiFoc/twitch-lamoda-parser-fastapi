import json

from core.mongo import MongoService
from models.twitch import Category
from services.redis_service import redis_service
from utils.serializer import serialize

mongo_service = MongoService()


class TwichService:
    async def get_streamers(self, query, cache_key):
        cached_data = await redis_service.get(cache_key)

        if cached_data:
            return json.loads(cached_data)
        streamers = mongo_service.get_documents('twitch_channels', query)
        streamers_list = serialize(streamers)

        streamers_list.sort(key=lambda x: x['viewers_count'], reverse=True)
        response = [{**streamer} for streamer in streamers_list]
        await redis_service.set_with_ttl(cache_key, json.dumps(response), 900)
        return response

    def add_category(self, category: Category):
        query = category.dict()
        category_query = {"name": query["name"]}
        id_query = {"id": category.id}
        if mongo_service.db['twitch_categories'].count_documents(category_query) > 0:
            return {"message": "The category already exists!"}
        if mongo_service.db['twitch_categories'].count_documents(id_query) > 0:
            return {"message": "The category with this id already exists!"}
        mongo_service.insert_document('twitch_categories', query)

