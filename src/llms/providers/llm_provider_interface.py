from abc import ABC, abstractmethod

class LLMProviderInterface(ABC):
    @abstractmethod
    def set_generation_model(self, model_id: str):
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embed_size: int):
        pass

    @abstractmethod
    def generate_text(self, text: str, chat_history: list=[], max_tokens: int=None, temperature: float=None):
        pass

    @abstractmethod
    def embed_text(self, text: str, doc_type: str):
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass