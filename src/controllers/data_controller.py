from .base_controller import BaseController
from .project_controller import ProjectController
from fastapi import UploadFile
from models.enums import ResponseSignals
import uuid, re

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
    
    def generate_unique_filepath(self, orig_file_name: str, project_id: str):
        project_path     = ProjectController().get_project_path(project_id=project_id)
        cleaned_filename = self.get_clean_file_name(orig_file_name=orig_file_name)

        return project_path / f"{uuid.uuid4().hex}_{cleaned_filename}"
    
    def get_clean_file_name(self, orig_file_name: str):
        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name