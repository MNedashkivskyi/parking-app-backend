from src.utils.database_connection import DatabaseConnection

ADD_PARKING_HISTORY_QUERY = 'INSERT INTO parking_history (place_id, car_id, start_time, battery_on_start, charging_speed) VALUES(?, ?, ?, ?, ?)'
END_PARKING_HISTORY_QUERY = 'UPDATE parking_history SET end_time = ?, battery_on_end = ? WHERE place_id = ? AND battery_on_end IS NULL'
GET_CAR_FROM_PLACE_QUERY = 'SELECT car_id FROM parking_history WHERE place_id = ? AND end_time IS NULL'
GET_PLACE_FROM_CAR_QUERY = 'SELECT place_id FROM parking_history WHERE car_id = ? AND end_time IS NULL'
GET_BATTERY_STATUS_QUERY = 'SELECT start_time, battery_on_start, charging_speed FROM parking_history WHERE car_id = ? AND end_time IS NULL'


def db_initialize_record(place_id: int, car_id: int, time: str, battery: float, charging: int) -> int:
    with DatabaseConnection() as connection:
        connection.cursor.execute(ADD_PARKING_HISTORY_QUERY, (place_id, car_id, time, battery, charging))
    return True


def db_add_end_to_record(place_id: int, time: str, battery: float) -> bool:
    with DatabaseConnection() as connection:
        connection.cursor.execute(END_PARKING_HISTORY_QUERY, (time, battery, place_id))
    return True


def db_get_car(place_id: int):
    with DatabaseConnection() as connection:
        result = connection.cursor.execute(GET_CAR_FROM_PLACE_QUERY, (place_id,)).fetchone()
    return result[0] if result is not None else None


def db_get_place(car_id: int):
    with DatabaseConnection() as connection:
        result = connection.cursor.execute(GET_PLACE_FROM_CAR_QUERY, (car_id,)).fetchone()
    return result[0] if result is not None else None


def db_get_battery_status(car_id: int):
    with DatabaseConnection() as connection:
        results = connection.cursor.execute(GET_BATTERY_STATUS_QUERY, (car_id,)).fetchone()
    return results
