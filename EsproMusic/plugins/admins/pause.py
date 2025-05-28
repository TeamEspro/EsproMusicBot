from pyrogram import filters
from pyrogram.types import Message

from EsproMusic import app
from EsproMusic.core.call import Ritik
from EsproMusic.utils.database import is_Music_playing, Music_off
from EsproMusic.utils.decorators import AdminRightsCheck
from EsproMusic.utils.inline import close_markup
from config import BANNED_USERS


@app.on_message(filters.command(["pause", "cpause"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    if not await is_Music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await Music_off(chat_id)
    await Ritik.pause_stream(chat_id)
    await message.reply_text(
        _["admin_2"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
