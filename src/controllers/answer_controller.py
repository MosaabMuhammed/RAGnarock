from .base_controller import BaseController
from .project_controller import ProjectController
from .index_controller import IndexController
from models.db_schemas import Project
from llms.prompts import PromptParser

class AnswerController(BaseController):
    def __init__(self, index_controller: IndexController, prompt_parser: PromptParser):
        self.index_controller = index_controller
        self.prompt_parser    = prompt_parser
        self.generation_client = index_controller.generation_client

    def answer_query(self, project: Project, query: str, top_k: int=10):
        retrieved_docs = self.index_controller.search_index(project, query, top_k)

        if not retrieved_docs:
            return None, None, None
        
        system_prompt = self.prompt_parser.get("QnA", "system_prompt")

        document_prompts = "\n\n".join([
            self.prompt_parser.get("QnA", "doc_prompt", {"doc_no": idx+1,
                                                         "doc_text": self.generation_client.process_text(doc['text'])}) 
            for idx, doc in enumerate(retrieved_docs)
        ])

        footer_prompt = self.prompt_parser.get("QnA", "footer_prompt", {"query": query})

        chat_history = [self.generation_client.construct_prompt(system_prompt, 
                                                                self.generation_client.roles.SYSTEM.value)]
        
        prompt = "\n\n".join([document_prompts, footer_prompt])

        response = self.index_controller.generation_client.generate_text(prompt=prompt,
                                                                         chat_history=chat_history)
                
        return response.content, prompt, chat_history