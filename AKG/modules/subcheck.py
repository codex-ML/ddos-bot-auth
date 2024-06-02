from pyrogram import Client, filters
from pyrogram.types import Message
from AKG import app, check_user_subscription
from AKG.core.keys_db import is_user_in_db, has_active_key
import logging


@app.on_message(filters.command("lol"))
async def start_command(client, message: Message):
    user_id = message.from_user.id

    can_proceed, response_message = check_user_subscription(user_id)
    if can_proceed:
        await message.reply_text("You can now use the bot commands.")
        # Here, you can handle further commands or actions for the user
    else:
        await message.reply_text(response_message)
