from pyrogram import Client, filters
from config import OWNER_ID, LOGO, LOG_CHANNEL, AUTH_USERS
from AKG import app
from AKG.core.keys_db import is_user_in_db, get_user_info


# Command handler for /info command
@app.on_message(filters.regex("INFO"))
def info_command(client, message):
  user_id = message.from_user.id
  if user_id:
    user_data = get_user_info(user_id)
    if user_data:
      formatted_info = f"┌**SOURCE NETWORK**\n"
      formatted_info += f"┠ User Info\n"
      formatted_info += f"┠ Key: {user_data['key']}\n"
      formatted_info += f"┠ User ID: {user_data['user_id']}\n"
      formatted_info += f"┠ Key Status: {user_data['key_status']}\n"
      formatted_info += f"┠ Status: {user_data['status']}\n"
      formatted_info += f"┠ Start Date: {user_data['start_on']}\n"
      formatted_info += f"┠ Current Date: {user_data['current']}\n"
      formatted_info += f"┠ End Date: {user_data['end_on']}\n"
      formatted_info += f"┠ Days Left: {user_data['days_left']}\n"
      formatted_info += "┖"

      message.reply(formatted_info)
    else:
      message.reply(f"User with ID {user_id} not found.")
  else:
    message.reply("Please provide a valid user ID or username.")
