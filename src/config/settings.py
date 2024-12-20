from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_SUPPORTED_TYPES: list
    FILE_MAX_SIZE_MB: int
    FILE_CHUNK_SIZE_BYTES: int

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    
    OPENAI_API_KEY: str=None
    OPENAI_API_URL: str=None
    COHERE_API_KEY: str=None
    GENERATION_MODEL_ID: str=None
    EMBEDDING_MODEL_ID: str=None
    EMBEDDING_MODEL_SIZE: int=None
    MAX_INPUT_TOKENS: int=None
    MAX_OUTPUT_TOKENS: int=None
    TEMPERATURE: float=None

    VECTORDB_BACKEND: str=None
    VECTORDB_PATH: str=None
    VECTORDB_DISTANCE_METHOD: str=None

    DEFAULT_LANG: str
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()