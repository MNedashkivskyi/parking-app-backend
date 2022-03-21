from requests import get, post

BASE_MOCK_URL = "http://localhost:9091/"


def get_real_battery_status(place_id: int):
    return get(BASE_MOCK_URL + "status", params={"place_id": place_id}).json()


def get_real_battery_volume(place_id: int):
    return get(BASE_MOCK_URL + "volume", params={"place_id": place_id}).json()


def get_real_charging_speed(place_id: int):
    return get(BASE_MOCK_URL + "charging", params={"place_id": place_id}).json()


def set_real_charging_speed(place_id: int, speed: int, minimum: float):
    return post(BASE_MOCK_URL, params={"place_id": place_id, "speed": speed, "minimum": minimum})
