from src.utils.database_connection import DatabaseConnection


def get_all_parking_lot_ids():
    with DatabaseConnection() as connection:
        parking_lots = connection.cursor.execute("SELECT p.id FROM parkings p").fetchall()
    return [parking_lot[0] for parking_lot in parking_lots]


def get_all_parking_lots(city: str = None):
    with DatabaseConnection() as connection:
        query = """
                SELECT p.id, p.name, p.description, p.city, p.street, p.postal_code, p.image_url, COUNT(pl.id)
                FROM parkings p
                    JOIN levels l on p.id = l.parking_id
                    JOIN places pl on l.id = pl.level_id
                WHERE pl.status = 0
                GROUP BY p.id, p.name, p.description, p.city, p.street, p.postal_code, p.image_url
                """
        parking_lots = connection.cursor.execute(query).fetchall()
    if city:
        filtered_parking_lots = []
        for parking in parking_lots:
            if city in parking[3]:
                filtered_parking_lots.append(parking)
        parking_lots = filtered_parking_lots
    return parking_lots


def get_all_parking_lots_with_levels_and_places():
    query = """
            SELECT p.id, p.name, p.description, l.id, l.name, pl.id, pl.status
            FROM parkings p
                JOIN levels l on p.id = l.parking_id
                JOIN places pl on l.id = pl.level_id
            """

    with DatabaseConnection() as connection:
        parking_aggregated_data = connection.cursor.execute(query).fetchall()
    return parking_aggregated_data


def make_aggregated_parking_data_dictionary(data):
    parking_lots = []
    levels = []
    places = []

    for parking_id, parking_name, parking_description, _, _, _, _ in data:
        parking = {
            "id": parking_id,
            "name": parking_name,
            "description": parking_description,
            "levels": []
        }
        if parking not in parking_lots:
            parking_lots.append(parking)

    for parking_id, _, _, level_id, level_name, _, _ in data:
        level = {
            "id": level_id,
            "name": level_name,
            "places": [],
            "parking_id": parking_id
        }
        if level not in levels:
            levels.append(level)

    for _, _, _, level_id, _, place_id, place_status in data:
        place = {
            "id": place_id,
            "status": place_status,
            "level_id": level_id
        }
        if place not in places:
            places.append(place)

    for level in levels:
        level["places"] = [place for place in places if place["level_id"] == level["id"]]

    for parking in parking_lots:
        parking["levels"] = [level for level in levels if level["parking_id"] == parking["id"]]

    return parking_lots


def count_free_places_for_each_parking():
    query = """
                SELECT p.name, COUNT(pl.id)
                FROM parkings p
                    JOIN levels l on p.id = l.parking_id
                    JOIN places pl on l.id = pl.level_id
                WHERE pl.status = 0
                GROUP BY p.name
                """

    with DatabaseConnection() as connection:
        result = connection.cursor.execute(query).fetchall()
    return [{"name": parking_name, "free_places": free_places} for parking_name, free_places in result]


def count_all_places_for_parking(parking_id: int):
    query = """
                SELECT COUNT(pl.id)
                FROM parkings p
                    JOIN levels l on p.id = l.parking_id
                    JOIN places pl on l.id = pl.level_id
                WHERE p.id = ?
                """

    with DatabaseConnection() as connection:
        result = connection.cursor.execute(query, (parking_id,)).fetchone()
    return result[0] if result is not None else None


def count_free_places_for_parking(parking_id: int):
    query = """
                SELECT COUNT(pl.id)
                FROM parkings p
                    JOIN levels l on p.id = l.parking_id
                    JOIN places pl on l.id = pl.level_id
                WHERE pl.status = 0 AND p.id = ?
                """

    with DatabaseConnection() as connection:
        result = connection.cursor.execute(query, (parking_id,)).fetchone()
    return result[0] if result is not None else None


def get_all_cars(parking_id: int):
    query = """
            SELECT ph.car_id, ph.place_id, c.preferred_battery_percent
            FROM parkings p
                JOIN levels l on p.id = l.parking_id
                JOIN places pl on l.id = pl.level_id
                JOIN parking_history ph on pl.id = ph.place_id
                JOIN cars c on c.id = ph.car_id
            WHERE p.id = ? AND ph.end_time IS NULL
            """
    with DatabaseConnection() as connection:
        result = connection.cursor.execute(query, (parking_id,)).fetchall()
    return result


def convert_file_to_binary(filename: str):
    with open(filename, 'rb') as file:
        blob = file.read()
    return blob


def update_parking_binary_photo(parking_id: int, binary: bytes):
    with DatabaseConnection() as connection:
        connection.cursor.execute(f'UPDATE parkings SET image = ? WHERE id = ?', (binary, parking_id))


def db_get_parking_image(parking_id: int):
    with DatabaseConnection() as connection:
        db_result = connection.cursor.execute(f'SELECT image FROM parkings p WHERE id = ?', (parking_id,)).fetchone()
    if db_result is not None:
        return db_result[0]
    else:
        return None
