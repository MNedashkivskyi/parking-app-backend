import requests
import uvicorn
from os import environ
from sys import path
from numpy.random import normal, randint
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

MAIN_API_URL = "http://localhost:8080"
CHARGER_API_URL = "http://localhost:9091"
environ['MODE'] = 'PROD'
path.append('.')

from src.api.resources.auth import start_session

cookies = {"SESSION_TOKEN": start_session(2678400)}

app = FastAPI()
templates = Jinja2Templates(directory="src/mocks/parking-simulator/templates")
app.mount("/static", StaticFiles(directory="src/mocks/parking-simulator/static"), name="static")


def add_car_to_mock(id: int, volume=randint(20, 100)):
    requests.post(f"{CHARGER_API_URL}/car", params={"place_id": id}, cookies=cookies, json={
        "battery_status": normal(loc=50.0, scale=25.0),
        "battery_volume": volume * 60 * 1000,  # kWh -> Wmin
        "charging_speed": randint(5, 100),
        "minimum": 0
        })


def remove_car_from_mock(id: int):
    requests.delete(f"{CHARGER_API_URL}/car", params={"place_id": id}, cookies=cookies)


@app.get("/")
def root(req: Request):
    data = get_parking()
    return templates.TemplateResponse(
        "index.html.j2",
        {"request": req, "parking_lots": data["parking_lots"]}
    )


@app.get("/free")
def free(id: int):
    requests.put(f"{MAIN_API_URL}/places/free", params={"id": id}, cookies=cookies)
    remove_car_from_mock(id)
    return RedirectResponse("/")


@app.get("/reserve")
def reserve(id: int, battery: int):
    requests.put(f"{MAIN_API_URL}/places/reserve", params={"id": id}, cookies=cookies)
    add_car_to_mock(id, battery)
    return RedirectResponse("/")


def get_parking():
    parking_data = requests.get(f"{MAIN_API_URL}/all", cookies=cookies).json()
    print(parking_data)
    return parking_data


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=9090, log_level="info", reload=True)
