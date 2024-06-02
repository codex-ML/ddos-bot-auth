from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID, LOGO, LOG_CHANNEL, AUTH_USERS
from AKG import app
import requests
from AKG import XD_URL


@app.on_message(filters.regex("PANEL") & filters.user(OWNER_ID))
async def panel_command(c, m: Message):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    # Respond with the panel link including the global IP address
    await m.reply_text(
        f"**〘======Panel=======〙**\n\n{XD_URL}/keys\n\n〘======Panel=======〙")
