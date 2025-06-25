from config.database import get_async_session
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Word
from .schemas import (
    PaginationQueryParams,
    WordQueryParams,
    WordSchemaCreate,
    WordSchemaRead,
    WordSchemaUpdate,
)

router = APIRouter(prefix="/dictionary", tags=["Dictionary"])


@router.get("")
async def get_words(
    query_params: WordQueryParams = Depends(),
    pagination_query_params: PaginationQueryParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> list[WordSchemaRead]:
    query = select(Word)
    for key, value in query_params.model_dump().items():
        if value is not None:
            query = query.where(getattr(Word, key) == value)
    query = query.limit(pagination_query_params.limit).offset(pagination_query_params.offset)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_word(word: WordSchemaCreate, session: AsyncSession = Depends(get_async_session)) -> WordSchemaRead:
    new_word = Word(**word.model_dump())
    session.add(new_word)
    await session.commit()
    await session.refresh(new_word)
    return new_word


@router.patch("/{word_id}", status_code=status.HTTP_200_OK)
async def update_word(
    word_id: int,
    word: WordSchemaUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> WordSchemaRead:
    query = select(Word).where(Word.id == word_id)
    result = await session.execute(query)
    quote_to_update = result.scalars().first()
    if not quote_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found",
        )
    stmt = update(Word).where(Word.id == quote_to_update.id).values(word.model_dump(exclude_unset=True))
    await session.execute(stmt)
    await session.commit()
    await session.refresh(quote_to_update)
    return quote_to_update
