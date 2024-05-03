from enum import StrEnum

from pydantic import BaseModel, Field


class ConversationIdList(StrEnum):
    quotes_conversation_id = "078f8eda-2f53-4e0a-a91c-91b18a53c8b6"


class AppIdList(StrEnum):
    GPT_4 = "5382c082-f063-42ae-9086-f85df937aa8b"


class AppModel(BaseModel):
    id: str
    name: str
    status: str
    template: str
    params: dict
    meta: dict
    description: str | None = None
    created_at: int = Field(alias="createdAt")
    updated_at: int = Field(alias="updatedAt")


class ConversationHistoryContent(BaseModel):
    type: str
    text: str
    localization_key: str | None = Field(default=None, alias="localizationKey")


class ConversationHistory(BaseModel):
    id: str
    conversation_id: str = Field(alias="conversationId")
    status: str
    type: str
    content: list[ConversationHistoryContent]


class Conversation(BaseModel):
    id: str
    name: str
    app: AppModel
    status: str
    created_at: int = Field(alias="createdAt")
    updated_at: int = Field(alias="updatedAt")
    meta: dict
    history: list[ConversationHistory]
