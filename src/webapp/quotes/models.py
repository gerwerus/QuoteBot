from config.database import Base
from config.minio_field import MinioField
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import URLType

app_name = "quotes"


class Post(Base):
    __tablename__ = f"{app_name}_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(String(length=128))
    image_url: Mapped[str] = mapped_column(URLType)
    image_with_text: Mapped[str | None] = mapped_column(
        MinioField(bucket_name="quotes-files"),
        nullable=True,
    )
    keyword_ru: Mapped[str | None] = mapped_column(String(length=64), nullable=True)
    keyword_en: Mapped[str | None] = mapped_column(String(length=64), nullable=True)
    is_published: Mapped[bool] = mapped_column(default=False)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}> id={self.id}"


class Quiz(Base):
    __tablename__ = f"{app_name}_quiz"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(String(length=128))
    is_published: Mapped[bool] = mapped_column(default=False)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}> id={self.id}"


class PostMultipleImage(Base):
    __tablename__ = f"{app_name}_posts_multiple_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(String(length=128))
    is_published: Mapped[bool] = mapped_column(default=False)
    image_urls: Mapped[list["Image"]] = relationship(
        back_populates="post_multiple_image",
        lazy="selectin",
    )

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}> id={self.id}"


class Image(Base):
    __tablename__ = f"{app_name}_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(URLType)
    post_multiple_image_id = mapped_column(ForeignKey(PostMultipleImage.id))
    post_multiple_image: Mapped["PostMultipleImage"] = relationship(
        back_populates="image_urls",
    )

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}> id={self.id}"
