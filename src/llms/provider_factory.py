from .providers import OpenAIProvider, CohereProvider, LLMEnums

class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config

    def create(self, provider_name: str):
        if provider_name == LLMEnums.OPENAI:
            return OpenAIProvider(api_key=self.config.OPENAI_API_KEY,
                                  api_url=self.config.OPENAI_API_URL,
                                  max_input_tokens=self.config.MAX_INPUT_TOKENS,
                                  max_output_tokens=self.config.MAX_OUTPUT_TOKENS,
                                  temperature=self.config.TEMPERATURE)
        elif provider_name == LLMEnums.COHERE:
            return CohereProvider(api_key=self.config.COHERE_API_KEY,
                                  max_input_tokens=self.config.MAX_INPUT_TOKENS,
                                  max_output_tokens=self.config.MAX_OUTPUT_TOKENS,
                                  temperature=self.config.TEMPERATURE)
        return None