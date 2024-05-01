from pydantic import BaseModel, HttpUrl


class PostSchemaCreate(BaseModel):    
    text: str
    author: str
    image_url: HttpUrl
    keyword_ru: str
    keyword_en: str
    image_with_text_url: str | None = None

class PostSchemaRead(PostSchemaCreate):
    id: int
    # is_published: bool
