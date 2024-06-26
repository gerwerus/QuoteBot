from io import BytesIO
from urllib.parse import urljoin

import aiohttp
from minio_client import MinioClient
from pydantic import TypeAdapter

from .entities import Post, PostCreate, PostUpdate, Quiz, QuizCreate, QuizUpdate
from .settings import InnerApiSettings


class InnerApiClient:
    def __init__(
        self,
        settings: InnerApiSettings | None = None,
        minio_client: MinioClient | None = None,
    ) -> None:
        self.settings = settings or InnerApiSettings.initialize_from_environment()
        self.minio_client = minio_client or MinioClient(settings=settings)

        self.quotes_endpoint = urljoin(self.settings.BASE_URL, "quotes/")
        self.quizes_endpoint = urljoin(self.quotes_endpoint, "quizes/")

    async def get_posts(self, is_published: bool | None = None, limit: int = 1, offset: int = 0) -> list[Post]:
        params = {"limit": limit, "offset": offset}
        if is_published is not None:
            params["is_published"] = str(is_published)

        async with aiohttp.ClientSession() as session, session.get(
            self.quotes_endpoint,
            params=params,
        ) as response:
            data = await response.json()
            return TypeAdapter(list[Post]).validate_python(data)

    async def create_post(
        self,
        post: PostCreate,
        image_data: bytes,
        bucket_name: str | None,
    ) -> Post:
        bucket_name = bucket_name or self.minio_client.settings.MINIO_STORAGE_BUCKET

        with BytesIO(image_data) as image:
            self.minio_client.cli.put_object(
                bucket_name=bucket_name,
                object_name=post.image_with_text,
                data=image,
                length=len(image_data),
            )

        async with aiohttp.ClientSession(
            raise_for_status=True,
        ) as session, session.post(
            self.quotes_endpoint,
            json=post.model_dump(),
        ) as response:
            data = await response.json()
            return TypeAdapter(Post).validate_python(data)

    async def update_post(self, id_: int, post: PostUpdate) -> Post:
        async with aiohttp.ClientSession(  # noqa SIM117
            raise_for_status=True,
        ) as session:
            async with session.patch(  # noqa SIM117
                urljoin(self.quotes_endpoint, str(id_)),
                json=post.model_dump(exclude_unset=True),
            ) as response:
                data = await response.json()
                return TypeAdapter(Post).validate_python(data)
    
    async def get_quizes(self, is_published: bool | None = None, limit: int = 1, offset: int = 0) -> list[Quiz]:
        params = params = {"limit": limit, "offset": offset}
        if is_published is not None:
            params["is_published"] = str(is_published)

        async with aiohttp.ClientSession() as session, session.get(
            self.quizes_endpoint,
            params=params,
        ) as response:
            data = await response.json()
            return TypeAdapter(list[Quiz]).validate_python(data)

    async def create_quiz(
        self,
        quiz: QuizCreate,
    ) -> Quiz:
        async with aiohttp.ClientSession(
            raise_for_status=True,
        ) as session, session.post(
            self.quotes_endpoint,
            json=quiz.model_dump(),
        ) as response:
            data = await response.json()
            return TypeAdapter(Quiz).validate_python(data)

    async def update_quiz(self, id_: int, quiz: QuizUpdate) -> Quiz:
        async with aiohttp.ClientSession(  # noqa SIM117
            raise_for_status=True,
        ) as session:
            async with session.patch(  # noqa SIM117
                urljoin(self.quotes_endpoint, str(id_)),
                json=quiz.model_dump(exclude_unset=True),
            ) as response:
                data = await response.json()
                return TypeAdapter(Quiz).validate_python(data)

    @staticmethod
    async def get_image_bytes(url: str) -> bytes:
        async with aiohttp.ClientSession() as session, session.get(url) as response:
            return await response.read()
