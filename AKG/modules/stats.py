import asyncio
import importlib
import logging
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from AKG.modules import ALL_MODULES
from config import LOG_GROUP, LOGO
from AKG import app
from config import AUTH_USERS, OWNER_ID
from AKG.core.db import get_all_users


@app.on_message(filters.regex("STATS") & filters.user(OWNER_ID))
async def sts(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    user_ids = get_all_users()
    if not user_ids:
        await m.reply_text("No users found in the database.")
        return

    # Get user details
    users = await app.get_users(user_ids)

    # Prepare the message
    user_details = [
        f"┠User ID: {user.id} - First Name: {user.first_name}"
        for user in users
    ]
    user_list = "\n".join(user_details)

    await m.reply_text(text=f"**┌Total Users in Database 📂:**\n{user_list}",
                       quote=True)
