import os
from dataclasses import dataclass
from typing import Self


@dataclass
class QuoteClientSettings:
    PROXY_URL: str

    @classmethod
    def initialize_from_environment(cls) -> Self:
        return cls(
            PROXY_URL=os.getenv("PROXY_URL", ""),
        )
