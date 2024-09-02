Twitch-Lamoda Parser FastAPI Backend

Overview

This project implements a FastAPI backend for parsing Lamoda website data using BeautifulSoup (bs4) and Twitch API data using requests. The backend utilizes various modern Python technologies and frameworks to create a robust and efficient parsing solution.

Project Structure

The project uses Poetry for dependency management and follows standard Python package structure conventions.

Dependencies

FastAPI: Web framework for building APIs
BeautifulSoup (bs4): HTML parsing library
Requests: HTTP library for API calls
Python-dotenv: Environment variable management
httpx: Async HTTP client
aioredis: Async Redis client
aiokafka: Async Kafka client
pymongo: MongoDB driver

Features

1. Lamoda Parsing:
Utilizes BeautifulSoup to scrape product information from Lamoda website
Handles various product pages and categories
2. Twitch API Integration:
Uses requests to fetch data from Twitch API
Supports various Twitch API endpoints
3. Asynchronous Operations:
Leverages asyncio for efficient handling of concurrent operations
Improves performance when dealing with multiple API calls or web scraping tasks
4. Database Support:
Includes drivers for Redis and MongoDB for data storage and caching
Allows for flexible data persistence options
5. Kafka Integration:
Supports publishing parsed data to Kafka topics for further processing
6. FastAPI Backend:
Provides RESTful APIs for accessing parsed data
Offers automatic interactive documentation via Swagger UI
