from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup
from pyrogram.types import Message
from AKG import app, check_user_subscription
from AKG.core.keys_db import is_user_in_db, has_active_key
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.on_message(filters.command("sshc"))
async def ssh_checker(client, message):
  if len(message.command) < 2:
    await message.reply_text("Usage: /sshc <ip>")
    return

  ip = message.command[1]
  url = f'https://sshcheck.com/server/{ip}/22'
  headers = {
      'User-Agent':
      'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
      'Accept':
      'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
      'Accept-Encoding': 'gzip, deflate, br',
      'Connection': 'keep-alive',
      'Referer': 'https://sshcheck.com/',
      'Upgrade-Insecure-Requests': '1',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-User': '?1'
  }

  try:
    logger.info(f"Fetching SSH check results for IP: {ip}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_content = response.text
    logger.info("SSH check response fetched successfully")

    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find_all('tr')

    result = {}
    for row in rows:
      columns = row.find_all('td')
      if len(columns) == 2:
        key = columns[0].get_text(strip=True)
        value = columns[1].get_text(strip=True)
        result[key] = value

    server_identification = result.get('Server Identification:')
    generated_at = result.get('Generated at:')

    if server_identification and generated_at:
      result_message = (
          f"**SSH Test Result for `{ip}`**\n"
          f"**Server Identification:** `{server_identification}`\n"
          f"**Generated at:** `{generated_at}`")
      logger.info(f"SSH check results for {ip}: {result_message}")
    else:
      result_message = "Failed to retrieve the required information."
      logger.warning("Required information not found in SSH check results")

    await message.reply_text(result_message)

  except requests.RequestException as e:
    logger.error(f"HTTP request failed: {e}")
    await message.reply_text("Failed to fetch the SSH check result.")

  except Exception as e:
    logger.error(f"An error occurred: {e}")
    await message.reply_text(f"An error occurred: {e}")
