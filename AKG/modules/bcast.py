import asyncio
import datetime
import os
import random
import string
import time
import traceback
from pyrogram.client import Client
from pyrogram import Client, filters
from AKG import broadcast
from AKG import app
from config import AUTH_USERS

@app.on_message(filters.command("bcast"))
async def broadcast_handler_open(_, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if m.reply_to_message is None:
        await m.delete()
    else:
        await broadcast(m, db)