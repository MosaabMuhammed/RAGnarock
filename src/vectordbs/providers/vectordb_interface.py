from abc import abstractmethod, ABC
from typing import List, Dict, Any
from models.db_schemas import RetrievedDoc

class VectorDBInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def list_all_collections(self) -> List:
        pass

    @abstractmethod
    def get_collection(self, collection_name: str) -> Dict:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass

    @abstractmethod
    def create_collection(self, 
                          collection_name: str,
                          embedding_size: int,
                          do_reset: bool=False):
        pass

    @abstractmethod
    def insert_one(self, 
               collection_name: str,
               text: str,
               vector: list,
               metadata: Dict=None,
               record_id: str=None):
        pass

    @abstractmethod
    def insert_many(self, 
                    collection_name: str,
                    texts: List[Dict[str, Any]],
                    vectors: List,
                    metadata: List[Dict]=None,
                    record_ids: List[str]=None,
                    batch_size: int=50):
        pass

    @abstractmethod
    def search_by_vector(self, 
                         collection_name: str,
                         vector: list,
                         top_k: int=1) -> List[RetrievedDoc]:
        pass