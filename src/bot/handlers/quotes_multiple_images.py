from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import BufferedInputFile, Message
from aiogram.utils.media_group import MediaGroupBuilder
from inner_api_client.entities import PostMultipleImage, PostMultipleImageUpdate
from loguru import logger

from ..config.constants import QUOTE_GROUP_ID
from ..config.settings import bot, inner_api_client, quote_post_client
from ..filters.admin import AdminFilter

router = Router(name="post_multiple_images")


@router.message(Command("make_post_multiple_images"), AdminFilter())
async def make_post_multiple_images(message: Message) -> None:
    try:
        post = await quote_post_client.get_post_multiple_images()
        logger.debug("Post with multiple images (id={}) was created", post.id)
        await message.answer(f"Пост с множеством картинок (id={post.id}) был создан")
    except Exception as e:
        logger.error("Failed to create post with multiple images: {}", e, backtrace=True)
        await message.answer("Не удалось создать пост с множеством картинок, попробуйте еще раз.")


@router.message(Command("view_post_multiple_images"), AdminFilter())
async def view_post_multiple_images(message: Message) -> None:
    try:
        await send_post_multiple_images(chat_id=message.chat.id, set_is_published=False)
    except ValueError as e:
        await message.answer(str(e))
    else:
        await message.answer(f"Пост с множеством картинок был отправлен в chat_id={message.chat.id}")


@router.message(Command("skip_post_multiple_images"), AdminFilter())
async def skip_post_multiple_images(message: Message) -> None:
    posts = await inner_api_client.get_posts_multiple_images(is_published=False)
    if not posts:
        raise ValueError("Нет постов с для отправки")

    post = posts[0]
    await inner_api_client.update_post_multiple_images(post.id, post=PostMultipleImageUpdate(is_published=True))
    await message.answer(f"Пост с множеством картинок (id={post.id}) был пропущен")


@router.message(Command("send_post_multiple_images"), AdminFilter())
async def force_send_post_multiple_images(message: Message) -> None:
    try:
        await send_post_multiple_images(chat_id=QUOTE_GROUP_ID)
    except ValueError as e:
        await message.answer(str(e))
    else:
        await message.answer(f"Пост с множеством картинок был отправлен в chat_id={message.chat.id}")


def get_caption(post: PostMultipleImage) -> str:
    return f"""<b>{post.text}</b>
    
— <i>{post.author}</i>
    
<a href="https://t.me/oblivion_swamp">🏔 Топь Небытия 🏔</a>"""


async def send_post_multiple_images(chat_id: int, *, set_is_published: bool = True) -> None:
    posts = await inner_api_client.get_posts_multiple_images(is_published=False)
    if not posts:
        raise ValueError("Нет постов с множеством картинок для отправки")

    post = posts[0]
    logger.debug("GOT post with multiple images (id={}) to be sent {}", post.id, post)

    media_group = MediaGroupBuilder()
    post_caption = get_caption(post)
    for ind, img in enumerate(post.image_urls):
        media = BufferedInputFile(
            file=await inner_api_client.get_image_bytes(url=img.image_url),
            filename=inner_api_client.minio_client.get_filename_from_url(url=img.image_url),
        )
        if ind != 0:
            media_group.add_photo(media=media)
        else:
            media_group.add_photo(media=media, caption=post_caption, parse_mode="HTML")

    await bot.send_media_group(chat_id=chat_id, media=media_group.build())
    if set_is_published:
        await inner_api_client.update_post_multiple_images(post.id, post=PostMultipleImageUpdate(is_published=True))
