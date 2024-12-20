from enum import Enum

class ResponseSignals(str, Enum):
    FILE_VALIDATED_SUCCESS  = "file_validated_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED      = "file_size_exceeded"
    FILE_UPLOAD_FAILED      = "file_upload_failed"
    FILE_UPLOAD_SUCCESS     = "file_uploaded_successfully"
    FILE_NOT_FOUND          = "file_not_found"

    PROCESS_SUCCESS = "file_process_success"
    PROCESS_FAILED  = "file process_failed"

    PROJECT_NOT_FOUND = "project_not_found"
    INDEX_INSERTION_FAILED = "index_insertion_failed"
    INDEX_INSERTION_SUCCESS = "index_insertion_success"
    INDEX_INFO_FETCHED      = "index_info_fetched"
    INDEX_SEARCH_SUCCESS    = "index_search_success"
    INDEX_SEARCH_FAILED     = "index_search_failed"

    ANSWER_GENERATED_SUCCESS = "answer_generated_success"
    ANSWER_GENERATED_FAILED  = "answer_generated_failed"

    def __str__(self) -> str:
        return str.__str__(self)