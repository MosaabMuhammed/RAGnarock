from .base_controller import BaseController
from fastapi import UploadFile
from models.enums import ResponseSignals

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.bit_scale_size = 1_048_576  # Convert MB to bytes

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_SUPPORTED_TYPES:
            return False, ResponseSignals.FILE_TYPE_NOT_SUPPORTED
        
        if file.size > self.app_settings.FILE_MAX_SIZE_MB * self.bit_scale_size:
            return False, ResponseSignals.FILE_SIZE_EXCEEDED
        
        return True, ResponseSignals.FILE_VALIDATED_SUCCESS