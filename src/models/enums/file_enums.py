from enum import Enum

class FileEnums(str, Enum):
    TXT = ".txt"
    PDF = ".pdf"

    def __str__(self) -> str:
        return str.__str__(self)