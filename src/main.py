from fastapi import FastAPI
# from dotenv import load_dotenv

# load_dotenv()

from routes import base_router, data_router
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import get_settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db     = app.client[settings.MONGODB_DB]

    yield

    app.db.client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(base_router)
app.include_router(data_router)