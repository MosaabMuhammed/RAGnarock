from fastapi import APIRouter, Depends
from config.settings import get_settings, Settings

base_router = APIRouter(prefix="/api/v1",
                        tags=["base"])

@base_router.get("/")
def get_health():
    return {"status": "OK"}

@base_router.get("/app_info")
def get_app_info(app_settings: Settings=Depends(get_settings)):
    return {
        "app_name": app_settings.APP_NAME,
        "app_version": app_settings.APP_VERSION,
    }