import os
from fastapi import APIRouter

base_router = APIRouter(prefix="/api/v1",
                        tags=["base"])

@base_router.get("/")
def get_health():
    return {"status": "OK"}

@base_router.get("/app_info")
def get_app_info():
    return {
        "app_name": os.getenv("APP_NAME"),
        "app_version": os.getenv("APP_VERSION")
    }