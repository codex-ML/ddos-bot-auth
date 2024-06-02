from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID, LOGO, LOG_CHANNEL, AUTH_USERS
from AKG import app
import requests
from AKG import XD_URL


@app.on_message(filters.regex("HELP"))
async def panel_command(c, m: Message):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    doc_message = (
        "<code>┏╼==============Documentation============╾<code>\n"
        "<code>┣-                                        <code>\n"
        "<code>┣===============USER COMMANDS===========<code>\n"
        "<code>┣-                                        <code>\n"
        "<code>┣-                **Attack COMMANDS**        <code>\n"
        "<code>┣- `/udp  ip  port duration`   - Duration <code>\n"
        "<code>┣- `/attack  ip  port duration`   - Duration <code>\n"
        "<code>┣- `/sshc  ip `   -  ssh port checker <code>\n"
        "<code>┣-             **NMAP**             <code>\n"
        "<code>┣- `/nmap  arg ` -script -os -port -open  [No Of keys] - Gen keys <code>\n"
        "<code>┣-             **ACTIVATE COMMANDS**             <code>\n"
        "<code>┣- `/activate <keys>`  - activate subscription<code>\n"
        "<code>┣-             **INFO  COMMANDS**             <code>\n"
        "<code>┣- `INFO` - Get account Info                  <code>\n"
        "<code>┣-                                        <code>\n"
        "<code>┣-╼=========ADMIN COMMANDS===========╾<code>\n"
        "<code>┣-             **Key Generator**             <code>\n"
        "<code>┣- `/gen mm/dd/YYYY ` [No Of keys] - Gen keys <code>\n"
        "<code>┣-             **STATS**             <code>\n"
        "<code>┣- `STATS ` [No Of keys] - Gen keys <code>\n"
        "<code>┣-             **DELETE**             <code>\n"
        "<code>┣- `/delete <key>` - Get panel links                 <code>\n"
        "<code>┣-             **PANEL LINK**             <code>\n"
        "<code>┣- `PANEL` - Get panel links                 <code>\n"
        "<code>┗╼===============Documentation===========╾<code>")

    # Respond with the panel link including the global IP address
    await m.reply_text(doc_message)
