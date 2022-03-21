from datetime import datetime

from src.utils.database_connection import DatabaseConnection, TIME_FORMAT

GET_ENERGY_HISTORY_QUERY = 'SELECT post_date, value FROM energy_history'
ADD_ENERGY_HISTORY_QUERY = 'INSERT INTO energy_history (post_date, value) VALUES(?, ?)'


def db_get_data():
    with DatabaseConnection() as connection:
        result = connection.cursor.execute(GET_ENERGY_HISTORY_QUERY).fetchall()
    return [(datetime.strptime(date, TIME_FORMAT), value) for date, value in result]

def db_save_post(value: float):
    with DatabaseConnection() as connection:
        connection.cursor.execute(ADD_ENERGY_HISTORY_QUERY, (str(datetime.now()), value))
    return True
