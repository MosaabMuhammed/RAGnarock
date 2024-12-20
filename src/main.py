from fastapi import FastAPI

from routes import base_router, data_router, index_router, answer_router
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import get_settings
from contextlib import asynccontextmanager
from llms import LLMProviderFactory
from llms.prompts import PromptParser
from vectordbs import VectorDBFactory

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client  = app.mongo_conn[settings.APP_NAME]

    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_factory     = VectorDBFactory(settings)

    app.generation_client = llm_provider_factory.create(settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(settings.GENERATION_MODEL_ID)
    app.generation_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                                embed_size=settings.EMBEDDING_MODEL_SIZE)

    app.embedding_client  = llm_provider_factory.create(settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                             embed_size=settings.EMBEDDING_MODEL_SIZE)
    
    app.vectordb_client = vectordb_factory.create(settings.VECTORDB_BACKEND)
    app.vectordb_client.connect()

    app.prompt_parser = PromptParser(lang=settings.DEFAULT_LANG,
                                     default_lang=settings.DEFAULT_LANG)

    yield

    app.mongo_conn.close()
    app.vectordb_client.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(base_router)
app.include_router(data_router)
app.include_router(index_router)
app.include_router(answer_router)