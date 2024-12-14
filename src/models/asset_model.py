from .db_model import DatabaseModel
from .enums import DBEnums
from .db_schemas import Asset
from bson.objectid import ObjectId
from pymongo import InsertOne

class AssetModel(DatabaseModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DBEnums.ASSET_COLLECTION_NAME]

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DBEnums.ASSET_COLLECTION_NAME not in all_collections:
            self.collection = self.db_client[DBEnums.ASSET_COLLECTION_NAME]
            indices = Asset.get_indexes()
            for index in indices:
                await self.collection.create_index(**index)

    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def insert_one(self, asset: Asset):
        result = await self.collection.insert_one(asset.to_dict_with_timestamp())
        asset.id = result.inserted_id
        return asset
    
    async def insert_many(self, assets: list, batch_size: int=100):
        for i in range(0, len(assets), batch_size):
            batch = assets[i:i + batch_size]
            operations = [InsertOne(asset.to_dict_with_timestamp()) for asset in batch]
        await self.collection.bulk_write(operations)
        return len(assets)
    
    async def get_one(self, asset_id: str):
        asset = await self.collection.find_one({"_id": ObjectId(asset_id)})
        if asset is None:
            return None
        return Asset(**asset)
    
    async def get_by_name(self, name: str):
        asset = await self.collection.find_one({"name": name})
        if asset is None:
            return None
        return Asset(**asset)
    
    async def get_many(self, project_id: str, type: str=None):
        records = await self.collection.find({"project_id": project_id, "type": type}).to_list(length=None)

        return [Asset(**record) for record in records]
    
    async def delete_many_by_project_id(self, project_id: str):
        result = await self.collection.delete_many({"project_id": project_id})
        return result.deleted_count