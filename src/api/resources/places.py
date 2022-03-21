from src.utils.database_connection import DatabaseConnection


def get_all_places():
    with DatabaseConnection() as connection:
        places = connection.cursor.execute(f'SELECT * FROM places ORDER BY level_id').fetchall()
    return places


def get_parking_places(parking_id: int):
    with DatabaseConnection() as connection:
        query = f"""
                SELECT pl.id as id, pl.status as status, pl.level_id as level_id
                FROM places pl
                    JOIN levels l ON l.id = pl.level_id
                WHERE l.parking_id = ? ORDER BY level_id
                """
        places = connection.cursor.execute(query, (parking_id,)).fetchall()
    return places


def get_place_status(place_id: int):
    with DatabaseConnection() as connection:
        status = connection.cursor.execute(f'SELECT status FROM places WHERE id = ?', (place_id,)).fetchone()[0]
    return status


def do_occupy_place(place_id: int):
    with DatabaseConnection() as connection:
        connection.cursor.execute(f'UPDATE places SET status = 2 WHERE id = ?', (place_id,))
    return True


def do_free_place(place_id: int):
    with DatabaseConnection() as connection:
        connection.cursor.execute(f'UPDATE places SET status = 0 WHERE id = ?', (place_id,))
    return False


def do_reserve_place(place_id: int):
    with DatabaseConnection() as connection:
        connection.cursor.execute(f'UPDATE places SET status = 1 WHERE id = ?', (place_id,))
    return False


def db_get_name_of_parking_and_level(place_id: int):
    query = """
                SELECT p.id, p.name, l.name
                FROM parkings p
                    JOIN levels l on p.id = l.parking_id
                    JOIN places pl on l.id = pl.level_id
                WHERE pl.id = ?
                """
    with DatabaseConnection() as connection:
        result = connection.cursor.execute(query, (place_id,)).fetchone()
    return result
