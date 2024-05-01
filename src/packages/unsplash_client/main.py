import aiohttp
import asyncio

from entities import UnsplashModel
from pydantic import TypeAdapter


class UnsplashClient:
    API_URL: str | None = "https://api.unsplash.com/photos/random"
    ACCESS_KEY: str = "V1LPKwkwfKej0dfeGSaic24gzq9d84hjoh7I54zj6LI"

    async def __get_photo(self, keyword: str, amount: int, width: int) -> str:
        params = {
            "query": keyword,
            "client_id": self.ACCESS_KEY,
            "count": amount,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.API_URL, params=params) as response:
                json: list[dict] = await response.json()
                for el in json:
                    el.update(width=width)
                return TypeAdapter(list[UnsplashModel]).validate_python(json)

    async def get_by_keyword(self, keyword, photo_amount, width: int) -> list[dict]:
        return await asyncio.gather(
            asyncio.create_task(self.__get_photo(keyword, photo_amount, width))
        )
    
    # async def download_photo(self, url) -> BytesIo:
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         with open(filename, 'wb') as f:
    #             f.write(response.content)
    #     else:
    #         print('Failed to download the photo.')


async def main():
    q = UnsplashClient()
    loop = asyncio.get_event_loop()
    task = loop.create_task(q.get_by_keyword("jesus", 3, 600))
    text = await asyncio.gather(task)
    print(text)


asyncio.run(main())
