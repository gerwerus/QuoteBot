import io
import textwrap
import uuid
from PIL import Image, ImageFont, ImageDraw

from .entities import ColorChoices, FontChoicesRu


class ImageTextClient:
    def __draw_multiple_line_text(
        self,
        image: Image,
        text: str,
        font: ImageFont.FreeTypeFont,
        text_color: ColorChoices,
        text_start_height: int,
    ):
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size
        lines = textwrap.wrap(text, width=40)
        _, _, _, line_height = font.getbbox(lines[0])
        y_text = text_start_height - len(lines) * line_height / 2
        for line in lines:
            _, _, line_width, line_height = font.getbbox(line)
            draw.text(
                ((image_width - line_width) / 2, y_text),
                line,
                font=font,
                fill=text_color.value,
            )
            y_text += line_height

    def image_place_text(
        self,
        text: str,
        img_stream: str | io.BytesIO,
        fontsize: int = 32,
        font_path: FontChoicesRu = FontChoicesRu.FONT1,
        text_color: ColorChoices = ColorChoices.WHITE,
        offset_y: int = 0,
    ) -> tuple[bytes, str]:
        with Image.open(img_stream) as img:
            W, H = img.size
            font = ImageFont.truetype(font_path.value, size=fontsize)
            self.__draw_multiple_line_text(
                img,
                text,
                font,
                text_color,
                H / 2 + offset_y,
            )
            image_name = f"{str(uuid.uuid4())}_{W}x{H}.{img.format.lower()}"
            
            with io.BytesIO() as image_bytes:
                img.save(image_bytes, format=img.format)
                return image_bytes.getvalue(), image_name
