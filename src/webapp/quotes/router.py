from config.database import get_async_session
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import TypeAdapter
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Post, Quiz
from .schemas import (
    PaginationQueryParams,
    PostQueryParams,
    PostSchemaCreate,
    PostSchemaRead,
    PostSchemaUpdate,
    QuizSchemaCreate,
    QuizSchemaRead,
    QuizSchemaUpdate,
)
from .utils import set_quiz_answers

router = APIRouter(
    prefix="/quotes",
    tags=["Quotes"],
)


@router.get("")
async def get_quotes(
    query_params: PostQueryParams = Depends(),
    pagination_query_params: PaginationQueryParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> list[PostSchemaRead]:
    query = select(Post)
    for key, value in query_params.model_dump().items():
        if value is not None:
            query = query.where(getattr(Post, key) == value)
    query = query.limit(pagination_query_params.limit).offset(pagination_query_params.offset)
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
async def update_quote(
    quote_id: int,
    quote: PostSchemaUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> PostSchemaRead:
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


@router.get("/quiz")
async def get_quizes(
    query_params: PostQueryParams = Depends(),
    pagination_query_params: PaginationQueryParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> list[QuizSchemaRead]:
    query = select(Quiz)
    for key, value in query_params.model_dump().items():
        if value is not None:
            query = query.where(getattr(Quiz, key) == value)
    query = query.limit(pagination_query_params.limit).offset(pagination_query_params.offset)
    result = await session.execute(query)
    quizes = TypeAdapter(list[QuizSchemaRead]).validate_python(result.scalars().all(), from_attributes=True)
    for quiz in quizes:
        await set_quiz_answers(quiz, session)
    return quizes


@router.post("/quiz", status_code=status.HTTP_201_CREATED)
async def create_quiz(quiz: QuizSchemaCreate, session: AsyncSession = Depends(get_async_session)) -> QuizSchemaRead:
    new_quiz = Quiz(**quiz.model_dump())
    session.add(new_quiz)
    await session.commit()
    await session.refresh(new_quiz)
    return new_quiz


@router.patch("/quiz/{quiz_id}", status_code=status.HTTP_200_OK)
async def update_quiz(
    quiz_id: int,
    quiz: QuizSchemaUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> QuizSchemaRead:
    query = select(Quiz).where(Quiz.id == quiz_id)
    result = await session.execute(query)
    quiz_to_update = result.scalars().first()
    if not quiz_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="quiz not found")
    stmt = update(Quiz).where(Quiz.id == quiz_to_update.id).values(quiz.model_dump(exclude_unset=True))
    await session.execute(stmt)
    await session.commit()
    await session.refresh(quiz_to_update)
    return quiz_to_update
