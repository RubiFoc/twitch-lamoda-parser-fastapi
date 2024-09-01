from app.core.mongo import MongoService
from app.utils.serializer import serialize

mongo_service = MongoService()


def get_streamers(query):
    streamers = mongo_service.get_documents('twitch_channels', query)
    streamers_list=serialize(streamers)

    streamers_list.sort(key=lambda x: x['viewers_count'], reverse=True)
    response = [{**streamer} for streamer in streamers_list]
    return response