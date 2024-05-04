import asyncio
import base64
import io
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart
from aiogram.types import BufferedInputFile
import requests

from .config.settings import settings

logging.basicConfig(level=logging.INFO)


bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await bot.send_message(chat_id=-1002044200889, text="Hello!")

    # url = "http://minio:9000/quotes-files/image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minio%2F20240504%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240504T090232Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=4ab7b6436e12e6a661f7f21dd60e13868fa310c719c7c5f4531d00b66165b68e"
    # response = requests.get(url)
    # image = BufferedInputFile(response.content, filename="image.jpg")
    # await bot.send_photo(chat_id=-1002044200889, photo=image, caption="Hello!")
    
    image_response = requests.get("https://t4.ftcdn.net/jpg/06/66/00/13/240_F_666001386_68GsUMjRfNTTj9sOuNUW7FTPal16CV9G.jpg")
    
with io.BytesIO() as file:
    file.write(image_response.content)
    file.seek(0)
    
    response = requests.post(
        "http://webapp:8000/quotes",
        json={
            "text": "Hello!",
            "author": "Author",
            "image_url": "http://google.com",
            "keyword_ru": "ru",
            "keyword_en": "en",
        },
        data={
            "image_with_text_url": {
                "data": base64.b64encode(file.read()),
            }
        }
    )
    
    await message.answer("Hello!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
