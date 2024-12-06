from enum import Enum

class ResponseSignals(str, Enum):
    FILE_VALIDATED_SUCCESS  = "file_validated_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED      = "file_size_exceeded"
    FILE_UPLOAD_FAILED      = "file_upload_failed"
    FILE_UPLOAD_SUCCESS     = "file_uploaded_successfully"

    PROCESS_SUCCESS = "file_process_success"
    PROCESS_FAILED  = "file process_failed"

    def __str__(self) -> str:
        return str.__str__(self)