import hashlib
import json
import random
import psutil
from datetime import datetime, timedelta
from bcrypt import hashpw, checkpw, gensalt

from src.utils.database_connection import DatabaseConnection, TIME_FORMAT

SESSION_DURATION = 3600  # Seconds
USER_TYPES = {'A': 'admin', 'U': 'user'}


def perform_login(username: str, password: str):
    b_password = bytes(password, encoding='utf8')

    with DatabaseConnection() as connection:
        try:
            user_id, db_password = connection.cursor.execute(
                f'SELECT id, password FROM users WHERE username = ?',
                (username,)).fetchone()
        except TypeError:
            return None
    return user_id if checkpw(b_password, bytes(db_password)) else None


def perform_register(username: str, password: str, mail: str):
    b_password = bytes(password, encoding='utf8')
    hashed_password = hashpw(b_password, gensalt(14))

    with DatabaseConnection() as connection:
        result = connection.cursor.execute(f'SELECT username FROM users WHERE username = ?',
                                           (username,)).fetchall()
        if len(result) != 0:
            return None
        connection.cursor.execute(f'INSERT INTO users (username, password, mail) VALUES(?, ?, ?)',
                                  (username, hashed_password, mail))

        user_id = connection.cursor.execute(f'SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]
    return user_id


def is_admin(user_id: int):
    with DatabaseConnection() as connection:
        try:
            user_type = connection.cursor.execute(
                f'SELECT type FROM users WHERE id = ?',
                (user_id,)).fetchone()[0]
            user_type = USER_TYPES[user_type]
        except TypeError:
            return None
    return user_type if user_type else None


def start_session(user_id, session_duration=SESSION_DURATION):
    session_token = generate_session_token()
    valid_to = datetime.utcnow() + timedelta(seconds=session_duration)
    valid_to_str = valid_to.strftime(TIME_FORMAT)

    with DatabaseConnection() as connection:
        connection.cursor.execute(f'INSERT INTO sessions (session_token, valid_to, user_id) VALUES (?, ?, ?)',
                                  (session_token, valid_to_str, user_id))
    return session_token


def obtain_user_id_from_session(session_token):
    with DatabaseConnection() as connection:
        user_id = connection.cursor.execute(
            f'SELECT user_id FROM sessions WHERE session_token = ?',
            (session_token,)).fetchone()[0]
    return user_id


def generate_session_token() -> str:
    data = {
        "cpu_usage": psutil.cpu_percent(interval=None),
        "cpu_count": psutil.cpu_count(),
        "cpu_stats": psutil.cpu_stats(),
        "cpu_frequency": psutil.cpu_freq(percpu=True),
        "disk_partitions": psutil.disk_partitions(),
        "boot_time": psutil.boot_time(),
        "random_number": random.randint(0, 123456789)
    }
    encoded = json.dumps(data).encode()
    session_token = hashlib.sha512(encoded, usedforsecurity=True).hexdigest()
    return session_token


def validate_session_token(session_token: str):
    with DatabaseConnection() as connection:
        db_result = connection.cursor.execute(f'SELECT * FROM sessions WHERE session_token = ?',
                                              (session_token,)).fetchone()

        if db_result is None:
            return None
        else:
            db_session_token, db_valid_to = db_result
            valid_to = datetime.strptime(db_valid_to, TIME_FORMAT)
            if valid_to < datetime.utcnow():
                connection.cursor.execute(f'DELETE FROM sessions WHERE session_token = ?', (session_token,))
                return False
    return True
