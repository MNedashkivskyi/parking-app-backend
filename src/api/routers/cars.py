from fastapi import APIRouter, status, Response, Depends
from pydantic import BaseModel

from api.dependencies import obtain_user_id
from src.api.resources.cars import db_delete_car, db_get_cars, db_save_car, db_get_preffered_car_battery, \
    db_set_preferred_car_battery, db_get_car_owner
from src.api.resources.places import db_get_name_of_parking_and_level
from src.api.resources.parking_history import db_get_place
from src.api.domain.battery import get_battery_status, get_estimate_charge_time

router = APIRouter()


class AddCarRequest(BaseModel):
    manufacturer: str
    model: str
    registration_number: str


class DeleteCarRequest(BaseModel):
    registration_number: str


class CarPreferencesRequest(BaseModel):
    preferred_battery_percent: float


@router.get("")
def get_cars(owner_id: int = Depends(obtain_user_id)):
    # zl / W
    UNREGISTERED_COST = 0.0000010
    UNDER_PREFFERED_COST = 0.0000008
    OVER_PREFFERED_COST = 0.0000007

    cars = db_get_cars(owner_id)
    response = []
    for r_id, r_manufacturer, r_model, r_registration_number, r_preferred_battery_percent, r_battery_volume in cars:
        place_id = db_get_place(r_id)
        if place_id is not None:
            parking_id, parking_name, level_name = db_get_name_of_parking_and_level(place_id)
            battery_percent, charging_speed = get_battery_status(r_id)
            time_to_preffered = get_estimate_charge_time(r_id, r_preferred_battery_percent)
            time_to_full = get_estimate_charge_time(r_id, 100.0)
            cost_to_preffered = max(0, (r_preferred_battery_percent - battery_percent)) * r_battery_volume * UNDER_PREFFERED_COST
            cost_to_full = cost_to_preffered + max(0, (100.0 - (r_preferred_battery_percent if cost_to_preffered > 0.0 else battery_percent))) * r_battery_volume * OVER_PREFFERED_COST
        response.append(
            {
                "id": r_id,
                "manufacturer": r_manufacturer,
                "model": r_model,
                "registration_number": r_registration_number,
                "preferred_battery_percent": r_preferred_battery_percent,
                "charging_info": {
                    "battery_status": battery_percent,
                    "charging_status": charging_speed,
                    "place_id": place_id,
                    "parking_id": parking_id,
                    "parking_name": parking_name,
                    "level_name": level_name,
                    "time_to_preffered": time_to_preffered,
                    "time_to_full": time_to_full,
                    "cost_to_preffered": cost_to_preffered,
                    "cost_to_full": cost_to_full
                } if place_id is not None else None
            }
        )
    return response


@router.get("/info")
def get_status(id: int):
    place = db_get_place(id)
    if place is not None:
        battery_percent, charging_speed = get_battery_status(id)
    return {
        "battery_status": battery_percent if place is not None else None,
        "charging_status": charging_speed if place is not None else None
    }


@router.get("/preferences")
def get_preferences(id: int):
    return {
        "preferred_battery_percent": db_get_preffered_car_battery(id)
    }


@router.post("/preferences")
def set_preferences(id: int, request: CarPreferencesRequest):
    db_set_preferred_car_battery(id, request.preferred_battery_percent)
    return Response()


@router.post("")
def add_car(request: AddCarRequest, response: Response, owner_id: int = Depends(obtain_user_id)):
    if db_save_car(owner_id, request.manufacturer, request.model, request.registration_number):
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Car added successfully!"}
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Something went wrong, car could not be added"}


@router.delete("")
def delete_car(request: DeleteCarRequest, response: Response, owner_id: int = Depends(obtain_user_id)):
    registration_number = request.registration_number
    if db_get_car_owner(registration_number) != owner_id:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "You do not have permission to delete this car."}
    if db_delete_car(registration_number):
        response.status_code = status.HTTP_202_ACCEPTED
        return {"message": "Car deleted successfully!"}
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Something went wrong, car could not be deleted"}
