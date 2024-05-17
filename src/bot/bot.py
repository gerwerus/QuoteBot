import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import BufferedInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from inner_api_client import InnerApiClient
from inner_api_client.entities import PostUpdate
from loguru import logger

from .config.constants import QUOTE_GROUP_ID, TIMEZONE
from .config.settings import settings
from .config.utils import get_image_bytes

logging.basicConfig(level=logging.INFO)

inner_api_client = InnerApiClient()

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TIMEZONE)


@dp.message(Command("send_post"))
async def cmd_start(message: types.Message) -> None:
    await send_post()
    # post = PostCreate(
    #     text="Hello!",
    #     author="Bot",
    #     image_url="https://t4.ftcdn.net/jpg/06/66/00/13/240_F_666001386_68GsUMjRfNTTj9sOuNUW7FTPal16CV9G.jpg",
    #     image_with_text="image_with_text.jpg",
    #     keyword_ru="keyword_ru",
    #     keyword_en="keyword_en",
    # )
    # image_response = requests.get("https://t4.ftcdn.net/jpg/06/66/00/13/240_F_666001386_68GsUMjRfNTTj9sOuNUW7FTPal16CV9G.jpg")

    # created_post = await inner_api_client.create_post(post, image_data=image_response.content, bucket_name="quotes-files")
    # print(created_post)


async def send_post() -> None:
    posts = await inner_api_client.get_posts(is_published=False)
    if not posts:
        raise ValueError("No posts to be sent")

    post = posts[0]
    logger.debug("GOT post (id={}) to be sent {}", post.id, post)

    image = BufferedInputFile(
        file=await get_image_bytes(url=post.image_with_text),
        filename=inner_api_client.minio_client.get_filename_from_url(url=post.image_with_text),
    )
    await bot.send_photo(chat_id=QUOTE_GROUP_ID, photo=image, caption=post.text)
    await inner_api_client.update_post(id=post.id, post=PostUpdate(is_published=True))


def configure_scheduled_tasks(scheduler: AsyncIOScheduler) -> None:
    trigger = OrTrigger(
        [
            CronTrigger(hour=6, timezone=TIMEZONE),
            CronTrigger(hour=10, timezone=TIMEZONE),
            CronTrigger(hour=18, timezone=TIMEZONE),
        ],
    )
    scheduler.add_job(send_post, trigger=trigger)


async def main() -> None:
    configure_scheduled_tasks(scheduler)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
