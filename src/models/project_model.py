from .db_model import DatabaseModel
from .enums import DBEnums
from .db_schemas import Project
from sqlalchemy.future import select
from sqlalchemy import func


class ProjectModel(DatabaseModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        return instance

    async def insert_one(self, project: Project):
        async with self.db_client() as session:
            async with session.begin():
                session.add(project)
            await session.commit()
            await session.refresh(project)
        return project
    
    async def get_or_create_one(self, project_id: int):
        async with self.db_client() as session:
            async with session.begin():
                query = await session.execute(select(Project).where(Project.id == project_id))
                project = query.scalar_one_or_none()
                if project is None:
                    project = await self.insert_one(Project(id=project_id))
                return project
    
    async def get_many(self, page_index: int=1, page_size: int=10):
        async with self.db_client() as session:
            async with session.begin():
                total_docs = await session.execute(select(func.count(Project.id))).scalar_one()
                total_pages = total_docs // page_size
                if total_docs % page_size > 0:
                    total_pages += 1
                query = select(Project).offset((page_index - 1) * page_size).limit(page_size)
                results = await session.execute(query).scalars().all()
                return results, total_pages
