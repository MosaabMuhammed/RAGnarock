from enum import Enum

class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)

class VectorDBEnums(StrEnum):
    QDRANT = "QDRANT"

class DistanceMethodEnums(StrEnum):
    COSINE    = "cosine"
    DOT       = "dot"
    EUCLIDEAN = "euclidean"
