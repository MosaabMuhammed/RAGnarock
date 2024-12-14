from enum import Enum

class AssetTypeEnums(str, Enum):
    FILE = "file"

    def __str__(self) -> str:
        return str.__str__(self)