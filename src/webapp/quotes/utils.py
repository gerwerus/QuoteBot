from random import shuffle

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Post
from .schemas import QuizSchemaRead


async def set_quiz_answers(quiz: QuizSchemaRead, session: AsyncSession) -> None:
    query = select(Post.author).where(Post.author != quiz.author).limit(100)
    result = await session.execute(query)
    authors = list(result.scalars().all())
    shuffle(authors)
    quiz.answers = authors[:3]
