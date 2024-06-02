import os
from AKG.core.bot import Bot
from config import OWNER_ID, LOG_GROUP, DB_NAME
from pyrogram import filters, errors
import asyncio
import datetime
import os
import random
import string
import time
import traceback
import logging
from pyrogram.client import Client
from pyrogram import Client, filters
from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    PeerIdInvalid,
    UserIsBlocked,
)
from AKG.core.keys_db import is_user_in_db, has_active_key
import sqlite3
from AKG.core.ngrok import NGROK
from config import AUTH_USERS, BROADCAST_AS_COPY

XD_URL = None

broadcast_ids = {}

ngrok_instance = NGROK()
print(f"Public URL: {ngrok_instance.APP_URL}")
# Set global XD_URL
XD_URL = ngrok_instance.APP_URL

app = Bot()


def check_user_subscription(user_id):
    try:
        if has_active_key(user_id):
            return True, "Welcome! You can now use the bot commands."
        else:
            return False, "No active subscription found. Please activate your key or renew your subscription."
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return False, "An error occurred while accessing the database. Please try again later."
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False, "An unexpected error occurred. Please try again later."


async def send_msg(user_id, message):
    try:
        if BROADCAST_AS_COPY is False:
            await message.forward(chat_id=user_id)
        elif BROADCAST_AS_COPY is True:
            await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        logger.exception(
            f"An error occurred while sending message to user {user_id}: {e}")
        return 500, f"{user_id} : {traceback.format_exc()}\n"


# Update the broadcast function to log progress
async def broadcast(m, db):
    logger.info("Broadcast started")
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = "".join(
            [random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    out = await m.reply_text(
        text=
        f"Broadcast Started! You will be notified with log file when all the users are notified."
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(total=total_users,
                                       current=done,
                                       failed=failed,
                                       success=success)
    async with aiofiles.open("broadcast.txt", "w") as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id=int(user["id"]),
                                      message=broadcast_msg)
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user["id"])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(current=done, failed=failed, success=success))
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await m.reply_text(
            text=
            f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True,
        )
    else:
        await m.reply_document(
            document="broadcast.txt",
            caption=
            f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True,
        )
    os.remove("broadcast.txt")
