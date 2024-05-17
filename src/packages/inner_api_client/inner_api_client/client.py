from io import BytesIO
from urllib.parse import urljoin

import aiohttp
from minio_client import MinioClient
from pydantic import TypeAdapter

from .entities import Post, PostCreate, PostUpdate
from .settings import InnerApiSettings


class InnerApiClient:
    def __init__(self, settings: InnerApiSettings | None = None, minio_client: MinioClient | None = None) -> None:
        self.settings = settings or InnerApiSettings.initialize_from_environment()
        self.minio_client = minio_client or MinioClient(settings=settings)

        self.quotes_endpoint = urljoin(self.settings.BASE_URL, "quotes/")

    async def get_posts(self, is_published: bool | None = None) -> list[Post]:
        params = {}
        if is_published is not None:
            params["is_published"] = str(is_published)

        async with aiohttp.ClientSession() as session:
            async with session.get(self.quotes_endpoint, params=params) as response:
                data = await response.json()
                return TypeAdapter(list[Post]).validate_python(data)

    async def create_post(self, post: PostCreate, image_data: bytes, bucket_name: str | None) -> Post:
        bucket_name = bucket_name or self.minio_client.settings.MINIO_STORAGE_BUCKET

        with BytesIO(image_data) as image:
            self.minio_client.cli.put_object(
                bucket_name=bucket_name,
                object_name=post.image_with_text,
                data=image,
                length=len(image_data),
            )

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.post(self.quotes_endpoint, json=post.model_dump()) as response:
                data = await response.json()
                return TypeAdapter(Post).validate_python(data)

    async def update_post(self, id: int, post: PostUpdate) -> Post:
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.patch(
                urljoin(self.quotes_endpoint, str(id)), json=post.model_dump(exclude_unset=True),
            ) as response:
                data = await response.json()
                return TypeAdapter(Post).validate_python(data)
    
    @staticmethod
    async def get_image_bytes(url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()
