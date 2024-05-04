from dataclasses import dataclass
import os
from typing import Self


@dataclass
class MinioSettings:
    MINIO_STORAGE_ENDPOINT_HOST: str
    MINIO_STORAGE_ENDPOINT_PORT: int
    MINIO_STORAGE_ACCESS_KEY: str
    MINIO_STORAGE_SECRET_KEY: str
    MINIO_STORAGE_BUCKET: str
    
    @classmethod
    def initialize_from_environment(cls) -> Self:
        return cls(
            MINIO_STORAGE_ENDPOINT_HOST=os.getenv("MINIO_STORAGE_ENDPOINT_HOST", "minio"),
            MINIO_STORAGE_ENDPOINT_PORT=int(os.getenv("MINIO_STORAGE_ENDPOINT_PORT", 9000)),
            MINIO_STORAGE_ACCESS_KEY=os.getenv("MINIO_STORAGE_ACCESS_KEY", ""),
            MINIO_STORAGE_SECRET_KEY=os.getenv("MINIO_STORAGE_SECRET_KEY", ""),
            MINIO_STORAGE_BUCKET=os.getenv("MINIO_STORAGE_BUCKET", ""),
        )
