from random import SystemRandom

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from inner_api_client.entities import QuizUpdate
from loguru import logger

from ..config.constants import QUOTE_GROUP_ID
from ..filters.admin import AdminFilter

router = Router(name="base_commands")


@router.message(Command("help"), AdminFilter())
async def help(message: Message) -> None:
    text = "Доступные команды⚙️\n"\
        "<b>Post</b>🪧\n"\
        "• /make_post - создать пост\n"\
        "• /skip_post - пропустить пост\n"\
        "• /send_post - отправить пост\n"\
        "• /view_post - посмотреть пост\n"\
        "<b>Quiz</b>🌠\n"\
        "• /make_quiz - создать квиз\n"\
        "• /skip_quiz - пропустить квиз\n"\
        "• /send_quiz - отправить квиз\n"
    await message.answer(text, parse_mode="html")
