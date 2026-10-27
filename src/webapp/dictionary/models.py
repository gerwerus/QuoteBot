from config.database import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

app_name = "dictionary"


class Word(Base):
    __tablename__ = f"{app_name}_words"

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(Text)
    definition: Mapped[str] = mapped_column(String(length=128))
    is_published: Mapped[bool] = mapped_column(default=False)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}> id={self.id}"
