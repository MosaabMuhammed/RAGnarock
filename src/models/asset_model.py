from .db_model import DatabaseModel
from .enums import DBEnums
from .db_schemas import Asset
from bson.objectid import ObjectId
from pymongo import InsertOne
from sqlalchemy.future import select
from sqlalchemy import func, delete

class AssetModel(DatabaseModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        return instance

    async def insert_one(self, asset: Asset):
        async with self.db_client() as session:
            async with session.begin():
                session.add(asset)
            await session.commit()
            await session.refresh(asset)
        return asset
    
    async def insert_many(self, assets: list, batch_size: int=100):
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(assets), batch_size):
                    batch = assets[i:i + batch_size]
                    session.add_all(batch)
                await session.commit()
        return len(assets)
    
    async def get_one(self, asset_id: str):
        async with self.db_client() as session:
            result = await session.execute(select(Asset).where(Asset.id == asset_id))
            asset = result.scalar_one_or_none()
        return asset
    
    async def get_by_name(self, name: str):
        async with self.db_client() as session:
            result = await session.execute(select(Asset).where(Asset.name == name))
            asset = result.scalar_one_or_none()
        return asset
    
    async def get_many(self, project_id: int, type: str=None):
        async with self.db_client() as session:
            async with session.begin():
                query = select(Asset).where(Asset.project_id == project_id)
                if type is not None:
                    query = query.where(Asset.type == type)
                results = await session.execute(query)
                return results.scalars().all()
    
    async def delete_many_by_project_id(self, project_id: int):
        async with self.db_client() as session:
            async with session.begin():
                result = await session.execute(delete(Asset).where(Asset.project_id == project_id))
                await session.commit()
        return result.rowcount