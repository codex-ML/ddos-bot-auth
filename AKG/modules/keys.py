from pyrogram import Client, filters
from pyrogram.types import Message
from config import AUTH_USERS
from AKG import app
from AKG.core.keys_db import get_keys

@app.on_message(filters.command("keys"))
async def get_keys_command(client, message):
    # Call the get_keys function to retrieve keys
    keys = get_keys()

    # Format the keys data for sending as a message
    keys_message = ""
    for key_data in keys:
        keys_message += f"Key: {key_data['key']}, Status: {key_data['key_status']}\n"

    # Send the keys data as a message
    await message.reply_text(keys_message)