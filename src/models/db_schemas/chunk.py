from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId

class Chunk(BaseModel):
    id: Optional[ObjectId]  = Field(None, alias="_id")
    text: str               = Field(..., min_length=1)
    order: int              = Field(..., gt=0)
    project_id: ObjectId
    asset_id: ObjectId
    metadata: dict

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "keys": [("project_id", 1), ("order", 1)],
                "name": "project_id_order_index_1",
                "unique": False
            }
        ]