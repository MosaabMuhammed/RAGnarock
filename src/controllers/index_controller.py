from .base_controller import BaseController
from models.db_schemas import Project, Chunk
from llms.providers import DocumentTypeEnums
from typing import List
import json

class IndexController(BaseController):
    def __init__(self, vectordb_client, generation_client, embedding_client):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client

    def create_collection_name(self, project_id: str) -> str:
        return f"collection_{project_id}".strip()
    
    def reset_vectordb_collection(self, project: Project):
        collection_name = self.create_collection_name(project.project_id)
        return self.vectordb_client.delete_collection(collection_name)
    
    def get_vectordb_collection(self, project: Project):
        collection_name = self.create_collection_name(project.project_id)
        collection_info = self.vectordb_client.get_collection(collection_name)

        return json.loads(json.dumps(collection_info, default=lambda x: x.__dict__))
    
    def index_into_vectordb(self, project: Project, ids: List[int], chunks: List[Chunk], do_reset: bool=False):
        collection_name = self.create_collection_name(project.project_id)

        texts    = [c.text for c in chunks]
        metadata = [c.metadata for c in chunks]
        vectors  = [self.embedding_client.embed_text(text, doc_type=DocumentTypeEnums.DOCUMENT) for text in texts]

        _ = self.vectordb_client.create_collection(collection_name=collection_name,
                                                   embedding_size=self.embedding_client.embedding_size,
                                                   do_reset=do_reset)
        
        _ = self.vectordb_client.insert_many(collection_name=collection_name,
                                             record_ids=ids,
                                             texts=texts,
                                             metadata=metadata,
                                             vectors=vectors)
        
        return True
        
    def search_index(self, project: Project, query: str, top_k: int=10):
        collection_name = self.create_collection_name(project.project_id)
        vector = self.embedding_client.embed_text(query, doc_type=DocumentTypeEnums.QUERY)

        if not vector:
            return False
        
        search_results = self.vectordb_client.search_by_vector(collection_name=collection_name,
                                                               vector=vector,
                                                               top_k=top_k)
        
        if not search_results:
            return False

        return json.loads(json.dumps(search_results, default=lambda x: x.__dict__))
