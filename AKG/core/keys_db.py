import sqlite3
import random
import string
import requests
from datetime import datetime
import asyncio
import logging

DB_FILE = "keys.db"
TIME_API_URL = "https://timeapi.io/api/Time/current/zone?timeZone=asia/kolkata"

# TIME_API_URL = "https://pastebin.com/raw/UUnNZrFV"


# Initialize the database
def initialize_keys_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 user_id INTEGER PRIMARY KEY
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS keys (
                 key TEXT PRIMARY KEY,
                 user_id INTEGER PRIMARY KEY,
                 key_status TEXT,
                 status BOOLEAN,
                 start_on TEXT,
                 current TEXT,
                 end_on TEXT,
                 days_left INTEGER
                 )''')
    conn.commit()
    conn.close()


def get_current_time():
    response = requests.get(TIME_API_URL)
    return response.json()['date']


async def check_key_dates():
    while True:
        await asyncio.sleep(60)  # Check key dates every 60 seconds
        current_time = get_current_time()
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(
            "SELECT * FROM keys WHERE status=1")  # Select only active keys
        keys = c.fetchall()
        for key in keys:
            key_details = {
                'key': key[0],
                'user_id': key[1],
                'key_status': key[2],
                'status': key[3],
                'start_on': key[4],
                'current': key[5],
                'end_on': key[6],
                'days_left': key[7]
            }
            # Calculate days left for each key
            days_left = calculate_days_left(key_details['end_on'],
                                            current_time)
            if days_left <= 0:
                # Set status to expired if days_left is negative or zero
                c.execute(
                    "UPDATE keys SET days_left=?, status=0, key_status='expired' WHERE key=?",
                    (days_left, key_details['key']))
            else:
                c.execute("UPDATE keys SET days_left=?, current=? WHERE key=?",
                          (days_left, current_time, key_details['key']))
        conn.commit()
        conn.close()


# Function to generate a random key
def generate_random_key(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# Function to generate keys and add them to the database
def generate_keys(end_on, number_of_keys=1):
    keys = []
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for _ in range(number_of_keys):
        key = generate_random_key()
        c.execute(
            "INSERT INTO keys (key, status, end_on, key_status) VALUES (?, ?, ?, ?)",
            (key, True, end_on, 'null'))
        keys.append(key)
    conn.commit()
    conn.close()
    return keys


def activate_key(user_id, key):
    if not is_key_available(key):
        return False

    current_time_data = get_current_time()
    start_on = current_time_data

    # Check if the key exists before accessing its details
    key_details = get_key_details(key)
    if key_details is None:
        return False

    end_on = key_details['end_on']
    end_date = datetime.strptime(end_on, "%m/%d/%Y")
    start_date = datetime.strptime(current_time_data['date'], "%m/%d/%Y")
    days_left = (end_date - start_date).days

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "UPDATE keys SET user_id=?, start_on=?, current=?, status=0, key_status='active', days_left=? WHERE key=?",
        (user_id, start_on, start_on, days_left, key))
    conn.commit()
    conn.close()
    return True


# Function to check if a key is available
def is_key_available(key):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM keys WHERE key=? AND status=1", (key, ))
    result = c.fetchone()
    conn.close()
    return result is not None


# Function to get key details
def get_key_details(key):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM keys WHERE key=?", (key, ))
    key_details = c.fetchone()
    conn.close()
    if key_details:
        return {
            'key': key_details[0],
            'user_id': key_details[1],
            'key_status': key_details[2],
            'status': key_details[3],
            'start_on': key_details[4],
            'current': key_details[5],
            'end_on': key_details[6],
            'days_left': key_details[7]
        }
    return None


def get_keys(status=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = "SELECT * FROM keys"
    params = ()

    if status is not None:
        query += " WHERE key_status=?"
        params = (status, )

    c.execute(query, params)
    keys = c.fetchall()
    conn.close()

    keys_data = []
    for key in keys:
        keys_data.append({
            'key': key[0],
            'user_id': key[1],
            'key_status': key[2],
            'status': key[3],
            'start_on': key[4],
            'current': key[5],
            'end_on': key[6],
            'days_left': key[7]
        })
    return keys_data


# Function to update the current time for each key in the database
async def update_current_time():
    while True:
        await asyncio.sleep(60)
        current_time = get_current_time()
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("UPDATE keys SET current=?", (current_time, ))
        conn.commit()
        conn.close()


def update_key_activation(key, user_id, start_time):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "UPDATE keys SET user_id=?, key_status='active', start_on=?, current=?, status=1 WHERE key=?",
        (user_id, start_time, start_time, key))
    conn.commit()
    conn.close()


def calculate_days_left(end_date, start_date):
    # Remove milliseconds portion if present
    start_date = current_time = get_current_time()

    # Parse start_date and end_date strings into datetime objects
    end_date = datetime.strptime(end_date, "%m/%d/%Y")
    start_date = datetime.strptime(start_date, "%m/%d/%Y")

    # Calculate the difference in days between end_date and start_date
    delta = end_date - start_date
    return delta.days


def has_active_key(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM keys WHERE user_id=? AND key_status='active'",
              (user_id, ))
    result = c.fetchone()
    conn.close()
    return result is not None


def is_user_in_db(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id, ))
    result = c.fetchone()
    conn.close()
    return result is not None


def get_user_info(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM keys WHERE user_id=?", (user_id, ))
    key_details = c.fetchone()
    conn.close()
    if key_details:
        return {
            'key': key_details[0],
            'user_id': key_details[1],
            'key_status': key_details[2],
            'status': key_details[3],
            'start_on': key_details[4],
            'current': key_details[5],
            'end_on': key_details[6],
            'days_left': key_details[7]
        }
    return None


def delete_user_or_key(identifier):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    try:
        # Try deleting as a key
        c.execute("DELETE FROM keys WHERE key=?", (identifier, ))
        key_deleted = c.rowcount

        # If no key was deleted, try deleting as a user_id
        if key_deleted == 0:
            c.execute("DELETE FROM users WHERE user_id=?", (identifier, ))
            user_deleted = c.rowcount

            if user_deleted == 0:
                return False, f"No key or user found with identifier: {identifier}"
            else:
                return True, f"User with ID {identifier} has been deleted."
        else:
            return True, f"Key {identifier} has been deleted."

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return False, "An error occurred while accessing the database. Please try again later."
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False, "An unexpected error occurred. Please try again later."
    finally:
        conn.commit()
        conn.close()


def get_usr_info(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Fetch user details from the database
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user_data = c.fetchone()

    if user_data:
        user_info = {
            'user_id': user_data[0],
            # Add more fields if needed
        }

        # Fetch associated key details from the database
        c.execute("SELECT * FROM keys WHERE user_id=?", (user_id,))
        keys_data = c.fetchall()

        user_keys = []
        for key in keys_data:
            key_info = {
                'key': key[0],
                'key_status': key[2],
                'status': key[3],
                'start_on': key[4],
                'current': key[5],
                'end_on': key[6],
                'days_left': key[7]
            }
            user_keys.append(key_info)

        user_info['keys'] = user_keys

        conn.close()
        return user_info
    else:
        logging.error(f"User with ID {user_id} not found.")
        conn.close()
        return None
