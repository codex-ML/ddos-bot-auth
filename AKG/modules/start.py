from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from config import OWNER_ID, LOGO, LOG_CHANNEL
from AKG import app
from AKG.core.db import is_user_in_db, add_user_to_db


@app.on_message(filters.command("start"))
async def startprivate(client, message):
    chat_id = message.from_user.id
    if not is_user_in_db(chat_id):
        data = await client.get_me()
        BOT_USERNAME = data.username
        add_user_to_db(chat_id)
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
            )
        else:
            await message.reply_text(
                f"#NewUser :- Name : {message.from_user.first_name} ID : {message.from_user.id}"
            )

    joinButton = InlineKeyboardMarkup([[
        InlineKeyboardButton("CHANNEL",
                             url="https://t.me/source_code_network"),
        InlineKeyboardButton("SUPPORT CHAT", url="https://t.me/CODEX_ML_bot"),
    ]])
    welcomed = f"Hey <b>{message.from_user.first_name}</b>\nWelcome to this bot. \nThis bot contains TOOLS \n\nSend /cmds to see its commands \n\n 🎚"
    await message.reply_photo(photo=LOGO,
                              caption=welcomed,
                              reply_markup=joinButton)
    await message.reply_text(".",
                             reply_markup=ReplyKeyboardMarkup(
                                 [["MENU"]], resize_keyboard=True))


@app.on_message(filters.regex("MENU"))
async def MENU(client, message):
    await message.reply_text(
        ".",
        reply_markup=ReplyKeyboardMarkup(
            [["INFO"], ["HELP"], ["SETTINGS"], ["ABOUT"], ["BACK"]],
            resize_keyboard=True))


@app.on_message(filters.regex("SETTINGS") & filters.user(OWNER_ID))
async def SETTINGS(client, message):
    await message.reply_text(".",
                             reply_markup=ReplyKeyboardMarkup(
                                 [["MENU"], ["STATS"], ["PANEL"], ["BACK"]],
                                 resize_keyboard=True))


@app.on_message(filters.regex("BACK"))
async def BACLK(client, message):
    await message.reply_text(".",
                             reply_markup=ReplyKeyboardMarkup(
                                 [["MENU"]], resize_keyboard=True))
