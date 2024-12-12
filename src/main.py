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
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client  = app.mongo_conn[settings.APP_NAME]

    yield

    app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)
app.include_router(base_router)
app.include_router(data_router)