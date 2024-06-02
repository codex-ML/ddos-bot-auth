import subprocess
from pyrogram import Client, filters
import logging
from pyrogram.types import Message
from AKG import app

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#


@app.on_message(filters.command("nmap"))
async def nmap_scan(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /nmap options ip")
        return

    options = message.command[1]
    ip = message.command[2]

    try:
        logger.info(f"Running Nmap scan with options: {options} for IP: {ip}")

        if "-script" in options:
            command = f"nmap -Pn --script vuln {ip}"
        elif "-os" in options:
            command = f"sudo nmap -Pn -O {ip}"
        elif "-port" in options:
            command = f"nmap -p 1-100 {ip}"
        elif "-open" in options:
            command = f"nmap -Pn --open {ip}"
        else:
            await message.reply_text(
                "Invalid option provided. Please use '-script', '-os', or '-open'."
            )
            return
        await message.reply_text(
            f"Nmap scan processing for `{ip}`")
        # Execute the command using subprocess
        result = subprocess.run(command,
                                shell=True,
                                capture_output=True,
                                text=True)

        # Check if the command was successful
        if result.returncode == 0:
            await message.reply_text(
                f"Nmap scan result for {ip}:\n```\n{result.stdout}\n```")
        else:
            await message.reply_text(
                f"Failed to execute Nmap command. Error: {result.stderr}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await message.reply_text(f"An error occurred: {e}")
