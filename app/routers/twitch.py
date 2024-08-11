from fastapi import APIRouter, HTTPException

from app.core.mongo import MongoService
from app.models.twich import Filter
from app.services.kafka import KafkaService

router = APIRouter(prefix="/twitch")
mongo_service = MongoService()


@router.post("/parse")
async def start_parsing(filter: Filter):
    kafka = KafkaService()
    await kafka.send_message("parse", "app.core.twich_parser@get_top_streams_by_query" + filter.query)
    return {"message": "Parsed successfully!"}

