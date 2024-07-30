import asyncio
import logging

from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger

from .config.constants import QUOTE_GROUP_ID, TIMEZONE
from .config.settings import bot
from .handlers.base_commands import router as base_commands_router
from .handlers.quiz import router as quiz_router
from .handlers.quiz import send_quiz
from .handlers.quotes import router as quotes_router
from .handlers.quotes import send_post
from .handlers.quotes_multiple_images import router as post_multiple_images_router
from .handlers.quotes_multiple_images import send_post_multiple_images
from .services.command_settings import set_default_commands

logging.basicConfig(level=logging.INFO)


def configure_scheduled_tasks(scheduler: AsyncIOScheduler) -> None:
    trigger = OrTrigger([CronTrigger(hour=6, timezone=TIMEZONE), CronTrigger(hour=10, timezone=TIMEZONE)])
    scheduler.add_job(send_post, trigger=trigger, kwargs={"chat_id": QUOTE_GROUP_ID})
    scheduler.add_job(send_quiz, trigger=CronTrigger(hour=13, timezone=TIMEZONE), kwargs={"chat_id": QUOTE_GROUP_ID})
    scheduler.add_job(
        send_post_multiple_images,
        trigger=CronTrigger(hour=18, timezone=TIMEZONE),
        kwargs={"chat_id": QUOTE_GROUP_ID},
    )


async def main() -> None:
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)

    dp.include_routers(base_commands_router, quotes_router, quiz_router, post_multiple_images_router)
    configure_scheduled_tasks(scheduler)

    scheduler.start()
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
