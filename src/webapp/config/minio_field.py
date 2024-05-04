from sqlalchemy import Dialect
from sqlalchemy.types import TypeDecorator, String


class MinioField(TypeDecorator):
    impl = String

    cache_ok = True

    def __init__(self, bucket_name: str, **kwargs):
        self.bucket_name = bucket_name
        super().__init__(**kwargs)

    def process_result_value(self, value: str, dialect: Dialect) -> dict[str, str]:
        return {"bucket_name": self.bucket_name, "object_name": value}
    