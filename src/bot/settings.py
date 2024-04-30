import os
from dataclasses import dataclass
from typing import Self


@dataclass
class BotSettings:
    TOKEN: str
    
    @classmethod
    def initialize_from_environment(cls) -> Self:
        return cls(
            TOKEN=os.getenv("TOKEN"),
        )
