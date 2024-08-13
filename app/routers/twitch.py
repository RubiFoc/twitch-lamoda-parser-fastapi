from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from app.core.mongo import MongoService
from app.core.twitch_parser import get_top_streams_by_query
from app.models.twitch import Filter, Category, Channel
from app.services.kafka import KafkaService
from app.utils.streamers_getter import get_streamers

router = APIRouter(prefix="/twitch")
mongo_service = MongoService()


@router.post("/parse")
async def start_parsing(filter: Filter):
    # kafka = KafkaService()
    # await kafka.send_message("parse", "app.core.twitch_parser@get_top_streams_by_query" + filter.query)
    await get_top_streams_by_query(filter.query)
    return {"message": "Parsed successfully!"}


@router.get("/streamers/{category}")
async def get_top_category_streamers(category: str):
    query = {"game_name": category}
    response = get_streamers(query)
    return jsonable_encoder({category: response})


@router.get("/streamers_by_nick/{nick}")
async def get_streamer_by_nick(nick: str):
    query = {"channel_name": nick}
    response = get_streamers(query)
    return response


@router.get("/streamers")
async def get_all_parsed_streamers():
    query = {}
    response = get_streamers(query)
    return response


@router.delete("/streamers/{id}")
async def delete_streamer_by_id(id: str):
    query = {"_id": ObjectId(id)}
    mongo_service.delete_document('twitch_streamers', query)
    return {"message": "Deleted successfully!"}


@router.put("/streamers/{id}")
async def update_streamer_by_id(id: str, channel: Channel):
    query = {"_id": id}
    update = {"$set": channel.dict()}
    mongo_service.update_document("twitch_channels", query, update)
    return {"message": "Channel updated successfully"}


@router.post("/categories")
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


@router.delete("/categories/{category_id}")
async def delete_category(category_id):
    query = {"_id": category_id}
    mongo_service.delete_document('twitch_categories', query)
    return {"message": "Deleted successfully!"}


@router.put("/categories/{id}")
async def update_category(category_id: str, category: Category):
    query = {"_id": category_id}
    update = {"$set": category.dict()}
    mongo_service.update_document("twitch_categories", query, update)
    return {"message": "Category updated successfully"}
