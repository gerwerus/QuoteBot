import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart
from dotenv import load_dotenv

from .settings import BotSettings

load_dotenv("C:/Users/admin/Desktop/QuoteBot/env/bot.env")
logging.basicConfig(level=logging.INFO)
settings = BotSettings.initialize_from_environment()

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await bot.send_message(chat_id=-1002044200889, text="Hello!")
    await message.answer("Hello!")

async def main():
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
