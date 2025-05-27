import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

from EsproMusic import app
from config import YOUTUBE_IMG_URL
logging.basicConfig(level=logging.INFO)


class Ritik1:
    def __init__(
        self,
        cache_dir: str = "cache",
        font_path1: str = "EsproMusic/assets/font2.ttf",
        font_path2: str = "EsproMusic/assets/font.ttf",
    ):
        self.cache_dir = cache_dir
        self.font_path1 = font_path1
        self.font_path2 = font_path2
        self.app_name = unidecode(app.name)
        os.makedirs(self.cache_dir, exist_ok=True)

    def change_image_size(self, max_width: int, max_height: int, image: Image.Image) -> Image.Image:
        width_ratio = max_width / image.size[0]
        height_ratio = max_height / image.size[1]
        new_width = int(width_ratio * image.size[0])
        new_height = int(height_ratio * image.size[1])
        return image.resize((new_width, new_height))

    def clear_title(self, text: str) -> str:
        words = text.split(" ")
        title = ""
        for word in words:
            if len(title) + len(word) < 60:
                title += " " + word
        return title.strip()

    async def get_thumbnail(self, video_id: str) -> str:
        final_path = os.path.join(self.cache_dir, f"{video_id}.png")
        if os.path.isfile(final_path):
            return final_path

        url = f"https://www.youtube.com/watch?v={video_id}"

        try:
            results = VideosSearch(url, limit=1)
            search_result = (await results.next())["result"][0]

            title = re.sub(r"\W+", " ", search_result.get("title", "Unsupported Title")).title()
            duration = search_result.get("duration", "Unknown Mins")
            thumbnail_url = search_result["thumbnails"][0]["url"].split("?")[0]
            views = search_result.get("viewCount", {}).get("short", "Unknown Views")
            channel = search_result.get("channel", {}).get("name", "Unknown Channel")

            temp_path = os.path.join(self.cache_dir, f"thumb_{video_id}.png")
            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail_url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(temp_path, mode="wb") as f:
                            await f.write(await resp.read())

            youtube_img = Image.open(temp_path)
            resized = self.change_image_size(1280, 720, youtube_img).convert("RGBA")
            background = ImageEnhance.Brightness(resized.filter(ImageFilter.BoxBlur(10))).enhance(0.5)

            draw = ImageDraw.Draw(background)
            arial = ImageFont.truetype(self.font_path1, 30)
            font = ImageFont.truetype(self.font_path2, 30)

            # Draw text and elements
            draw.text((1110, 8), self.app_name, fill="white", font=arial)
            draw.text((55, 560), f"{channel} | {views[:23]}", fill="white", font=arial)
            draw.text((57, 600), self.clear_title(title), fill="white", font=font)
            draw.line([(55, 660), (1220, 660)], fill="white", width=5, joint="curve")
            draw.ellipse([(918, 648), (942, 672)], outline="white", fill="white", width=15)
            draw.text((36, 685), "00:00", fill="white", font=arial)
            draw.text((1185, 685), duration[:23], fill="white", font=arial)

            os.remove(temp_path)
            background.save(final_path)
            return final_path

        except Exception as e:
            print(f"[ThumbnailGenerator Error] {e}")
            return YOUTUBE_IMG_URL



#second class

class Ritik2:
    def __init__(self, font_dir="EsproMusic/assets"):
        self.font_regular = os.path.join(font_dir, "font.ttf")
        self.font_secondary = os.path.join(font_dir, "font2.ttf")
        self.font_title = os.path.join(font_dir, "font3.ttf")
        self.play_icon_path = os.path.join(font_dir, "play_icons.png")
        self.cache_dir = "cache"
        os.makedirs(self.cache_dir, exist_ok=True)

    def _change_image_size(self, maxWidth, maxHeight, image):
        widthRatio = maxWidth / image.size[0]
        heightRatio = maxHeight / image.size[1]
        return image.resize((int(widthRatio * image.size[0]), int(heightRatio * image.size[1])))

    def _truncate(self, text):
        parts = text.split(" ")
        text1, text2 = "", ""
        for part in parts:
            if len(text1) + len(part) < 30:
                text1 += " " + part
            elif len(text2) + len(part) < 30:
                text2 += " " + part
        return [text1.strip(), text2.strip()]

    def _random_color(self):
        return tuple(random.randint(0, 255) for _ in range(3))

    def _generate_gradient(self, width, height, start_color, end_color):
        base = Image.new('RGBA', (width, height), start_color)
        top = Image.new('RGBA', (width, height), end_color)
        mask = Image.new('L', (width, height))
        mask_data = [int(60 * (y / height)) for y in range(height) for _ in range(width)]
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base

    def _crop_center_circle(self, img, output_size, border, border_color, crop_scale=1.5):
        half_w, half_h = img.size[0] / 2, img.size[1] / 2
        larger_size = int(output_size * crop_scale)
        img = img.crop((half_w - larger_size/2, half_h - larger_size/2, half_w + larger_size/2, half_h + larger_size/2))
        img = img.resize((output_size - 2*border, output_size - 2*border))
        final_img = Image.new("RGBA", (output_size, output_size), border_color)
        mask_main = Image.new("L", (output_size - 2*border, output_size - 2*border), 0)
        draw_main = ImageDraw.Draw(mask_main)
        draw_main.ellipse((0, 0, output_size - 2*border, output_size - 2*border), fill=255)
        final_img.paste(img, (border, border), mask_main)
        mask_border = Image.new("L", (output_size, output_size), 0)
        draw_border = ImageDraw.Draw(mask_border)
        draw_border.ellipse((0, 0, output_size, output_size), fill=255)
        return Image.composite(final_img, Image.new("RGBA", final_img.size, (0, 0, 0, 0)), mask_border)

    def _draw_text_with_shadow(self, background, draw, position, text, font, fill, offset=(3, 3), blur=5):
        shadow = Image.new("RGBA", background.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.text(position, text, font=font, fill="black")
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
        background.paste(shadow, offset, shadow)
        draw.text(position, text, font=font, fill=fill)

    async def generate(self, videoid: str):
        try:
            cached_path = os.path.join(self.cache_dir, f"{videoid}_v4.png")
            if os.path.isfile(cached_path):
                return cached_path

            results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
            result = (await results.next())["result"][0]

            title = re.sub(r"\W+", " ", result.get("title", "Unsupported Title")).title()
            duration = result.get("duration", "Live")
            thumbnail_url = result.get("thumbnails", [{}])[0].get("url", "").split("?")[0]
            views = result.get("viewCount", {}).get("short", "Unknown Views")
            channel = result.get("channel", {}).get("name", "Unknown Channel")

            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail_url) as resp:
                    if resp.status == 200:
                        raw = await resp.read()
                        path = os.path.join(self.cache_dir, f"thumb{videoid}.png")
                        async with aiofiles.open(path, "wb") as f:
                            await f.write(raw)

            original_img = Image.open(path)
            os.remove(path)

            base = self._change_image_size(1280, 720, original_img).convert("RGBA")
            base = ImageEnhance.Brightness(base.filter(ImageFilter.BoxBlur(20))).enhance(0.6)
            gradient = self._generate_gradient(1280, 720, self._random_color(), self._random_color())
            background = Image.blend(base, gradient, 0.2)

            draw = ImageDraw.Draw(background)
            fonts = {
                "arial": ImageFont.truetype(self.font_secondary, 30),
                "font": ImageFont.truetype(self.font_regular, 30),
                "title": ImageFont.truetype(self.font_title, 45)
            }

            circle = self._crop_center_circle(original_img, 400, 20, self._random_color())
            background.paste(circle, (120, 160), circle)

            truncated = self._truncate(title)
            self._draw_text_with_shadow(background, draw, (565, 180), truncated[0], fonts["title"], "white")
            self._draw_text_with_shadow(background, draw, (565, 230), truncated[1], fonts["title"], "white")
            self._draw_text_with_shadow(background, draw, (565, 320), f"{channel} | {views[:23]}", fonts["arial"], "white")

            # Progress bar
            duration_bar_color = self._random_color() if duration != "Live" else (255, 0, 0)
            bar_x, bar_y = 565, 380
            bar_len = 580

            if duration != "Live":
                pct = random.uniform(0.15, 0.85)
                draw.line([(bar_x, bar_y), (bar_x + int(bar_len * pct), bar_y)], fill=duration_bar_color, width=9)
                draw.line([(bar_x + int(bar_len * pct), bar_y), (bar_x + bar_len, bar_y)], fill="white", width=8)
                draw.ellipse(
                    [(bar_x + int(bar_len * pct) - 10, bar_y - 10), (bar_x + int(bar_len * pct) + 10, bar_y + 10)],
                    fill=duration_bar_color,
                )
            else:
                draw.line([(bar_x, bar_y), (bar_x + bar_len, bar_y)], fill=duration_bar_color, width=9)
                draw.ellipse([(bar_x + bar_len - 10, bar_y - 10), (bar_x + bar_len + 10, bar_y + 10)], fill=duration_bar_color)

            self._draw_text_with_shadow(background, draw, (565, 400), "00:00", fonts["arial"], "white")
            self._draw_text_with_shadow(background, draw, (1080, 400), duration, fonts["arial"], "white")

            play_icons = Image.open(self.play_icon_path).resize((580, 62))
            background.paste(play_icons, (565, 450), play_icons)

            background.save(cached_path)
            return cached_path

        except Exception as e:
            logging.error(f"Thumbnail generation error for video {videoid}: {e}")
            traceback.print_exc()
            return None
