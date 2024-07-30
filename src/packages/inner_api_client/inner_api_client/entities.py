from pydantic import BaseModel


class PostCreate(BaseModel):
    text: str
    author: str
    image_url: str
    image_with_text: str
    keyword_ru: str | None = None
    keyword_en: str | None = None
    is_published: bool = False


class PostUpdate(BaseModel):
    text: str | None = None
    author: str | None = None
    image_url: str | None = None
    image_with_text: str | None = None
    keyword_ru: str | None = None
    keyword_en: str | None = None
    is_published: bool | None = None


class Post(PostCreate):
    id: int


class QuizCreate(BaseModel):
    text: str
    author: str


class Quiz(QuizCreate):
    id: int
    is_published: bool
    answers: list[str] | None = None


class QuizUpdate(BaseModel):
    text: str | None = None
    author: str | None = None
    is_published: bool | None = None


class ImageModel(BaseModel):
    image_url: str


class PostMultipleImageCreate(BaseModel):
    text: str
    author: str
    image_urls: list[ImageModel]
    is_published: bool = False


class PostMultipleImageUpdate(BaseModel):
    text: str | None = None
    author: str | None = None
    image_urls: list[ImageModel] | None = None
    is_published: bool | None = None


class PostMultipleImage(PostMultipleImageCreate):
    id: int
