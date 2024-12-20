from fastapi import FastAPI, APIRouter, status, Request
from fastapi.responses import JSONResponse
from routes.schemas.index import PushRequest, SearchRequest
from controllers import IndexController
from models import ProjectModel, ResponseSignals, ChunkModel
import logging

logger = logging.getLogger("uvicorn.error")

index_router = APIRouter(prefix="/api/v1/index",
                         tags=["index"])

@index_router.post("/index/{project_id}")
async def index_project(request: Request, project_id: str, push_request: PushRequest):
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project       = await project_model.get_or_create_one(project_id=project_id)
    if not project:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"signal": ResponseSignals.PROJECT_NOT_FOUND})
    
    index_controller = IndexController(vectordb_client=request.app.vectordb_client,
                                       generation_client=request.app.generation_client,
                                       embedding_client=request.app.embedding_client)
    
    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

    has_records = True
    page_index  = 1
    inserted_count = 0
    idx = 0
    while has_records:
        chunks = await chunk_model.get_many(project_id=project.id, page_index=page_index, page_size=50)
        if not chunks:
            has_records = False
            break

        chunk_ids = list(range(idx, idx+len(chunks)))
        idx += len(chunks)

        is_inserted = index_controller.index_into_vectordb(project=project, 
                                                           ids=chunk_ids,
                                                           chunks=chunks, 
                                                           do_reset=False)
        if not is_inserted:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content={"signal": ResponseSignals.INDEX_INSERTION_FAILED})
        
        page_index += 1
        inserted_count += len(chunks)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"signal": ResponseSignals.INDEX_INSERTION_SUCCESS})

@index_router.get("/get_index_info/{project_id}")
async def get_index_info(request: Request, project_id: str):
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project       = await project_model.get_or_create_one(project_id=project_id)

    index_controller = IndexController(vectordb_client=request.app.vectordb_client,
                                       embedding_client=request.app.embedding_client,
                                        generation_client=request.app.generation_client)
    
    collection_info = index_controller.get_vectordb_collection(project=project)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"signal": ResponseSignals.INDEX_INFO_FETCHED,
                                 "collection_info": collection_info})

@index_router.post("/search/{project_id}")
async def search_index(request: Request, project_id: str, search_request: SearchRequest):
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project       = await project_model.get_or_create_one(project_id=project_id)

    index_controller = IndexController(vectordb_client=request.app.vectordb_client,
                                        embedding_client=request.app.embedding_client,
                                        generation_client=request.app.generation_client)
    
    results = index_controller.search_index(project=project, query=search_request.query, top_k=search_request.top_k)

    if not results:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"signal": ResponseSignals.INDEX_SEARCH_FAILED})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"signal": ResponseSignals.INDEX_SEARCH_SUCCESS,
                                 "result": results})