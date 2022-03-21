from os import environ
import requests

environ['MODE'] = 'TEST'

from src.utils.database_connection import DatabaseConnection, get_project_root

with open(get_project_root() + '/src/utils/db_ddl.sql', 'r') as ddl:
    with open(get_project_root() + '/src/utils/db_dml.sql', 'r') as dml:
        with DatabaseConnection() as connection:
            connection.cursor.executescript(ddl.read())
            connection.cursor.executescript(dml.read())

requests.post("http://0.0.0.0:9091/car?place_id=0", json={
    "battery_status": 20.05,
    "battery_volume": 50 * 60 * 1000,
    "charging_speed": 10
})