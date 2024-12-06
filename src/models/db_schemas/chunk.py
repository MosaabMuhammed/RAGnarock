from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId

class Chunk(BaseModel):
    _id: Optional[ObjectId] = Field(alias="_id")
    project_id: ObjectId    = Field(..., alias="project_id")
    text: str               = Field(..., alias="text", min_length=1)
    metadata: dict          = Field(..., alias="metadata")
    order: int              = Field(..., alias="order", gt=0)

    class Config:
        arbitrary_types_allowed = True