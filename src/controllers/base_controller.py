from config.settings import get_settings
from pathlib import Path

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = Path(__file__).parent.parent
        self.files_dir = self.base_dir / "assets" / "files"