from sqlalchemy import Dialect
from sqlalchemy.types import String, TypeDecorator


class MinioField(TypeDecorator):
    impl = String

    cache_ok = True

    def __init__(self, bucket_name: str, **kwargs: dict):
        self.bucket_name = bucket_name
        super().__init__(**kwargs)

    def process_result_value(self, value: str | None, dialect: Dialect) -> dict[str, str | None]:
        return {"bucket_name": self.bucket_name, "object_name": value}
