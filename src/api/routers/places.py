from typing import Optional
from fastapi import APIRouter, Response, status
from datetime import datetime

from src.api.resources.places import get_all_places, get_parking_places, get_place_status, do_occupy_place, do_free_place, do_reserve_place
from src.api.resources.parking_history import db_initialize_record, db_add_end_to_record
from src.api.resources.charger import get_real_battery_status, get_real_battery_volume, get_real_charging_speed
from src.api.resources.cars import db_set_car_battery, db_is_car_battery_null


router = APIRouter()

FREE = 0
RESERVED = 1
OCCUPIED = 2


@router.get("/")
def get_places(parking_id: Optional[int] = None):
    if parking_id is None:
        places = get_all_places()
    else:
        places = get_parking_places(parking_id)
    places_response = [
        {
            "id": r_index,
            "status": r_place_status,
            "level": r_level
        } for r_index, r_place_status, r_level in places
    ]
    return {"places": places_response}


@router.get("/{place_id}")
def place_status(place_id: int):
    return {"status": get_place_status(place_id)}


@router.put("/occupy")
def occupy_place(id: int, car: int, response: Response):
    current_status = get_place_status(id)
    if current_status == RESERVED:
        db_initialize_record(id, car, str(datetime.now()), get_real_battery_status(id), get_real_charging_speed(id))
        if (db_is_car_battery_null(car)):
            db_set_car_battery(car, get_real_battery_volume(id))
        r = do_occupy_place(id)
        response.status_code = status.HTTP_200_OK
        return {"message": "Place successfully occupied!"}
    else:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "Couldn't occupy the place"}


@router.put("/free")
def free_place(id: int, response: Response):
    current_status = get_place_status(id)
    if current_status == OCCUPIED:
        db_add_end_to_record(id, str(datetime.now()), get_real_battery_status(id))
        r = do_free_place(id)
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_409_CONFLICT
    return


@router.put("/reserve")
def reserve_place(id: int, response: Response):
    current_status = get_place_status(id)
    if current_status == FREE:
        r = do_reserve_place(id)
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_409_CONFLICT
    return
