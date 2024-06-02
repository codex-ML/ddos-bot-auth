from pyrogram import Client, filters
from pyrogram.types import Message
from AKG import app
from AKG.core.keys_db import get_key_details, update_key_activation, get_current_time, calculate_days_left


@app.on_message(filters.command("activate"))
async def activate_key_command(client, message: Message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /activate <key>")
        return

    key = message.command[1]
    user_id = message.from_user.id

    # Get key details from the database
    key_details = get_key_details(key)
    if not key_details:
        await message.reply_text("Invalid key.")
        return

    # Check key status
    key_status = key_details['key_status']
    if key_status == "expired":
        await message.reply_text("This key is expired.")
        return
    elif key_status == "active":
        await message.reply_text("This key has already been used.")
        return

    # Get current time from the API
    current_time_data = get_current_time()
    current_time = current_time_data
    end_date = key_details['end_on']
    days_left = calculate_days_left(end_date, current_time)

    # Update key activation details in the database
    update_key_activation(key, user_id, current_time)

    # Reply to the user
    await message.reply_text(
        f"Key activated successfully! Days left: {days_left}")
