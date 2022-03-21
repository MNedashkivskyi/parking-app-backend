from os import environ
from sys import path
from requests import post
from datetime import datetime
from math import pi, sin
from time import sleep
from src.api.resources.auth import start_session

MAIN_API_URL = "http://0.0.0.0:8080"
WAIT_SECONDS = 15
environ['MODE'] = 'PROD'
path.append('.')


cookies = {"SESSION_TOKEN": start_session(2678400)}


def energy_demand_function(x: float):
    return -sin((0.00225 * x + 0.5) ** 2 + pi / 4) + 3 * sin(((0.00229 * x + 0.3) / 3.6) ** 3 * pi) + 16


if __name__ == "__main__":
    while True:
        now = datetime.now()
        minute = int((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()) // 60
        post(f"{MAIN_API_URL}/energy", params={"value": energy_demand_function(minute)}, cookies=cookies)
        sleep(WAIT_SECONDS)
