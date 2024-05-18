import asyncio
import logging

from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger

from .config.constants import QUOTE_GROUP_ID, TIMEZONE
from .config.settings import bot
from .handlers.quotes import router as quotes_router
from .handlers.quotes import send_post

logging.basicConfig(level=logging.INFO)


def configure_scheduled_tasks(scheduler: AsyncIOScheduler) -> None:
    trigger = OrTrigger(
        [
            CronTrigger(hour=6, timezone=TIMEZONE),
            CronTrigger(hour=10, timezone=TIMEZONE),
            CronTrigger(hour=18, timezone=TIMEZONE),
        ],
    )
    scheduler.add_job(send_post, trigger=trigger, kwargs={"chat_id": QUOTE_GROUP_ID})


async def main() -> None:
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)

    dp.include_routers(quotes_router)
    configure_scheduled_tasks(scheduler)

    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
