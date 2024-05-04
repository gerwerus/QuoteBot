import os
from urllib.parse import urlparse

from minio import Minio

from .settings import MinioSettings


class MinioClient:
    def __init__(self, cli: Minio | None = None, settings: MinioSettings | None = None) -> None:
        self.settings = settings or MinioSettings.initialize_from_environment()
        self.cli = cli or self._configure_cli()
    
    @staticmethod
    def get_filename_from_url(url: str) -> str:
        return os.path.basename(urlparse(url).path)
    
    def _configure_cli(self) -> Minio:
        return Minio(
            f"{self.settings.MINIO_STORAGE_ENDPOINT_HOST}:{self.settings.MINIO_STORAGE_ENDPOINT_PORT}",
            access_key=self.settings.MINIO_STORAGE_ACCESS_KEY,
            secret_key=self.settings.MINIO_STORAGE_SECRET_KEY,
            secure=False,
        )
