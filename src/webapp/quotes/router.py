from config.database import get_async_session
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Post
from .schemas import PostSchemaCreate, PostSchemaRead, PostSchemaUpdate, PostQueryParams

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


@router.patch("/{quote_id}", status_code=status.HTTP_200_OK)
async def update_quote(quote_id: int, quote: PostSchemaUpdate, session: AsyncSession = Depends(get_async_session)) -> PostSchemaRead:
    query = select(Post).where(Post.id == quote_id)
    result = await session.execute(query)
    quote_to_update = result.scalars().first()
    if not quote_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    stmt = update(Post).where(Post.id == quote_to_update.id).values(quote.model_dump(exclude_unset=True))
    await session.execute(stmt)
    await session.commit()
    await session.refresh(quote_to_update)
    return quote_to_update
