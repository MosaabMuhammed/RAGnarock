from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_SUPPORTED_TYPES: list
    FILE_MAX_SIZE_MB: int

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()