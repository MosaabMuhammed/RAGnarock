from config.settings import get_settings
from pathlib import Path

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = Path(__file__).parent.parent
        self.files_dir = self.base_dir / "assets" / "files"
        self.database_dir = self.base_dir / "assets" / "database"

    def get_database_path(self, db_name: str):
        database_path = self.database_dir / db_name
        database_path.mkdir(parents=True, exist_ok=True)
        return database_path