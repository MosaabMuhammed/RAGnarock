from fastapi import APIRouter, UploadFile, Depends, status
from fastapi.responses import JSONResponse
from config.settings import get_settings, Settings
from controllers import DataController

data_router = APIRouter(
    prefix="/api/v1",
    tags=["data"],
)

@data_router.post("/upload_file/{project_id}")
async def upload_file(project_id: str, file: UploadFile, app_settings: Settings=Depends(get_settings)):
    is_valid, signal_res = DataController().validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content={"signal": signal_res})
    
    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"signal": signal_res})