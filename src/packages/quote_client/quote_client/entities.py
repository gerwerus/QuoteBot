from enum import Enum

from pydantic import BaseModel, Field, field_validator


class LangChoices(Enum):
    RUSSIAN = "ru"
    ENGLISH = "en"


class QuoteModel(BaseModel):
    text: str = Field(alias="quoteText")
    author: str | None = Field(alias="quoteAuthor", default=None)

    @field_validator("text", "author")
    @classmethod
    def strip_string(cls, v: str | None) -> str | None:
        if v:
            return v.strip()
        return None
