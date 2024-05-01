import io
import textwrap
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
    ):
        with Image.open(img_stream) as img:
            W, H = img.size
            font = ImageFont.truetype(font_path.value)
            self.__draw_multiple_line_text(
                img,
                text,
                font,
                text_color,
                H / 2 + offset_y,
            )
            img.save("a_test.png")


# response = requests.get(
#     "https://images.unsplash.com/photo-1417325384643-aac51acc9e5d?q=75&fm=jpg"
# )
# a = ImageTextClient()
# a.image_place_text(
#     "asgdgkdmlsfdsfs sdfsdokwfdflfgfs И немного русского шамана",
#     io.BytesIO(response.content),
# )
