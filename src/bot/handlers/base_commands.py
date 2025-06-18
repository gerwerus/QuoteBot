from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from ..filters.admin import AdminFilter

router = Router(name="base_commands")

help_text = (
    "Доступные команды⚙️\n"
    "<b>Пост</b>🪧\n"
    "• /make_post - создать пост\n"
    "• /skip_post - пропустить пост\n"
    "• /send_post - отправить пост\n"
    "• /view_post - посмотреть пост\n"
    "<b>Викторина</b>🌠\n"
    "• /make_quiz - создать квиз\n"
    "• /skip_quiz - пропустить квиз\n"
    "• /send_quiz - отправить квиз\n"
    "• /view_quiz - посмотреть квиз\n"
    "<b>Пост с множеством изображений</b>🌆\n"
    "• /make_post_multiple_images - создать пост\n"
    "• /skip_post_multiple_images - пропустить пост\n"
    "• /send_post_multiple_images - отправить пост\n"
    "• /view_post_multiple_images - посмотреть пост\n"
)


@router.message(Command("start"), AdminFilter())
async def start_command(message: Message) -> None:
    text = f"Добро пожаловать, <b>{message.from_user.full_name}</b>!\n\n{help_text}"
    await message.answer(text, parse_mode="html")


@router.message(Command("help"), AdminFilter())
async def help_command(message: Message) -> None:
    await message.answer(help_text, parse_mode="html")
