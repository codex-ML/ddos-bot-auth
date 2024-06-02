from pyrogram import Client, filters
from pyrogram.types import Message
from config import AUTH_USERS
from AKG import app
from AKG.core.keys_db import generate_keys

@app.on_message(filters.command("gen"))
async def generate_keys_command(client, message: Message):
    if message.from_user.id not in AUTH_USERS:
        await message.delete()
        return

    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: /gen <end_date> <number of keys>")
        return

    end_on = args[1]
    number_of_keys = 1 if len(args) == 2 else int(args[2])

    keys = generate_keys(end_on, number_of_keys)
    keys_text = "\n".join(keys)
    await message.reply_text(f"Generated {number_of_keys} key(s):\n{keys_text}")
