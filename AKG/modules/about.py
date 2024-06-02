from pyrogram import Client, filters
from config import OWNER_ID, LOGO, LOG_CHANNEL, AUTH_USERS
from AKG import app


# Command handler for /about command
@app.on_message(filters.regex("ABOUT"))
def about_command(client, message):
  about_text = (
      "🤖**Bot Information**\n\n"
      f"🔹 Bot Name: SOURCE CODE\n"
      f"🔹 GitHub: [Profile ](https://github.com/codex-ML)\n"
      f"🔹 Channel: [Channel](https://t.me/source_code_network)\n"
      f"🔹 Group: [Group](https://https://t.me/+Y9O5ptuPEFs3NGE1)\n"
      f"🔹 Developer: AKG\n"
      f"🔹 Developed with: Pyrogram\n"
      f"🔹 Version: 1.0.0\n"
      f"🔹 Support: [Contact](https://t.me/xi_xi_xi_xi_xi_xi)\n")

  message.reply(about_text, disable_web_page_preview=True)
