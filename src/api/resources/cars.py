from src.utils.database_connection import DatabaseConnection

GET_CARS_QUERY = 'SELECT id, manufacturer, model, registration_number, preferred_battery_percent, battery_volume FROM cars WHERE owner_id = ?'
SAVE_CAR_QUERY = 'INSERT INTO cars (manufacturer, model, registration_number, owner_id, preferred_battery_percent) VALUES(?, ?, ?, ?, 20)'
DELETE_CAR_QUERY = 'DELETE FROM cars WHERE registration_number = ?'
GET_CAR_BATTERY_QUERY = 'SELECT battery_volume FROM cars WHERE id = ?'
SET_CAR_BATTERY_QUERY = 'UPDATE cars SET battery_volume = ? WHERE id = ?'
GET_CAR_PREFFERED_BATTERY_QUERY = 'SELECT preferred_battery_percent FROM cars WHERE id = ?'
SET_CAR_PREFFERED_BATTERY_QUERY = 'UPDATE cars SET preferred_battery_percent = ? WHERE id = ?'


def db_get_cars(owner_id: int):
    with DatabaseConnection() as connection:
        result = connection.cursor.execute(GET_CARS_QUERY, (owner_id,)).fetchall()
    return result


def db_save_car(owner_id: int, manufacturer: str, model: str, registration_number: str):
    with DatabaseConnection() as connection:
        connection.cursor.execute(SAVE_CAR_QUERY, (manufacturer, model, registration_number, owner_id))
    return True


def db_get_car_owner(registration_number: str):
    with DatabaseConnection() as connection:
        try:
            user_id = connection.cursor.execute(
                f'SELECT owner_id FROM cars WHERE registration_number = ?',
                (registration_number,)).fetchone()[0]
        except TypeError:
            user_id = None
    return user_id


def db_delete_car(registration_number: str):
    with DatabaseConnection() as connection:
        connection.cursor.execute(DELETE_CAR_QUERY, (registration_number,))
    return True


def db_get_car_battery(car_id: int):
    with DatabaseConnection() as connection:
        result = connection.cursor.execute(GET_CAR_BATTERY_QUERY, (car_id,)).fetchone()
    return result[0] if result is not None else None


def db_is_car_battery_null(car_id: int):
    with DatabaseConnection() as connection:
        result = connection.cursor.execute(GET_CAR_BATTERY_QUERY, (car_id,)).fetchone()
    result = result[0] if result is not None else None
    return result is None


def db_set_car_battery(car_id: int, battery_volume: int):
    with DatabaseConnection() as connection:
        connection.cursor.execute(SET_CAR_BATTERY_QUERY, (battery_volume, car_id))
    return True


def db_get_preffered_car_battery(car_id: int):
    with DatabaseConnection() as connection:
        result = connection.cursor.execute(GET_CAR_PREFFERED_BATTERY_QUERY, (car_id,)).fetchone()
    return result[0] if result is not None else None


def db_set_preferred_car_battery(car_id: int, preferred_battery_percent: float):
    with DatabaseConnection() as connection:
        connection.cursor.execute(SET_CAR_PREFFERED_BATTERY_QUERY, (preferred_battery_percent, car_id))
    return True
