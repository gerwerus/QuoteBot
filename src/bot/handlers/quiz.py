from random import SystemRandom

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from inner_api_client.entities import QuizUpdate
from loguru import logger

from ..config.constants import QUOTE_GROUP_ID
from ..config.settings import bot, inner_api_client, quote_post_client
from ..filters.admin import AdminFilter

router = Router(name="quiz")
randint = SystemRandom().randint
choice = SystemRandom().choice
shuffle = SystemRandom().shuffle


@router.message(Command("make_quiz"), AdminFilter())
async def make_quiz(message: Message) -> None:
    try:
        quiz = await quote_post_client.get_quiz()
        logger.debug("Quiz (id={}) was created", quiz.id)
        await message.answer(f"Quiz (id={quiz.id}) was created")
    except Exception as e:
        logger.error("Failed to create quiz: {}", e, backtrace=True)
        await message.answer("Не удалось создать викторину, попробуйте еще раз.")


@router.message(Command("skip_quiz"), AdminFilter())
async def skip_quiz(message: Message) -> None:
    quizzes = await inner_api_client.get_quizzes(is_published=False)
    if not quizzes:
        raise ValueError("Нет квизов для отправки")

    quiz = quizzes[0]
    await inner_api_client.update_quiz(quiz.id, quiz=QuizUpdate(is_published=True))
    await message.answer(f"Квиз (id={quiz.id}) был пропущен")


@router.message(Command("send_quiz"), AdminFilter())
async def force_send_quiz(message: Message) -> None:
    try:
        await send_quiz(chat_id=QUOTE_GROUP_ID)
    except ValueError as e:
        await message.answer(str(e))
    await message.answer(f"Квиз был отправлен в chat_id={QUOTE_GROUP_ID}")


@router.message(Command("view_quiz"), AdminFilter())
async def view_quiz(message: Message) -> None:
    try:
        await send_quiz(chat_id=message.chat.id, set_is_published=False)
    except ValueError as e:
        await message.answer(str(e))


async def send_quiz(chat_id: int, *, set_is_published: bool = True) -> None:
    quizzes = await inner_api_client.get_quizzes(is_published=False)
    if not quizzes:
        raise ValueError("Нет квизов для отправки")

    quiz = quizzes[0]
    logger.debug("GOT quiz (id={}) to be sent {}", quiz.id, quiz)

    options = quiz.answers
    options.append(quiz.author)
    shuffle(options)
    answer_index = options.index(quiz.author)
    emojis = "🏔🤔🧐❓👉🧠👤🌚🗿"

    await bot.send_poll(
        chat_id=chat_id,
        question=f"{choice(emojis)}Кто является автором цитаты? «{quiz.text}»",
        options=options,
        is_anonymous=True,
        type="quiz",
        correct_option_id=answer_index,
    )

    if set_is_published:
        await inner_api_client.update_quiz(quiz.id, quiz=QuizUpdate(is_published=True))
