from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId

class Project(BaseModel):
    _id: Optional[ObjectId] = Field(alias="_id")
    project_id: str = Field(..., alias="project_id", min_length=1)

    @validator("project_id")
    def validate_project_id(cls, v):
        if not v.isalnum():
            raise ValueError("Project ID must be alphanumeric.")
        return v
    
    class Config:
        aritrary_types_allowed = True
