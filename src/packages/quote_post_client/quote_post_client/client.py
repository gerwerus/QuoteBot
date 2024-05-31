from io import BytesIO

from image_text_client import ImageTextClient
from image_text_client.entities import WatermarkChoices
from inner_api_client import InnerApiClient
from inner_api_client.entities import Post, PostCreate
from jay_copilot_client import JayCopilotClient
from quote_client import QuoteClient
from unsplash_client import UnsplashClient


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

    async def get_post(self) -> Post:
        quote = (await self.quote_client.get_quotes())[0]
        keywords = self.jay_copilot_client.get_quote_keywords(quote.text, 4)
        image_results = await self.unsplash_client.get_photo_by_keyword(keywords.en[0])
        image_url = image_results[0].link

        with BytesIO(
            await self.inner_api_client.get_image_bytes(url=image_url),
        ) as image:
            image_data, image_name = self.image_text_client.process_image(
                img_stream=image,
                text=quote.text,
                author=f"— {quote.author}",
                watermark=WatermarkChoices.OBLIVION_SWAMP,
            )
        post = PostCreate(
            text=quote.text,
            author=quote.author,
            image_url=image_url,
            image_with_text=image_name,
            keyword_ru=",".join(keywords.ru),
            keyword_en=",".join(keywords.en),
        )

        return await self.inner_api_client.create_post(
            post,
            image_data=image_data,
            bucket_name="quotes-files",
        )
