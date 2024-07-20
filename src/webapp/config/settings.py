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

    @classmethod
    def initialize_from_environment(cls) -> Self:
        return cls(
            DB_HOST=os.getenv("POSTGRES_HOST", ""),
            DB_PORT=os.getenv("POSTGRES_PORT", ""),
            DB_NAME=os.getenv("POSTGRES_DB", ""),
            DB_USER=os.getenv("POSTGRES_USER", ""),
            DB_PASS=os.getenv("POSTGRES_PASSWORD", ""),
        )


settings = Settings.initialize_from_environment()
