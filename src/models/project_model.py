from .db_model import DatabaseModel
from .enums import DBEnums
from .db_schemas import Project

class ProjectModel(DatabaseModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DBEnums.PROJECTS_COLLECTION_NAME]

    async def insert_one(self, project: Project):
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project._id = result.inserted_id
        return project
    
    async def get_or_create_one(self, project_id: str):
        project = await self.collection.find_one({"project_id": project_id})
        if project is None:
            project = Project(project_id=project_id)
            return await self.insert_one(project)
        return Project(**project)
    
    async def get_many(self, page_index: int=1, page_size: int=10):
        total_projects = await self.collection.count_documents({})
        total_pages = total_projects // page_size
        if total_projects % page_size > 0:
            total_pages += 1

        projects = self.collection.find().skip((page_index - 1) * page_size).limit(page_size)
        return [Project(**project) async for project in projects], total_pages