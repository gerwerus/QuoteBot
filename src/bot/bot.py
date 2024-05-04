import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart
from aiogram.types import BufferedInputFile
from inner_api_client import InnerApiClient
from inner_api_client.entities import PostCreate
import requests

from .config.settings import settings

logging.basicConfig(level=logging.INFO)

inner_api_client = InnerApiClient()

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await bot.send_message(chat_id=-1002044200889, text="Hello!")
    
    post = PostCreate(
        text="Hello!",
        author="Bot",
        image_url="https://t4.ftcdn.net/jpg/06/66/00/13/240_F_666001386_68GsUMjRfNTTj9sOuNUW7FTPal16CV9G.jpg",
        image_with_text="image_with_text.jpg",
        keyword_ru="keyword_ru",
        keyword_en="keyword_en",
    )
    image_response = requests.get("https://t4.ftcdn.net/jpg/06/66/00/13/240_F_666001386_68GsUMjRfNTTj9sOuNUW7FTPal16CV9G.jpg")
    
    created_post = await inner_api_client.create_post(post, image_data=image_response.content, bucket_name="quotes-files")
    print(created_post)

    # image = BufferedInputFile(response.content, filename="image.jpg")
    # await bot.send_photo(chat_id=-1002044200889, photo=image, caption="Hello!")
    
    
    await message.answer("Hello!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
