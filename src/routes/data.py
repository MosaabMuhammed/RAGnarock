from fastapi import APIRouter, UploadFile, Depends
from config.settings import get_settings, Settings
from controllers import DataController

data_router = APIRouter(
    prefix="/api/v1",
    tags=["data"],
)

@data_router.post("/upload_file")
async def upload_file(file: UploadFile, app_settings: Settings=Depends(get_settings)):
    is_valid = DataController().validate_uploaded_file(file=file)

    return is_valid