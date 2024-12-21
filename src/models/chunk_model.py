from .db_model import DatabaseModel
from .enums import DBEnums
from .db_schemas import Chunk
from bson.objectid import ObjectId
from pymongo import InsertOne
from sqlalchemy.future import select
from sqlalchemy import func, delete

class ChunkModel(DatabaseModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        return instance

    async def insert_one(self, chunk: Chunk):
        async with self.db_client() as session:
            async with session.begin():
                session.add(chunk)
            await session.commit()
            await session.refresh(chunk)
        return chunk
    
    async def insert_many(self, chunks: list, batch_size: int=100):
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i + batch_size]
                    session.add_all(batch)
                await session.commit()
        return len(chunks)
    
    async def get_one(self, chunk_id: str):
        async with self.db_client() as session:
            result = await session.execute(select(Chunk).where(Chunk.id == chunk_id))
            chunk = result.scalar_one_or_none()
        return chunk
    
    async def get_many(self, project_id: ObjectId, page_index: int=1, page_size: int=10):
        async with self.db_client() as session:
            async with session.begin():
                total_docs = await session.execute(select(func.count(Chunk.id)).where(Chunk.project_id == project_id))
                total_docs = total_docs.scalar_one()
                total_pages = total_docs // page_size
                if total_docs % page_size > 0:
                    total_pages += 1
                query = await session.execute(select(Chunk).where(Chunk.project_id == project_id).offset((page_index - 1) * page_size).limit(page_size))
                results = query.scalars().all()
                return results
    
    async def delete_many_by_project_id(self, project_id: int):
        async with self.db_client() as session:
            async with session.begin():
                result = await session.execute(delete(Chunk).where(Chunk.project_id == project_id))
                await session.commit()
        return result.rowcount