import logging
from typing import List, Dict, Any

from qdrant_client import models, QdrantClient

from .vectordb_interface import VectorDBInterface
from .vectordb_enums import DistanceMethodEnums
from models.db_schemas import RetrievedDoc

class QdarntDBProvider(VectorDBInterface):
    def __init__(self, db_path: str, distance_method: DistanceMethodEnums):
        self.client = None
        self.db_path = db_path

        if distance_method == DistanceMethodEnums.COSINE:
            self.distance_method = "Cosine"
        elif distance_method == DistanceMethodEnums.DOT:
            self.distance_method = "Dot"
        elif distance_method == DistanceMethodEnums.EUCLIDEAN:
            self.distance_method = "Euclid"

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name)
    
    def list_all_collections(self) -> List:
        return self.client.get_collections()
    
    def get_collection(self, collection_name: str) -> Dict:
        return self.client.get_collection(collection_name)
    
    def delete_collection(self, collection_name: str):
        if self.is_collection_exists(collection_name=collection_name):
            return self.client.delete_collection(collection_name)
        return False
        
    def create_collection(self, collection_name, embedding_size, do_reset = False):
        if do_reset:
            _ = self.delete_collection(collection_name)

        if not self.is_collection_exists(collection_name):
            self.client.create_collection(collection_name,
                                          vectors_config=models.VectorParams(
                                              size=embedding_size,
                                              distance=self.distance_method
                                          ))
            return True
        return False
    
    def insert_one(self, 
                   collection_name: str,
                   text: str,
                   vector: list,
                   metadata: Dict=None,
                   record_id: str=None):
        if not self.is_collection_exists(collection_name):
            self.logger.error(f"Collection {collection_name} does not exist")
            return False
        
        try:
            _ = self.client.upload_records(collection_name=collection_name,
                                        records=[models.Record(
                                            id=[record_id],
                                            vector=vector,
                                            payload={"text": text, "metadata": metadata}
                                        )])
        except Exception as e:
            self.logger.error(f"Error uploading record: {e}")
            return False
        return True


    def insert_many(self, 
                    collection_name: str,
                    texts: List[Dict[str, Any]],
                    vectors: List,
                    metadata: List[Dict]=None,
                    record_ids: List[str]=None,
                    batch_size: int=50):
        if metadata is None:
            metadata = [None] * len(texts)
        
        if record_ids is None:
            record_ids = list(range(0, len(texts)))

        for i in range(0, len(texts), batch_size):
            batch_texts      = texts[i:i+batch_size]
            batch_vectors    = vectors[i:i+batch_size] 
            batch_metadata   = metadata[i:i+batch_size]
            batch_record_ids = record_ids[i:i+batch_size]

            records = []
            for text, vector, meta, record_id in zip(batch_texts, batch_vectors, batch_metadata, batch_record_ids):
                records.append(models.Record(
                    vector=vector,
                    payload={"text": text, "metadata": meta},
                    id=record_id
                ))
            
            try:
                _ = self.client.upload_records(collection_name=collection_name,
                                               records=records)
            except Exception as e:
                self.logger.error(f"Error uploading records: {e}")
                return False
        return True

    def search_by_vector(self, 
                         collection_name: str,
                         vector: list,
                         top_k: int=1) -> List[Dict]:
        results = self.client.search(collection_name=collection_name,
                                     query_vector=vector,
                                     limit=top_k)
        
        if not results:
            return None
        
        return [RetrievedDoc(text=doc.payload["text"], score=doc.score) for doc in results]
