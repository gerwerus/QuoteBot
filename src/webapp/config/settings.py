from dataclasses import dataclass
import os
from typing import Self
from dotenv import load_dotenv
load_dotenv("C:/Users/admin/Desktop/QuoteBot/env/.env")


@dataclass
class Settings:
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    
    MINIO_STORAGE_ENDPOINT_HOST: str
    MINIO_STORAGE_ENDPOINT_PORT: str
    MINIO_STORAGE_ACCESS_KEY: str
    MINIO_STORAGE_SECRET_KEY: str
    MINIO_DEFAULT_BUCKETS: str

    @classmethod
    def initialize_from_environment(cls) -> Self:
        return cls(
            DB_HOST=os.getenv("POSTGRES_HOST"),
            DB_PORT=os.getenv("POSTGRES_PORT"),
            DB_NAME=os.getenv("POSTGRES_DB"),
            DB_USER=os.getenv("POSTGRES_USER"),
            DB_PASS=os.getenv("POSTGRES_PASSWORD"),
            
            MINIO_STORAGE_ENDPOINT_HOST=os.getenv("MINIO_STORAGE_ENDPOINT_HOST"),
            MINIO_STORAGE_ENDPOINT_PORT=os.getenv("MINIO_STORAGE_ENDPOINT_PORT"),
            MINIO_STORAGE_ACCESS_KEY=os.getenv("MINIO_STORAGE_ACCESS_KEY"),
            MINIO_STORAGE_SECRET_KEY=os.getenv("MINIO_STORAGE_SECRET_KEY"),
            MINIO_DEFAULT_BUCKETS=os.getenv("MINIO_DEFAULT_BUCKETS"),
        )

settings = Settings.initialize_from_environment()
