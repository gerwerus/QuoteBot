from pydantic import BaseModel


class PostSchemaCrete(BaseModel):    
    text: str
    author: str
    image_url: str
    image_with_text_url: str | None
    keyword_ru: str
    keyword_en: str
    is_published: bool

class PostSchemaRead(BaseModel):
    id: int
