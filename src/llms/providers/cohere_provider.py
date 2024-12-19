from .provider_interface import ProviderInterface
from .llm_enums import CohereEnums, DocumentTypeEnums
import cohere
import logging

class CohereProvider(ProviderInterface):
    def __init__(self,
                 api_key: str,
                 max_input_tokens: int=1000,
                 max_output_tokens: int=1000,
                 temperature: float=0.1):
        self.api_key           = api_key
        self.max_input_tokens  = max_input_tokens
        self.max_output_tokens = max_output_tokens
        self.temperature       = temperature

        self.generation_model_id = None
        self.embedding_model_id  = None
        self.embedding_size      = None

        self.client = cohere.ClientV2(api_key=api_key)
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embed_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embed_size

    def process_text(self, text: str):
        return text[:self.max_input_tokens].strip()
    
    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }

    def generate_text(self, 
                      prompt: str,
                      chat_history: list=[],
                      max_tokens: int=None, 
                      temperature: float=None):
        if not self.client:
            self.logger.error("Cohere client was not set")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for Cohere was not set")
            return None
        
        max_tokens = max_tokens or self.max_output_tokens
        temperature = temperature or self.temperature

        chat_history.append(self.construct_prompt(prompt, CohereEnums.USER))

        response = self.client.chat(model=self.generation_model_id,
                                    messages=chat_history,
                                    max_tokens=max_tokens,
                                    temperature=temperature)
        
        if not response or not response.message or not response.message.content:
            self.logger.error("Error while generating text with Cohere")
            return None
        return response.message.content[0].text
    
    def embed_text(self, text: str, doc_type: str=None):
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI was not set")
            return None
        
        input_type = CohereEnums.DOCUMENT
        if doc_type == DocumentTypeEnums.QUERY:
            input_type = CohereEnums.QUERY

        response = self.client.embed(model=self.embedding_model_id,
                                     texts=[self.process_text(text)],
                                     input_type=input_type,
                                     embedding_types=['float'])

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error while embedding text with Cohere")
            return None
        
        return response.embeddings.float[0]
