import os
from dataclasses import dataclass


@dataclass
class JayCopilotSettings:
    API_KEY: str

    @classmethod
    def initialize_from_environment(cls) -> "JayCopilotSettings":
        return cls(
            API_KEY=os.getenv("JAY_COPILOT_API_KEY"),
        )
