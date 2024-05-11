from datetime import timedelta

from config.database import minio_client
from pydantic import BaseModel, field_validator


class PostSchemaCreate(BaseModel):
    text: str
    author: str
    image_url: str
    keyword_ru: str | None = None
    keyword_en: str | None = None
    image_with_text: str | None = None


class PostSchemaRead(PostSchemaCreate):
    id: int
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


class PostSchemaUpdate(PostSchemaCreate):
    text: str | None = None
    author: str | None = None
    image_url: str | None = None
    keyword_ru: str | None = None
    keyword_en: str | None = None
    image_with_text: str | None = None
    is_published: bool | None = None


class PostQueryParams(BaseModel):
    is_published: bool | None = None
