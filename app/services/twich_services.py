from core.mongo import MongoService
from models.twitch import Category
from utils.serializer import serialize

mongo_service = MongoService()


class TwichService:
    def get_streamers(self, query):
        streamers = mongo_service.get_documents('twitch_channels', query)
        streamers_list = serialize(streamers)

        streamers_list.sort(key=lambda x: x['viewers_count'], reverse=True)
        response = [{**streamer} for streamer in streamers_list]
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

