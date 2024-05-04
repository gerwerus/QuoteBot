from config.database import get_async_session
from config.named_file import NamedFile
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Post
from .schemas import PostSchemaCreate, PostSchemaRead

router = APIRouter(
    prefix="/quotes",
    tags=["Quotes"],
)


@router.get("")
async def get_quotes(session: AsyncSession = Depends(get_async_session)) -> list[PostSchemaRead]:
    query = select(Post)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_quote(quote: PostSchemaCreate, session: AsyncSession = Depends(get_async_session)) -> PostSchemaRead:
    file = None
    if quote.image_with_text_url:
        file = NamedFile(content=quote.image_with_text_url.data, filename=quote.image_with_text_url.filename)
    quote_dict = quote.model_dump()
    quote_dict["image_with_text_url"] = file

    new_quote = Post(**quote_dict)
    session.add(new_quote)
    await session.commit()
    await session.refresh(new_quote)
    return new_quote
