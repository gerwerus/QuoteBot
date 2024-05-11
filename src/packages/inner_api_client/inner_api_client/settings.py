import os
from dataclasses import dataclass
from typing import Self


@dataclass
class InnerApiSettings:
    BASE_URL: str

    @classmethod
    def initialize_from_environment(cls) -> Self:
        return cls(
            BASE_URL=os.getenv("INNER_API_URL", "http://webapp:8000"),
        )
