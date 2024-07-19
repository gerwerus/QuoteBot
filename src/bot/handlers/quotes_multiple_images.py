from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import BufferedInputFile, Message
from aiogram.utils.media_group import MediaGroupBuilder
from inner_api_client.entities import PostMultipleImageUpdate
from loguru import logger

from ..config.constants import QUOTE_GROUP_ID
from ..config.settings import bot, inner_api_client, quote_post_client
from ..filters.admin import AdminFilter

router = Router(name="quotes")


@router.message(Command("make_post_multiple_images"), AdminFilter())
async def make_post_multiple_images(message: Message) -> None:
    try:
        post = await quote_post_client.get_post_multiple_images()
        logger.debug("Post with multiple images (id={}) was created", post.id)
        await message.answer(f"Post with multiple images (id={post.id}) was created")
    except Exception as e:
        logger.error(
            "Failed to create post with multiple images: {}",
            e,
            backtrace=True,
        )
        await message.answer(
            "Post with multiple images was not created, see logs for more info.",
        )


@router.message(Command("view_post_multiple_images"), AdminFilter())
async def view_post_multiple_images(message: Message) -> None:
    await send_post_multiple_images(chat_id=message.chat.id, set_is_published=False)


@router.message(Command("skip_post_multiple_images"), AdminFilter())
async def skip_post_multiple_images(message: Message) -> None:
    posts = await inner_api_client.get_posts_multiple_images(is_published=False)
    if not posts:
        raise ValueError("No posts with multiple images to be sent")

    post = posts[0]
    await inner_api_client.update_post(
        post.id,
        post=PostMultipleImageUpdate(is_published=True),
    )
    await message.answer(f"Post with multiple images (id={post.id}) was skipped")


@router.message(Command("send_post_multiple_images"), AdminFilter())
async def force_send_post_multiple_images(message: Message) -> None:
    await send_post_multiple_images(chat_id=QUOTE_GROUP_ID)
    await message.answer(
        f"Post with multiple images was sent to chat_id={QUOTE_GROUP_ID}",
    )


async def send_post_multiple_images(
    chat_id: int,
    *,
    set_is_published: bool = True,
) -> None:
    posts = await inner_api_client.get_posts_multiple_images(is_published=False)
    if not posts:
        raise ValueError("No posts with multiple images to be sent")

    post = posts[0]
    logger.debug("GOT post with multiple images (id={}) to be sent {}", post.id, post)

    media_group = MediaGroupBuilder(caption=f"{post.text}\n— {post.author}")
    images = [
        BufferedInputFile(
            file=await inner_api_client.get_image_bytes(url=img.image_url),
            filename="maybe_name_should_be_different.jpg",
        )
        for img in post.image_urls
    ]
    for img in images:
        media_group.add_photo(media=img)
    await bot.send_media_group(chat_id=chat_id, media=media_group.build())
    if set_is_published:
        await inner_api_client.update_post(
            post.id,
            post=PostMultipleImageUpdate(is_published=True),
        )
