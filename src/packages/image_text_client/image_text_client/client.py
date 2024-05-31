import io
import textwrap
import uuid
from typing import Literal

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from .entities import ColorChoices, FontChoicesRu, WatermarkChoices

ImageFormats = Literal["jpeg", "png"]


class ImageTextClient:
    def __make_blur(
        self,
        xy: tuple[int, int],
        size: tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont,
        fill_color: ColorChoices,
        blur_amount: int = 18,
    ) -> Image:
        blurred_img = Image.new("RGBA", size)
        draw = ImageDraw.Draw(blurred_img)
        draw.text(xy=xy, text=text, fill=fill_color.value, font=font)
        blurred_img = blurred_img.filter(ImageFilter.GaussianBlur(blur_amount))
        return blurred_img

    def __draw_multiple_line_text(
        self,
        image: Image,
        *,
        text: str,
        font: ImageFont.FreeTypeFont,
        text_color: ColorChoices,
        text_start_height: int,
        with_blur: bool = True,
    ) -> int:
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size
        _, _, symbol_width, _ = font.getbbox("a")
        symbols_per_line = min(40, image_width / symbol_width)
        lines = textwrap.wrap(text, width=symbols_per_line)
        _, _, _, line_height = font.getbbox(lines[0])
        y_text = text_start_height - len(lines) * line_height / 2
        for line in lines:
            _, _, line_width, line_height = font.getbbox(line)
            if with_blur:
                blurred_img = self.__make_blur(
                    xy=((image_width - line_width) / 2, y_text),
                    size=image.size,
                    text=line,
                    font=font,
                    fill_color=ColorChoices.BLACK,
                )
                image.paste(blurred_img, blurred_img)
            draw.text(
                ((image_width - line_width) / 2, y_text),
                line,
                font=font,
                fill=text_color.value,
            )
            y_text += line_height
        return y_text + line_height * 2

    def change_brightness(self, image: Image, brightness: float = 0.6) -> Image:
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(brightness)

    def add_watermark(self, image: Image, watermark: WatermarkChoices) -> Image:
        image_w, image_h = image.size

        with Image.open(watermark.value) as watermark:
            watermark_w, watermark_h = watermark.size
            image.paste(
                watermark,
                ((image_w - watermark_w) // 2, int(0.85 * image_h)),
                watermark,
            )

        return image

    def image_place_text(
        self,
        image: Image,
        *,
        text: str,
        author: str | None = None,
        fontsize: int = 32,
        font_path: FontChoicesRu = FontChoicesRu.CENTURY_GOTHIC,
        text_color: ColorChoices = ColorChoices.WHITE,
        offset_y: int = 0,
    ) -> tuple[bytes, str]:
        width, height = image.size
        font = ImageFont.truetype(font_path.value, size=fontsize)
        text_y_end = self.__draw_multiple_line_text(
            image,
            text=text,
            font=font,
            text_color=text_color,
            text_start_height=int(0.35 * height) + offset_y,
        )
        if author:
            self.__draw_multiple_line_text(
                image,
                text=author,
                font=font,
                text_color=text_color,
                text_start_height=text_y_end,
            )
        return image

    def get_image_name(self, image: Image, format: ImageFormats) -> str:
        width, height = image.size
        return f"{str(uuid.uuid4())}_{width}x{height}.{format}"

    def process_image(
        self,
        img_stream: str | io.BytesIO,
        *,
        text: str,
        author: str | None = None,
        fontsize: int = 40,
        font_path: FontChoicesRu = FontChoicesRu.CENTURY_GOTHIC,
        text_color: ColorChoices = ColorChoices.WHITE,
        offset_y: int = 0,
        format: ImageFormats = "jpeg",
        watermark: WatermarkChoices | None = None,
    ) -> str:
        with Image.open(img_stream) as image:
            image = self.change_brightness(image)
            image = self.image_place_text(
                image,
                text=text,
                author=author,
                fontsize=fontsize,
                font_path=font_path,
                text_color=text_color,
                offset_y=offset_y,
            )

            if watermark:
                image: Image = self.add_watermark(image, watermark=watermark)

            with io.BytesIO() as image_bytes:
                image.save(image_bytes, format=format)
                return image_bytes.getvalue(), self.get_image_name(image, format)
