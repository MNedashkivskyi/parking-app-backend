from fastapi import APIRouter

from src.api.resources.charger import get_real_battery_status
from src.api.resources.parking_lots import count_all_places_for_parking, count_free_places_for_parking, get_all_cars
from src.api.domain.battery import get_real_charge_time
from src.api.domain.battery import get_estimate_charge_time, get_battery_status
from src.api.domain.energy import format_data, profitability

router = APIRouter()


@router.get("/places")
def places(parking_id: int):
    free, all = count_free_places_for_parking(parking_id), count_all_places_for_parking(parking_id)
    return {
        "cars_amount": all - free,
        "free_places": free * 100 // all
    }

@router.get("/battery")
def battery(parking_id: int):
    cars = {}
    for car_id, place_id, _ in get_all_cars(parking_id):
        # cars[car_id] = tuple([get_battery_status(place_id), get_estimate_charge_time(car_id, place_id=place_id)])
        cars[car_id] = tuple([get_battery_status(car_id)[0], get_estimate_charge_time(car_id)])
    percent = [car[0] for car in cars.values()]
    percent = (sum(percent) // len(percent)) if len(percent) != 0 else None
    time = [car[1] for car in cars.values()]
    time = max(time) if len(time) != 0 else None
    return {
        "average_battery_status": percent,
        "charge_time": time
    }

@router.get("/energy")
def get():
    data = {}

    x = [i for i in range(1440)]
    values, average = format_data()

    data["yesterday"] = [x, values]
    data["average"] = [x, average]

    charging, discharging = profitability(values, average)

    data["charging"] = [x, charging]
    data["discharging"] = [x, discharging]

    return data

@router.get("/history")
def history():
    return "TODO: historia zarobków i strat"
