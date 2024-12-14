from enum import Enum

class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)

class LLMEnums(StrEnum):
    OPENAI = "openai"
    COHERE = "cohere"

class OpenAIEnums(StrEnum):
    SYSTEM    = "system"
    USER      = "user"
    ASSISTANT = "assistant"

class CohereEnums(StrEnum):
    SYSTEM    = "system"
    USER      = "user"
    ASSISTANT = "assistant"

    DOCUMENT = "document_type"
    QUERY    = "query_type"

class DocumentTypeEnums(StrEnum):
    DOCUMENT = "document"
    QUERY    = "query"