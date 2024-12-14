from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_SUPPORTED_TYPES: list
    FILE_MAX_SIZE_MB: int
    FILE_CHUNK_SIZE_BYTES: int
    MONGODB_URL: str
    MONGODB_DB: str
    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str=None
    OPENAI_API_URL: str=None
    COHERE_API_KEY: str=None
    GENERATION_MODEL_ID: str=None
    EMBEDDING_MODEL_ID: str=None
    EMBEDDING_MODEL_SIZE: int=None
    MAX_INPUT_TOKENS: int=None
    MAX_OUTPUT_TOKENS: int=None
    TEMPERATURE: float=None


    class Config:
        env_file = ".env"

def get_settings():
    return Settings()