from datetime import datetime

from src.api.resources.cars import db_get_car_battery
from src.api.resources.charger import get_real_battery_status, get_real_battery_volume, get_real_charging_speed
from src.api.resources.parking_history import db_get_place, db_get_battery_status
from src.utils.database_connection import TIME_FORMAT


def __get_charge_time(battery_volume, charging_speed, current_battery_status, desired_battery_status):
    return (desired_battery_status - current_battery_status) / 100 * battery_volume // charging_speed


def __get_current_battery_percent_estimate(battery_volume, charging_speed, start_time, start_battery_status):
    time_passed = datetime.now() - datetime.strptime(start_time, TIME_FORMAT)
    time_passed = int(time_passed.total_seconds()) // 60
    return min(max(start_battery_status + time_passed * (charging_speed / battery_volume), 0.0), 100.0)


def get_real_charge_time(car_id: int, desired_battery_status: int = 100.0, place_id=None):
    if place_id is None:
        place_id = db_get_place(car_id)
    return __get_charge_time(get_real_battery_volume(place_id), get_real_charging_speed(place_id), get_real_battery_status(place_id), desired_battery_status)


def get_estimate_charge_time(car_id: int, desired_battery_status: int = 100.0):
    battery_volume = db_get_car_battery(car_id)
    start_time, battery_on_start, charging_speed = db_get_battery_status(car_id)
    current_battery_status = __get_current_battery_percent_estimate(battery_volume, charging_speed, start_time, battery_on_start)
    return __get_charge_time(battery_volume, charging_speed, current_battery_status, desired_battery_status)


def get_battery_status(car_id: int):
    start_time, battery_on_start, charging_speed = db_get_battery_status(car_id)
    if charging_speed is None:
        return battery_on_start, None
    else:
        battery = __get_current_battery_percent_estimate(db_get_car_battery(car_id), charging_speed, start_time, battery_on_start)
        return battery, charging_speed
