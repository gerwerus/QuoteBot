from enum import Enum
from pydantic import BaseModel, Field


class LangChoices(Enum):
    RUSSIAN = "ru"
    ENGLISH = "en"


class QuoteModel(BaseModel):
    text: str = Field(alias="quoteText")
    author: str | None = Field(alias="quoteAuthor", default=None)
