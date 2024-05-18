from enum import Enum
import os


class FontChoicesRu(Enum):
    CENTURY_GOTHIC = os.path.join(os.path.dirname(__file__), "fonts/ru/century-gothic.ttf")
    GILROY_MEDIUM = os.path.join(os.path.dirname(__file__), "fonts/ru/gilroy-medium.ttf")


class ColorChoices(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
