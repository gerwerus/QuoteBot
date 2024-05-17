from enum import Enum
import os


class FontChoicesRu(Enum):
    FONT1 = os.path.join(os.path.dirname(__file__), "fonts/ru/1.ttf")


class ColorChoices(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)