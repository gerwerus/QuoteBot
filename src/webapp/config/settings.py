import os
from dataclasses import dataclass
from typing import Self


@dataclass
class Settings:
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    MINIO_STORAGE_ENDPOINT_HOST: str
    MINIO_STORAGE_ENDPOINT_PORT: int
    MINIO_STORAGE_ACCESS_KEY: str
    MINIO_STORAGE_SECRET_KEY: str
    MINIO_STORAGE_BUCKET: str

    @classmethod
    def initialize_from_environment(cls) -> Self:
        return cls(
            DB_HOST=os.getenv("POSTGRES_HOST"),
            DB_PORT=os.getenv("POSTGRES_PORT"),
            DB_NAME=os.getenv("POSTGRES_DB"),
            DB_USER=os.getenv("POSTGRES_USER"),
            DB_PASS=os.getenv("POSTGRES_PASSWORD"),
            MINIO_STORAGE_ENDPOINT_HOST=os.getenv("MINIO_STORAGE_ENDPOINT_HOST"),
            MINIO_STORAGE_ENDPOINT_PORT=int(os.getenv("MINIO_STORAGE_ENDPOINT_PORT")),
            MINIO_STORAGE_ACCESS_KEY=os.getenv("MINIO_STORAGE_ACCESS_KEY"),
            MINIO_STORAGE_SECRET_KEY=os.getenv("MINIO_STORAGE_SECRET_KEY"),
            MINIO_STORAGE_BUCKET=os.getenv("MINIO_STORAGE_BUCKET"),
        )


settings = Settings.initialize_from_environment()
