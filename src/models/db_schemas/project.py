from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId

class Project(BaseModel):
    project_id: str   = Field(..., min_length=1)
    id: Optional[ObjectId] = Field(None, alias="_id")

    @validator("project_id")
    def validate_project_id(cls, v):
        if not v.isalnum():
            raise ValueError("Project ID must be alphanumeric.")
        return v
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
