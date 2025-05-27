import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

from EsproMusic import app
from config import YOUTUBE_IMG_URL


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
