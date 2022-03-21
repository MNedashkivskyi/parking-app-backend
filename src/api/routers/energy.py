from datetime import datetime
from fastapi import APIRouter

from src.api.domain.battery import get_battery_status
from src.api.resources.cars import db_get_car_battery
from src.api.resources.charger import get_real_battery_status, set_real_charging_speed
from src.api.domain.energy import format_data, profitability
from src.api.resources.energy_history import db_save_post
from src.api.resources.parking_history import db_add_end_to_record, db_get_place, db_initialize_record
from src.api.resources.parking_lots import get_all_cars, get_all_parking_lot_ids


router = APIRouter()


def adjust_charging_speeds(value: float):
    def change_charging_speed(car_id: int, speed: int, minimum: float):
        # can be negative, positive, or zero, but has to be in Watts
        place_id = db_get_place(car_id)
        db_add_end_to_record(place_id, str(datetime.now()), get_real_battery_status(place_id))
        set_real_charging_speed(place_id, speed, minimum)
        db_initialize_record(place_id, car_id, str(datetime.now()), get_real_battery_status(place_id), speed)

    CHARGE_SPEED = 60 * 1000 * 10 # kWh -> Wmin

    now = datetime.now()
    minute = int((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()) // 60
    charging, discharging = profitability(*format_data())
    
    parking_lots = get_all_parking_lot_ids()
    cars = []
    for id in parking_lots:
        cars.append(get_all_cars(id))
    cars = [item for sublist in cars for item in sublist]

    # sell if electricity is expensive
    if discharging[minute] >= 0.8:
        present_cars = []
        for car in cars:
            battery_status, _ = get_battery_status(car[0])
            available_energy = battery_status * db_get_car_battery(car[0])
            present_cars.append([car[0], available_energy, car[2]])
        for id, energy, minimum in present_cars:
            if energy > 0:
                change_charging_speed(id, -CHARGE_SPEED, minimum)
        return min(value, max(0, sum([car[1] for car in present_cars])))
    else:
        # buy if electricity is cheap
        if charging[minute] >= 0.5:
            for car in cars:
                change_charging_speed(car[0], CHARGE_SPEED, car[2])
        # else don't
        else:
            for car in cars:
                change_charging_speed(car[0], 0, car[2])
        return 0


@router.post("")
def post_energy(value: float):
    db_save_post(value)
    return {"Watts": adjust_charging_speeds(value * 1000000000)} # W -> GW
