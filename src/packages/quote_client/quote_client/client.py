import aiohttp
import asyncio
import random

from .entities import LangChoices, QuoteModel


class QuoteClient:
    API_URL = "http://api.forismatic.com/api/1.0/"
    DEFAULT_PARAMS = {"method": "getQuote", "format": "json"}

    async def __get_quote(self, lang: LangChoices) -> QuoteModel:
        params = {
            "lang": lang.value,
            "key": random.randint(0, 10**6 - 1),
            **self.DEFAULT_PARAMS,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.API_URL, params=params) as response:
                return QuoteModel.model_validate(await response.json())

    async def get_quotes(self, amount: int = 1, lang: LangChoices = LangChoices.RUSSIAN) -> list[QuoteModel]:
        tasks = []
        for _ in range(amount):
            tasks.append(asyncio.create_task(self.__get_quote(lang)))
        return await asyncio.gather(*tasks)
