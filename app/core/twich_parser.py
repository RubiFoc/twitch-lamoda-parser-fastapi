import os
import asyncio
import httpx
from app.config.twich_settings import twitch_settings


async def get_top_streams_by_query(filter_type_and_query, limit=100):
    filter_type, query = filter_type_and_query.split('&')
    query = query.replace('_', ' ')
    # Получение токена доступа
    token_url = "https://id.twitch.tv/oauth2/token"
    token_params = {
        "client_id": twitch_settings.client_id,
        "client_secret": twitch_settings.client_secret,
        "grant_type": "client_credentials"
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, params=token_params)
        token_response.raise_for_status()
        access_token = token_response.json()['access_token']

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Client-Id': twitch_settings.client_id
        }

        if filter_type == 'category':
            # Получение ID категории
            category_url = 'https://api.twitch.tv/helix/games'
            category_params = {'name': query}
            category_response = await client.get(category_url, headers=headers, params=category_params)

            if category_response.status_code != 200:
                print(f"Error getting category: {category_response.status_code}")
                return []

            category_data = category_response.json()
            if not category_data['data']:
                print(f"No category found with the name {query}")
                return []

            category_id = category_data['data'][0]['id']

            # Получение стримов по категории
            streams_url = 'https://api.twitch.tv/helix/streams'
            streams_params = {
                'game_id': category_id,
                'first': limit  # Получение топовых `limit` стримов
            }
        elif filter_type == 'channel':
            # Получение стримов по каналу
            streams_url = 'https://api.twitch.tv/helix/streams'
            streams_params = {
                'user_login': query,
                'first': limit  # Получение топовых `limit` стримов
            }
        else:
            print(f"Unknown filter type: {filter_type}")
            return []

        streams_response = await client.get(streams_url, headers=headers, params=streams_params)

        if streams_response.status_code != 200:
            print(f"Error getting streams: {streams_response.status_code}")
            return []

        return streams_response.json()['data']


async def main():
    # Пример использования
    filter_type_and_query = 'category&Just_Chatting'  # или 'channel&example_channel'
    streams = await get_top_streams_by_query(filter_type_and_query, limit=10)

    for stream in streams:
        print(f"Streamer: {stream['user_name']}, Title: {stream['title']}, Viewers: {stream['viewer_count']}")


if __name__ == "__main__":
    asyncio.run(main())
