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
from quote_post_client import QuoteGeneratorClient
from loguru import logger

from .config.constants import QUOTE_GROUP_ID, TIMEZONE
from .config.settings import settings

logging.basicConfig(level=logging.INFO)

inner_api_client = InnerApiClient()

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TIMEZONE)
qoute_post_client = QuoteGeneratorClient()


async def send_post() -> None:
    posts = await inner_api_client.get_posts(is_published=False)
    if not posts:
        raise ValueError("No posts to be sent")

    post = posts[0]
    logger.debug("GOT post (id={}) to be sent {}", post.id, post)

    image = BufferedInputFile(
        file=await inner_api_client.get_image_bytes(url=post.image_with_text),
        filename=inner_api_client.minio_client.get_filename_from_url(url=post.image_with_text),
    )
    await bot.send_photo(chat_id=QUOTE_GROUP_ID, photo=image, caption=post.text)
    await inner_api_client.update_post(id=post.id, post=PostUpdate(is_published=True))


@dp.message(Command("make_post"))
async def make_post(message: types.Message) -> None:
    post = await qoute_post_client.get_post()
    logger.debug("Post (id={}) was created", post.id)
    await message.answer(f"Post (id={post.id}) was created")


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
