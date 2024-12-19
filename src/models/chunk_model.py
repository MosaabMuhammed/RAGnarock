from .db_model import DatabaseModel
from .enums import DBEnums
from .db_schemas import Chunk
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(DatabaseModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DBEnums.CHUNKS_COLLECTION_NAME]

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DBEnums.CHUNKS_COLLECTION_NAME not in all_collections:
            self.collection = self.db_client[DBEnums.CHUNKS_COLLECTION_NAME]
            indices = Chunk.get_indexes()
            for index in indices:
                await self.collection.create_index(**index)

    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def insert_one(self, chunk: Chunk):
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        chunk.id = result.inserted_id
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
    
    async def get_many(self, project_id: ObjectId, page_index: int=1, page_size: int=10):
        records = await self.collection.find({"project_id": project_id}).skip((page_index - 1) * page_size).limit(page_size).to_list(length=None)

        return [Chunk(**record) for record in records]
    
    async def delete_many_by_project_id(self, project_id: str):
        result = await self.collection.delete_many({"project_id": project_id})
        return result.deleted_count