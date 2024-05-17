import asyncio

from image_text_client import ImageTextClient
from inner_api_client import InnerApiClient
from jay_copilot_client import JayCopilotClient
from unsplash_client import UnsplashClient
from quote_client import QuoteClient
from quote_client.entities import LangChoices


class QuoteGeneratorClient:
    def __init__(
        self,
        *,
        image_text_client: ImageTextClient | None = None,
        inner_api_client: InnerApiClient | None = None,
        jay_copilot_client: JayCopilotClient | None = None,
        quote_client: QuoteClient | None = None,
        unsplash_client: UnsplashClient | None = None,
    ):
        self.image_text_client = image_text_client or ImageTextClient()
        self.inner_api_client = inner_api_client or InnerApiClient()
        self.jay_copilot_client = jay_copilot_client or JayCopilotClient()
        self.quote_client = quote_client or QuoteClient()
        self.unsplash_client = unsplash_client or UnsplashClient()

    async def get_post(self):
        quote = self.quote_client.get_quotes(amount=1, lang=LangChoices.RUSSIAN)[0]
        keyword = self.jay_copilot_client.get_quote_keywords(quote.text, 1)[0]

        print(quote)
        print(keyword)
        
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("C:/Users/Катя/Desktop/QuoteBot/env/.env")
    
    client = QuoteGeneratorClient()
    asyncio.run(client.get_post())
