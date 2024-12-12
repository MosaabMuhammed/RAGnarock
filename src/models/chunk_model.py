from .db_model import DatabaseModel
from .enums import DBEnums
from .db_schemas import Chunk
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(DatabaseModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DBEnums.CHUNKS_COLLECTION_NAME]

    async def insert_one(self, chunk: Chunk):
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        chunk._id = result.inserted_id
        return chunk
    
    async def insert_many(self, chunks: list, batch_size: int=100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            operations = [InsertOne(chunk.dict(by_alias=True, exclude_unset=True)) for chunk in batch]
        await self.collection.bulk_write(operations)
        return len(chunks)
    
    async def get_one(self, chunk_id: str):
        chunk = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        if chunk is None:
            return None
        return Chunk(**chunk)
    
    async def get_many(self, project_id: str, page_index: int=1, page_size: int=10):
        records = await self.collection.find({"project_id": project_id}).skip((page_index - 1) * page_size).limit(page_size).tolist(length=None)

        return [Chunk(**record) for record in records]
    
    async def delete_many_by_project_id(self, project_id: str):
        result = await self.collection.delete_many({"project_id": project_id})
        return result.deleted_count