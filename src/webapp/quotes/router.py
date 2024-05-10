from config.database import get_async_session
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Post
from .schemas import PostSchemaCreate, PostSchemaRead, PostQueryParams

router = APIRouter(
    prefix="/quotes",
    tags=["Quotes"],
)


@router.get("")
async def get_quotes(query_params: PostQueryParams = Depends(), session: AsyncSession = Depends(get_async_session)) -> list[PostSchemaRead]:
    query = select(Post)
    for key, value in query_params.model_dump().items():
        if value is not None:
            query = query.where(getattr(Post, key) == value)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_quote(quote: PostSchemaCreate, session: AsyncSession = Depends(get_async_session)) -> PostSchemaRead:
    new_quote = Post(**quote.model_dump())
    session.add(new_quote)
    await session.commit()
    await session.refresh(new_quote)
    return new_quote
