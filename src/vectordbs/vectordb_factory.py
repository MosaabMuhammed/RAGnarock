from providers import QdarntDBProvider, VectorDBEnums
from controllers.base_controller import BaseController

class VectorDBFactory:
    def __init__(self, config):
        self.config = config
        self.base_controller = BaseController()

    def create(self, provider=None):
        if provider == VectorDBEnums.QDRANT:
            db_path = self.base_controller.get_database_path(self.config.VECTORDB_PATH)
            return QdarntDBProvider(db_path=db_path,
                                    distance_method=self.config.VECTORDB_DISTANCE_METHOD)
        else:
            raise ValueError(f"Unknown provider: {provider}")