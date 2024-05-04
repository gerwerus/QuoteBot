from datetime import timedelta

from config.database import minio_client
from config.settings import settings
from pydantic import BaseModel, HttpUrl, field_validator


class ImageData(BaseModel):
    data: str | bytes
    filename: str | None = None


class PostSchemaCreate(BaseModel):
    text: str
    author: str
    image_url: str
    keyword_ru: str | None = None
    keyword_en: str | None = None
    image_with_text_url: ImageData | None = None


class PostSchemaRead(PostSchemaCreate):
    id: int
    image_with_text_url: HttpUrl | None = None
    is_published: bool

    @field_validator("image_with_text_url", mode="before")
    def generate_url_from_filefield(cls, value) -> str | None:
        if value:
            return minio_client.get_presigned_url(
                "GET",
                bucket_name=settings.MINIO_STORAGE_BUCKET,
                object_name=value["file_id"],
                expires=timedelta(hours=1),
            )
        return None
