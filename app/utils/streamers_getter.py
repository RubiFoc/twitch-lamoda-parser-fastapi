from app.core.mongo import MongoService

mongo_service = MongoService()


def get_streamers(query):
    streamers = mongo_service.get_documents('twitch_channels', query)
    streamers_list = []
    for streamer in streamers:
        streamer['_id'] = str(streamer['_id'])
        streamers_list.append(streamer)

    streamers_list.sort(key=lambda x: x['viewers_count'], reverse=True)
    response = [{**streamer} for streamer in streamers_list]
    return response
