import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart
from aiogram.types import BufferedInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from inner_api_client import InnerApiClient
from inner_api_client.entities import PostCreate
from loguru import logger

from .config.constants import QUOTE_GROUP_ID
from .config.utils import get_image_bytes
from .config.settings import settings

logging.basicConfig(level=logging.INFO)

inner_api_client = InnerApiClient()

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Asia/Novosibirsk")


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
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
    
async def send_post():
    posts = await inner_api_client.get_posts(is_published=False)
    post = posts[0]
    logger.debug("GOT post (id={}) to be sent {}", post.id, post)
    
    image = BufferedInputFile(
        file = await get_image_bytes(url=post.image_with_text),
        filename=inner_api_client.minio_client.get_filename_from_url(url=post.image_with_text),
    )
    await bot.send_photo(chat_id=QUOTE_GROUP_ID, photo=image, caption=post.text)


async def main():
    scheduler.start()
    await dp.start_polling(bot)


def configure_scheduled_tasks(scheduler: AsyncIOScheduler) -> None:
    trigger = OrTrigger([CronTrigger(hour=6, timezone="Asia/Novosibirsk"), CronTrigger(hour=10, timezone="Asia/Novosibirsk"), CronTrigger(hour=18, timezone="Asia/Novosibirsk")])
    scheduler.add_job(send_post, trigger=trigger)


if __name__ == "__main__":
    configure_scheduled_tasks(scheduler)
    asyncio.run(main())
