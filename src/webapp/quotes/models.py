from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy_file import FileField
from sqlalchemy_utils import URLType

from config.database import Base

app_name = "quotes"

class Post(Base):
    __tablename__ = f"{app_name}_posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(String(length=128))
    image_url: Mapped[str] = mapped_column(URLType)
    image_with_text_url: Mapped[str | None] = mapped_column(FileField, nullable=True)
    keyword_ru: Mapped[str | None] = mapped_column(String(length=64), nullable=True)
    keyword_en: Mapped[str | None] = mapped_column(String(length=64), nullable=True)
    is_published: Mapped[bool] = mapped_column(default=False)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}> id={self.id}"
