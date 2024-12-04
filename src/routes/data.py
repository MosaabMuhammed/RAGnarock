from fastapi import APIRouter, UploadFile, Depends, status
from fastapi.responses import JSONResponse
from config.settings import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseSignals
import aiofiles
from .schemas.data import ProcessData

data_router = APIRouter(
    prefix="/api/v1",
    tags=["data"],
)

@data_router.post("/upload_file/{project_id}")
async def upload_file(project_id: str, file: UploadFile, app_settings: Settings=Depends(get_settings)):
    data_controller = DataController()

    is_valid, signal_res = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content={"signal": signal_res})
    

    file_path, file_id = data_controller.generate_unique_filepath(orig_file_name=file.filename,
                                                                   project_id=project_id)

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE_BYTES):
                await f.write(chunk)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            content={"signal": ResponseSignals.FILE_UPLOAD_FAILED})

    return JSONResponse(status_code=status.HTTP_201_CREATED, 
                        content={"signal": ResponseSignals.FILE_UPLOAD_SUCCESS,
                                 "file_id": file_id})

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_data: ProcessData):

    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_id=process_data.file_id)
    chunks = process_controller.process_file_content(file_content=file_content,
                                                     chunk_size=process_data.chunk_size,
                                                     overlap_size=process_data.overlap_size)

    if not chunks or len(chunks) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"signal": ResponseSignals.PROCESS_FAILED})



    return chunks