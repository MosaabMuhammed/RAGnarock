from fastapi import FastAPI

from routes import base_router, data_router
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import get_settings
from contextlib import asynccontextmanager
from llms import LLMProviderFactory

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client  = app.mongo_conn[settings.APP_NAME]

    llm_provider_factory = LLMProviderFactory(settings)

    app.generation_client = llm_provider_factory.create(settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(settings.GENERATION_MODEL_ID)

    app.embedding_client  = llm_provider_factory.create(settings.EMBEDDING_BACKEND)
    app.embedding_client.set_generation_model(model_id=settings.EMBEDDING_MODEL_ID,
                                              embed_size=settings.EMBEDDING_MODEL_SIZE)

    yield

    app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)
app.include_router(base_router)
app.include_router(data_router)