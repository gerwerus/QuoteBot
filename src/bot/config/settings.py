import os
from dataclasses import dataclass
from typing import Self

from aiogram import Bot
from inner_api_client import InnerApiClient
from quote_post_client import QuoteGeneratorClient


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
bot = Bot(token=settings.TOKEN)
inner_api_client = InnerApiClient()
quote_post_client = QuoteGeneratorClient()
