from pydantic import BaseModel


class WordSchemaCreate(BaseModel):
    word: str
    definition: str


class WordSchemaRead(WordSchemaCreate):
    id: int
    is_published: bool


class WordSchemaUpdate(BaseModel):
    word: str
    definition: str
    is_published: bool | None = None


class WordQueryParams(BaseModel):
    is_published: bool | None = None


class PaginationQueryParams(BaseModel):
    limit: int = 100
    offset: int = 0
