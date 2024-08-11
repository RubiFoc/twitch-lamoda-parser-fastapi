from fastapi import APIRouter, HTTPException

from app.core.mongo import MongoService
from app.core.twitch_parser import get_top_streams_by_query
from app.models.twitch import Filter
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
async def get_category_streamers(collection_name: str, query: str):
    await mongo_service.get_documents(collection_name, query)
