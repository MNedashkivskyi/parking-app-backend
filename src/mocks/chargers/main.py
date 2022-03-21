from os import environ
from sys import path
import uvicorn
import requests
from fastapi import FastAPI
from fastapi.responses import Response
from threading import Thread
from time import sleep
from pydantic import BaseModel
from numpy.random import normal, randint

MAIN_API_URL = "http://localhost:8080"
environ['MODE'] = 'PROD'
path.append('.')

from src.api.resources.auth import start_session

class AddCarRequest(BaseModel):
    battery_status: float
    battery_volume: int
    charging_speed: int


app = FastAPI()
app.chargers = {}
cookies = {"SESSION_TOKEN": start_session(2678400)}
for place in requests.get(f"{MAIN_API_URL}/places", cookies=cookies).json()["places"]:
    is_free = place['status'] == 0
    app.chargers[place['id']] = {
        "battery_status": normal(loc=50.0, scale=25.0) if not is_free else None,
        "battery_volume": randint(20, 100) * 60 * 1000 if not is_free else None,  # kWh -> Wmin, TODO this should not have to be randint
        "charging_speed": randint(5, 100) if not is_free else None,
        "minimum": 0
    }


@app.get("/status")
def get_battery_status(place_id: int):
    return app.chargers[place_id]["battery_status"]


@app.get("/volume")
def get_battery_volume(place_id: int):
    return app.chargers[place_id]["battery_volume"]


@app.get("/charging")
def get_charging_speed(place_id: int):
    return app.chargers[place_id]["charging_speed"]


@app.post("/")
def post_charging_speed(place_id: int, speed: int, minimum: float):
    app.chargers[place_id]["charging_speed"] = speed
    app.chargers[place_id]["minimun"] = minimum
    return Response()


@app.post("/car")
def post_car(place_id: int, request: AddCarRequest):
    app.chargers[place_id]["battery_status"] = request.battery_status
    app.chargers[place_id]["battery_volume"] = request.battery_volume
    app.chargers[place_id]["charging_speed"] = request.charging_speed


@app.delete("/car")
def delete_car(place_id: int):
    app.chargers[place_id]["battery_status"] = None
    app.chargers[place_id]["battery_volume"] = None
    app.chargers[place_id]["charging_speed"] = None


def charge():
    while True:
        for _, charger in app.chargers.items():
            if charger["battery_status"] is not None and charger["battery_volume"] is not None and charger["charging_speed"] is not None:
                charger["battery_status"] += charger["charging_speed"] / charger["battery_volume"]
                if charger["battery_status"] <= charger["minimum"]:
                    charger["battery_status"] = charger["minimum"]
                    charger["charging_speed"] = 0
                if charger["battery_status"] >= 100:
                    charger["battery_status"] = 100
                    charger["charging_speed"] = 0
        sleep(60)


if __name__ == "__main__":
    Thread(target=charge, daemon=True).start()
    uvicorn.run("main:app", host="0.0.0.0", port=9091, log_level="info", reload=False)
