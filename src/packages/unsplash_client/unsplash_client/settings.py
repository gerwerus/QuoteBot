from dataclasses import dataclass
import os
from typing import Self


@dataclass
class UnsplashSettings:
    ACCESS_KEY: str
    
    
    @classmethod
    def initialize_from_environment(cls) -> Self:
        return cls(
            ACCESS_KEY=os.getenv("UNSPLASH_ACCESS_KEY"),
        )