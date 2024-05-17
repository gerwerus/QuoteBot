import aiohttp
from pydantic import TypeAdapter

from .entities import UnsplashModel
from .settings import UnsplashSettings


class UnsplashClient:
    API_URL: str = "https://api.unsplash.com/photos/random"
    
    def __init__(self, settings: UnsplashSettings | None = None) -> None:
        self.settings = settings or UnsplashSettings.initialize_from_environment()

    async def get_photo_by_keyword(self, keyword: str, amount: int = 1, width: int = 720) -> list[UnsplashModel]:
        params = {
            "query": keyword,
            "client_id": self.settings.ACCESS_KEY,
            "count": amount,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.API_URL, params=params) as response:
                json: list[dict] = await response.json()
                for el in json:
                    el.update(width=width)
                return TypeAdapter(list[UnsplashModel]).validate_python(json)
