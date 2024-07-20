import asyncio
import random

import aiohttp

from .entities import LangChoices, QuoteModel


class QuoteClient:
    API_URL = "http://api.forismatic.com/api/1.0/"
    DEFAULT_PARAMS = {"method": "getQuote", "format": "json"}
    DEFAULT_UNKNOWN_AUTHOR = {
        LangChoices.ENGLISH: "Unknown author",
        LangChoices.RUSSIAN: "Неизвестный автор",
    }

    async def __get_quote(self, lang: LangChoices) -> QuoteModel:
        params = {
            "lang": lang.value,
            "key": random.randint(0, 10**6 - 1),
            **self.DEFAULT_PARAMS,
        }
        async with aiohttp.ClientSession() as session, session.get(
            self.API_URL,
            params=params,
        ) as response:
            quote = QuoteModel.model_validate(await response.json())
            quote.author = quote.author or self.DEFAULT_UNKNOWN_AUTHOR[lang]
            return quote

    async def get_quotes(
        self,
        amount: int = 1,
        lang: LangChoices = LangChoices.RUSSIAN,
    ) -> list[QuoteModel]:
        tasks = []
        for _ in range(amount):
            tasks.append(asyncio.create_task(self.__get_quote(lang)))
        return await asyncio.gather(*tasks)
