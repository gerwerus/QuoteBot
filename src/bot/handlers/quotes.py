from random import SystemRandom

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import BufferedInputFile, Message
from inner_api_client import InnerApiClient
from inner_api_client.entities import PostUpdate
from loguru import logger
from quote_post_client import QuoteGeneratorClient

from ..config.constants import QUOTE_GROUP_ID
from ..config.settings import bot
from ..filters.admin import AdminFilter


router = Router(name="quotes")
randint = SystemRandom().randint
inner_api_client = InnerApiClient()
quote_post_client = QuoteGeneratorClient()


@router.message(Command("make_post"), AdminFilter())
async def make_post(message: Message) -> None:
    try:
        post = await quote_post_client.get_post()
        logger.debug("Post (id={}) was created", post.id)
        await message.answer(f"Post (id={post.id}) was created")
    except Exception:
        await message.answer("Post was not created, see logs for more info.")


@router.message(Command("view_post"), AdminFilter())
async def view_post(message: Message) -> None:
    posts = await inner_api_client.get_posts(is_published=False)
    if not posts:
        await message.answer("No posts to view")
        raise ValueError("No posts to view")

    post = posts[0]

    image = BufferedInputFile(
        file=await inner_api_client.get_image_bytes(url=post.image_with_text),
        filename=inner_api_client.minio_client.get_filename_from_url(url=post.image_with_text),
    )
    await message.answer_photo(photo=image, caption=await get_keywords_caption(post.keyword_ru))


async def send_post() -> None:
    posts = await inner_api_client.get_posts(is_published=False)
    if not posts:
        raise ValueError("No posts to be sent")

    post = posts[0]
    logger.debug("GOT post (id={}) to be sent {}", post.id, post)

    image = BufferedInputFile(
        file=await inner_api_client.get_image_bytes(url=post.image_with_text),
        filename=inner_api_client.minio_client.get_filename_from_url(url=post.image_with_text),
    )
    await bot.send_photo(chat_id=QUOTE_GROUP_ID, photo=image, caption=await get_keywords_caption(post.keyword_ru))
    await inner_api_client.update_post(id=post.id, post=PostUpdate(is_published=True))


async def get_keywords_caption(keyword: str) -> str:
    keywords = keyword.split(",")
    return "#" + " #".join(keywords[:randint(1, len(keywords))])  # randomize keywords amount
