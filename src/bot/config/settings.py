import os
from dataclasses import dataclass
from typing import Self


@dataclass
class BotSettings:
    ADMIN_IDS: list[int]
    TOKEN: str

    @classmethod
    def initialize_from_environment(cls) -> Self:
        return cls(
            ADMIN_IDS=list(map(int, os.getenv("ADMIN_IDS", "").split(";"))),
            TOKEN=os.getenv("BOT_TOKEN", ""),
        )


settings = BotSettings.initialize_from_environment()
