from pyrogram import filters
from pyrogram.types import Message

from EsproMusic import app
from EsproMusic.core.call import Ritik
from EsproMusic.utils.database import is_Music_playing, Music_on
from EsproMusic.utils.decorators import AdminRightsCheck
from EsproMusic.utils.inline import close_markup
from config import BANNED_USERS


@app.on_message(filters.command(["resume", "cresume"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_com(cli, message: Message, _, chat_id):
    if await is_Music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await Music_on(chat_id)
    await Ritik.resume_stream(chat_id)
    await message.reply_text(
        _["admin_4"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
