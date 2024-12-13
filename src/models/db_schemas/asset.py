from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: ObjectId
    type: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    size: int = Field(default=None, ge=0, description="Size of the asset in bytes.")
    config: dict = Field(default=None, description="Configuration settings for the asset.")
    saved_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of when the asset was saved.")

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "keys": [("project_id", 1)],
                "name": "asset_project_id_index_1",
                "unique": False
            },
            {
                "keys": [("project_id", 1), ("name", 1)],
                "name": "project_id_asset_name_index_1",
                "unique": True
            }
        ]

    def to_dict_with_timestamp(self):
        asset_dict = self.dict(by_alias=True, exclude_unset=True)
        asset_dict['saved_at'] = self.saved_at
        return asset_dict