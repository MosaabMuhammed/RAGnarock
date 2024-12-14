from .base_controller import BaseController
from .project_controller import ProjectController
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from models.enums import FileEnums
from langchain.text_splitter import RecursiveCharacterTextSplitter


class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def __get_file_loader(self, file_id: Path): 
        file_extension = Path(file_id).suffix
        file_path      = self.project_path / file_id

        if not file_path.is_file():
            return None

        if file_extension == FileEnums.TXT:
            return TextLoader(file_path=file_path, encoding="utf-8")
        
        elif file_extension == FileEnums.PDF:
            return PyMuPDFLoader(file_path=file_path)

        #TODO: Raise an error here.
        return None
    
    def get_file_content(self, file_id: Path):
        loader = self.__get_file_loader(file_id=file_id)
        if loader is None: return None
        return loader.load()
    
    def process_file_content(self, 
                             file_content: list,
                             chunk_size: int=100,
                             overlap_size: int=20):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                       chunk_overlap=overlap_size,
                                                       length_function=len)
        file_content_texts    = [rec.page_content for rec in file_content]
        file_content_metadata = [rec.metadata for rec in file_content]

        chunks = text_splitter.create_documents(texts=file_content_texts,
                                                metadatas=file_content_metadata)
        return chunks