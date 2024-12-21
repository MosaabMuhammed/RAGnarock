from .base_controller import BaseController
from fastapi import UploadFile
from models import ResponseSignals
from pathlib import Path

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id):
        project_dir = Path(self.files_dir) / str(project_id)
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir
