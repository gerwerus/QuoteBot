from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from sqlalchemy_file.storage import StorageManager
from libcloud.storage.drivers.minio import MinIOStorageDriver

from .settings import settings


DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
Base = declarative_base()

container = MinIOStorageDriver(
    key=settings.MINIO_STORAGE_ACCESS_KEY,
    secret=settings.MINIO_STORAGE_SECRET_KEY,
    host=settings.MINIO_STORAGE_ENDPOINT_HOST,
    port=settings.MINIO_STORAGE_ENDPOINT_PORT,
    secure=False,
).get_container(settings.MINIO_DEFAULT_BUCKETS)
StorageManager.add_storage("minio", container)

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
