from enum import Enum

class ResponseSignals(str, Enum):
    FILE_VALIDATED_SUCCESS  = "File_validated_successfully"
    FILE_TYPE_NOT_SUPPORTED = "File_type_not_supported"
    FILE_SIZE_EXCEEDED      = "File_size_exceeded"
    FILE_UPLOAD_FAILED      = "File_upload_failed"
    FILE_UPLOAD_SUCCESS     = "File_upload_success"

    def __str__(self) -> str:
        return str.__str__(self)