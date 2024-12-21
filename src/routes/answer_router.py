from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from routes.schemas.index import SearchRequest
from controllers import IndexController, AnswerController
from models import ProjectModel, ResponseSignals
import logging

logger = logging.getLogger("uvicorn.error")

answer_router = APIRouter(prefix="/api/v1/answer",
                          tags=["answer"])

@answer_router.post("/answer_query/{project_id}")
async def answer_query(request: Request, project_id: int, search_request: SearchRequest):
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project       = await project_model.get_or_create_one(project_id=project_id)

    index_controller = IndexController(vectordb_client=request.app.vectordb_client,
                                        embedding_client=request.app.embedding_client,
                                        generation_client=request.app.generation_client)
    
    answer_controller = AnswerController(index_controller=index_controller,
                                         prompt_parser=request.app.prompt_parser)
    
    response, prompt, chat_history = answer_controller.answer_query(project=project, 
                                                                    query=search_request.query,
                                                                    top_k=search_request.top_k)
    if not response:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"signal": ResponseSignals.ANSWER_GENERATED_FAILED})
     
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"signal": ResponseSignals.ANSWER_GENERATED_SUCCESS,
                                 "response": response,
                                 "prompt": prompt,
                                 "chat_history": chat_history})