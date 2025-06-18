from aiogram import Bot
from aiogram.types.bot_command import BotCommand


async def set_default_commands(bot: Bot) -> bool:
    return await bot.set_my_commands(
        commands=[
            BotCommand(command="help", description="Помощь"),
            BotCommand(command="make_post", description="создать пост"),
            BotCommand(command="skip_post", description="пропустить пост"),
            BotCommand(command="send_post", description="отправить пост"),
            BotCommand(command="view_post", description="посмотреть пост"),
            BotCommand(command="make_quiz", description="создать квиз"),
            BotCommand(command="skip_quiz", description="пропустить квиз"),
            BotCommand(command="send_quiz", description="отправить квиз"),
            BotCommand(command="view_quiz", description="посмотреть квиз"),
            BotCommand(command="make_post_multiple_images", description="создать пост"),
            BotCommand(command="skip_post_multiple_images", description="пропустить пост"),
            BotCommand(command="send_post_multiple_images", description="отправить пост"),
            BotCommand(command="view_post_multiple_images", description="посмотреть пост"),
        ],
    )
