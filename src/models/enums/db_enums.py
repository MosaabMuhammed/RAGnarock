from enum import Enum

class DBEnums(str, Enum):
    PROJECTS_COLLECTION_NAME = "projects"
    CHUNKS_COLLECTION_NAME   = "chunks"
    ASSET_COLLECTION_NAME    = "assets"

    def __str__(self) -> str:
        return str.__str__(self)