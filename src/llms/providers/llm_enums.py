from enum import Enum

class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)

class LLMEnums(StrEnum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"

class OpenAIEnums(StrEnum):
    SYSTEM    = "system"
    USER      = "user"
    ASSISTANT = "assistant"

class CohereEnums(StrEnum):
    SYSTEM    = "system"
    USER      = "user"
    ASSISTANT = "assistant"

    DOCUMENT = "search_document"
    QUERY    = "search_query"

class DocumentTypeEnums(StrEnum):
    DOCUMENT = "document"
    QUERY    = "query"