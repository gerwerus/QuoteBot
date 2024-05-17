import asyncio

from image_text_client import ImageTextClient
from unsplash_client import UnsplashClient
from quote_client import QuoteClient


class QuoteGeneratorClient:
    async def get_post(self, amount, image_width):
        quote_bot = QuoteClient()
        quotes = await asyncio.gather(
            asyncio.create_task(quote_bot.get_quotes(amount=amount))
        )
        # get keyword
        keywords = ["jesus", "baby", "love"]
        unsplash_bot = UnsplashClient()
        for keyword in keywords:
            imgs = await asyncio.gather(
                asyncio.create_task(
                    unsplash_bot.get_by_keyword(
                        keyword=keyword, photo_amount=1, width=image_width
                    )
                )
            )
        image_text_bot = ImageTextClient()
        for post in zip(quotes, imgs):
            image_text_bot.image_place_text(
                text=post[0],
            )
