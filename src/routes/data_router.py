from fastapi import APIRouter, UploadFile, Depends, status, Request
from fastapi.responses import JSONResponse
from config.settings import get_settings, Settings
from controllers import DataController, ProcessController
from models import ResponseSignals
import aiofiles
import logging
from .schemas.data import ProcessData
from models import ProjectModel, ChunkModel, AssetModel
from models.db_schemas import Chunk, Asset
from models.enums import AssetTypeEnums

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1",
    tags=["data"],
)

@data_router.post("/upload_file/{project_id}")
async def upload_file(request: Request, 
                      project_id: str, 
                      file: UploadFile, 
                      app_settings: Settings=Depends(get_settings)):
    data_controller = DataController()

    is_valid, signal_res = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content={"signal": signal_res})
    
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project       = await project_model.get_or_create_one(project_id=project_id)
    

    file_path, file_id = data_controller.generate_unique_filepath(orig_file_name=file.filename,
                                                                   project_id=project_id)

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE_BYTES):
                await f.write(chunk)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            content={"signal": ResponseSignals.FILE_UPLOAD_FAILED})
    
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)

    asset = Asset(
        project_id=project.id,
        name=file_id,
        size=file_path.stat().st_size,
        type=AssetTypeEnums.FILE
    )

    asset_record = await asset_model.insert_one(asset=asset)

    return JSONResponse(status_code=status.HTTP_201_CREATED, 
                        content={"signal": ResponseSignals.FILE_UPLOAD_SUCCESS,
                                 "asset_id": str(asset_record.id)})

@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_data: ProcessData):
    process_controller = ProcessController(project_id=project_id)

    chunk_model   = await ChunkModel.create_instance(db_client=request.app.db_client)
    asset_model   = await AssetModel.create_instance(db_client=request.app.db_client)
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project       = await project_model.get_or_create_one(project_id=project_id)

    if process_data.do_reset == 1:
        _ = await chunk_model.delete_many_by_project_id(project_id=project.id)

    if process_data.file_id:
        asset = await asset_model.get_by_name(name=process_data.file_id)
        if asset is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"signal": ResponseSignals.FILE_NOT_FOUND})
        
        all_files = {asset.name: asset.id}
    else:
        all_assets   = await asset_model.get_many(project_id=project.id, type=AssetTypeEnums.FILE)

        all_files = {asset.name: asset.id for asset in all_assets}

        if len(all_files) == 0:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"signal": ResponseSignals.FILE_NOT_FOUND})


    n_records = 0
    n_files   = 0
    for file_id, asset_id in all_files.items():
        file_content = process_controller.get_file_content(file_id=file_id)
        if file_content is None:
            logger.error(f"File content is None for file_id: {file_id}")
            continue

        chunks       = process_controller.process_file_content(file_content=file_content,
                                                               chunk_size=process_data.chunk_size,
                                                               overlap_size=process_data.overlap_size)

        # if not chunks or len(chunks) == 0:
        #     return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
        #                         content={"signal": ResponseSignals.PROCESS_FAILED})

        project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
        project       = await project_model.get_or_create_one(project_id=project_id)

        new_chunks = [
            Chunk(
                text=chunk.page_content,
                metadata=chunk.metadata,
                order=i+1,
                project_id=project.id,
                asset_id=asset_id
            ) 
            for i, chunk in enumerate(chunks)]

        n_records   += await chunk_model.insert_many(chunks=new_chunks)
        n_files     += 1


    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"signal": ResponseSignals.PROCESS_SUCCESS,
                                 "n_processed_records": n_records,
                                 "total_files": len(all_files),
                                 "n_processed_files": n_files})