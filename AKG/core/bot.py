from pyrogram.client import Client
from config import api_id, api_hash, bot_token


class Bot(Client):

  def __init__(self):
    super().__init__("bot",
                     api_id=api_id,
                     api_hash=api_hash,
                     bot_token=bot_token)


print("bot Connected Successfully!")
