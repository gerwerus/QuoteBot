import os
from dataclasses import dataclass
from typing import Self


@dataclass
class JayCopilotSettings:
    API_KEY: str

    @classmethod
    def initialize_from_environment(cls) -> Self:
        return cls(
            API_KEY=os.getenv("JAY_COPILOT_API_KEY", ""),
        )
