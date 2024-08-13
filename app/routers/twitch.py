from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.mongo import MongoService
from app.core.twitch_parser import get_top_streams_by_query
from app.models.twitch import Filter, Category
from app.services.kafka import KafkaService

router = APIRouter(prefix="/twitch")
mongo_service = MongoService()


@router.post("/parse")
async def start_parsing(filter: Filter):
    # kafka = KafkaService()
    # await kafka.send_message("parse", "app.core.twitch_parser@get_top_streams_by_query" + filter.query)
    await get_top_streams_by_query(filter.query)
    return {"message": "Parsed successfully!"}


@router.post("/get_streamers_by_category")
async def get_top_category_streamers(category: str):
    query = {"game_name": category}
    streamers = mongo_service.get_documents('twitch_channels', query)
    streamers_list = []
    for streamer in streamers:
        streamer['_id'] = str(streamer['_id'])
        streamers_list.append(streamer)

    streamers_list.sort(key=lambda x: x['viewers_count'], reverse=True)
    response = [{**streamer} for streamer in streamers_list]
    return jsonable_encoder({category: response})


@router.post("/add_category")
async def add_category(category: Category):
    query = category.dict()
    category_query = {"name": query["name"]}
    id_query = {"id": category.id}
    if mongo_service.db['twitch_categories'].count_documents(category_query) > 0:
        return {"message": "The category already exists!"}
    if mongo_service.db['twitch_categories'].count_documents(id_query) > 0:
        return {"message": "The category with this id already exists!"}
    mongo_service.insert_document('twitch_categories', query)
    return {"message": "Added successfully!"}


@router.post("/delete_category")
async def delete_category(category: Category):
    query = category.dict()
    mongo_service.delete_document('twitch_categories', query)
    return {"message": "Deleted successfully!"}


@router.post("/update_category")
async def update_category(category_to_update: Category, new_values: Category):
    mongo_service.update_document('twitch_categories', category_to_update.dict(), new_values.dict())
