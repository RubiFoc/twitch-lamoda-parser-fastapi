from fastapi import FastAPI

from app.config.fastapi_settings import fastapi_settings
from app.utils.exception_handler import exception_handler
from app.routers import twitch

app = FastAPI()

app.add_exception_handler(Exception, exception_handler)
# app.include_router(lamoda.router)
app.include_router(twitch.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=fastapi_settings.host, port=fastapi_settings.port)
