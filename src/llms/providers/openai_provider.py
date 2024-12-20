from .llm_provider_interface import LLMProviderInterface
from openai import OpenAI
import logging
from .llm_enums import OpenAIEnums

class OpenAIProvider(LLMProviderInterface):
    def __init__(self, 
                 api_key: str,
                 api_url: str=None,
                 max_input_tokens: int=1000,
                 max_output_tokens: int=1000,
                 temperature: float=0.1):
        self.api_key           = api_key
        self.api_url           = api_url
        self.max_input_tokens  = max_input_tokens
        self.max_output_tokens = max_output_tokens
        self.temperature       = temperature

        self.generation_model_id = None
        self.embedding_model_id  = None
        self.embedding_size      = None

        self.roles = OpenAIEnums

        self.client = OpenAI(api_key=api_key, base_url=api_url)
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embed_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embed_size

    def process_text(self, text: str):
        return text[:self.max_input_tokens].strip()

    def generate_text(self, 
                      prompt: str,
                      chat_history: list=[],
                      max_tokens: int=None, 
                      temperature: float=None):
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI was not set")
            return None
        
        max_tokens = max_tokens or self.max_output_tokens
        temperature = temperature or self.temperature

        chat_history.append(self.construct_prompt(prompt, OpenAIEnums.USER.value))

        response = self.client.chat.completions.create(model=self.generation_model_id,
                                                       messages=chat_history,
                                                       max_tokens=max_tokens,
                                                       temperature=temperature)
        
        if not response or not response.choices or not response.choices[0].message:
            self.logger.error("Error while generating text with OpenAI")
            return None
        return response.choices[0].message

        
    def embed_text(self, text: str, doc_type: str=None):
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI was not set")
            return None
        
        response = self.client.embeddings.create(model=self.embedding_model_id,
                                                 input=text)

        if not response or not response.data or not response.data[0].embedding:
            self.logger.error("Error while embedding text with OpenAI")
            return None
        
        return response.data[0].embedding

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": prompt
        }