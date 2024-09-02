from bson import ObjectId
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from core.mongo import MongoService
from models.twitch import Filter, Category, Channel
from services.kafka import KafkaService
from services.twich_services import TwichService

router = APIRouter(prefix="/twitch")
mongo_service = MongoService()
twitch_service = TwichService()


@router.post("/parse")
async def start_parsing(filter: Filter):
    kafka = KafkaService()
    await kafka.send_message("parse", "core.twitch_parser@get_top_streams_by_query@" + filter.query)
    return {"message": "Parsed successfully!"}


@router.get("/streamers/{category}")
async def get_top_category_streamers(category: str):
    cache_key = f"category_{category}"
    query = {"game_name": category}
    response = await twitch_service.get_streamers(query, cache_key)
    return jsonable_encoder({category: response})


@router.get("/streamers_by_nick/{nick}")
async def get_streamer_by_nick(nick: str):
    query = {"channel_name": nick}
    response = await twitch_service.get_streamers(query, None)
    return response


@router.get("/streamers")
async def get_all_parsed_streamers():
    cache_key = "all_parsed_streamers"
    query = {}
    response = await twitch_service.get_streamers(query, cache_key)
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
    await twitch_service.add_category(category)
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
