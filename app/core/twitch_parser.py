import asyncio

import httpx

from app.config.twitch_settings import twitch_settings  # Ensure the correct import path
from app.core.mongo import MongoService
from app.models.twitch import Category, Channel


async def get_top_streams_by_query(filter_type_and_query, limit=100):
    filter_type, query = filter_type_and_query.split('&')

    params = {
        "query": query,
        "limit": limit,
    }
    token_url = "https://id.twitch.tv/oauth2/token"
    token_params = {
        "client_id": twitch_settings.client_id,
        "client_secret": twitch_settings.client_secret,
        "grant_type": "client_credentials"
    }

    if filter_type == "category":
        url = 'https://api.twitch.tv/helix/search/categories'
    elif filter_type == "channel":
        url = 'https://api.twitch.tv/helix/search/channels'

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, params=token_params)
        token_response.raise_for_status()
        data_token = token_response.json()

        headers = {
            'Authorization': f'Bearer {data_token["access_token"]}',
            'Client-Id': twitch_settings.client_id
        }

        response = await client.get(url, headers=headers, params=params)
        data = response.json()
        if response.status_code == 200:
            mongo_service = MongoService()
            if filter_type == "category":
                categories = data['data']
                for category in categories:
                    twitch_category = Category(id=category['id'], name=category['name'])
                    mongo_service.insert_document("twitch_categories", twitch_category.dict())

            elif filter_type == "channel":
                channels = data['data']
                for channel in channels:
                    if channel['is_live'] is True:
                        stream_params = {"user_login": channel['broadcaster_login']}
                        stream_response = await client.get("https://api.twitch.tv/helix/streams", headers=headers,
                                                           params=stream_params)
                        stream_data = stream_response.json()
                        twitch_channel = Channel(channel_name=channel['broadcaster_login'],
                                                 game_name=channel['game_name'],
                                                 viewers_count=stream_data['data'][0]['viewer_count'])
                        mongo_service.insert_document("twitch_channels", twitch_channel.dict())
                    else:
                        twitch_channel = Channel(channel_name=channel['broadcaster_login'],
                                                 game_name=channel['game_name'],
                                                 viewers_count=0)
                        mongo_service.insert_document("twitch_channels", twitch_channel.dict())
        else:
            print({'message': response.text}, response.status_code)
            return {'message': response.text}, response.status_code
