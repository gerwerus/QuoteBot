from typing import Literal, Self

from pydantic import BaseModel, Field, field_validator, model_validator

Orientation = Literal["landscape", "portrait", "squarish"]


class UnsplashModel(BaseModel):
    link: str | dict = Field(alias="urls")
    width: int | None = Field(default=None, alias="width")

    @field_validator("link", mode="before")
    @classmethod
    def validate_link(cls, v: dict) -> str:
        return v["raw"]

    @model_validator(mode="after")
    def configure_link(self) -> Self:
        if self.width:
            self.link = f"{self.link}?q=75&fm=jpg&w={self.width}&fit=max"
        return self
