from aiogram import Bot
from aiogram.types.bot_command import BotCommand
from aiogram.types.bot_command_scope_chat_member import BotCommandScopeChatMember


async def set_default_commands(bot: Bot) -> None:
    return await bot.set_my_commands(
        commands=[
            BotCommand(command="help", description="Помощь"),
            BotCommand(command="make_post", description="создать пост"),
            BotCommand(command="skip_post", description="пропустить пост"),
            BotCommand(command="send_post", description="отправить пост"),
            BotCommand(command="view_post", description="посмотреть пост"),
            BotCommand(command="make_quiz", description= "создать квиз"),
            BotCommand(command="skip_quiz", description= "пропустить квиз"),
            BotCommand(command="send_quiz", description= "отправить квиз"),
        ],
    )
    