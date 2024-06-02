from pyrogram import Client, filters
from pyrogram.types import Message
from AKG import app,check_user_subscription
from AKG.core.keys_db import is_user_in_db, has_active_key,delete_user_or_key
import logging
import sqlite3

# Command handler for /delete <key/user_id>
@app.on_message(filters.command("delete"))
async def delete_command(client, message: Message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /delete <key/user_id>")
        return

    identifier = message.command[1]

    success, response_message = delete_user_or_key(identifier)
    await message.reply_text(response_message)