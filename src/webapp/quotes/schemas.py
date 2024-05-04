from datetime import timedelta

from sqlalchemy import inspect

from config.database import minio_client
from config.settings import settings
from pydantic import BaseModel, HttpUrl, field_validator

from .models import Post


class PostSchemaCreate(BaseModel):
    text: str
    author: str
    image_url: str
    keyword_ru: str | None = None
    keyword_en: str | None = None
    image_with_text: str | None = None


class PostSchemaRead(PostSchemaCreate):
    id: int
    image_with_text: HttpUrl | None = None
    is_published: bool

    @field_validator("image_with_text", mode="before")
    def generate_url_from_filefield(cls, value) -> str | None:
        if value["object_name"]:
            return minio_client.cli.get_presigned_url(
                "GET",
                bucket_name=value["bucket_name"],
                object_name=value["object_name"],
                expires=timedelta(hours=1),
            )
        return None
