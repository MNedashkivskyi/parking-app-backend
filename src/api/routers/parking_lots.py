from fastapi import APIRouter, status
from typing import Optional
from fastapi.responses import Response, StreamingResponse
from io import BytesIO

from src.api.resources.parking_lots import get_all_parking_lots, db_get_parking_image

router = APIRouter()


@router.get("")
def get_parking_lots(city: Optional[str] = None):
    parking_lots = get_all_parking_lots(city)
    parking_lots_response = [
        {
            "id": r_index,
            "name": r_parking_name,
            "description": r_parking_description,
            "free_places": r_free_places_qty,
            "address": f"{r_street}, {r_city} ({r_postal_code})",
            "image_url": r_img
        } for r_index, r_parking_name, r_parking_description, r_city, r_street, r_postal_code, r_img, r_free_places_qty
        in parking_lots
    ]
    return {"parking_lots": parking_lots_response}


# @router.get('/image/{parking_id}')
# def get_parking_image(parking_id: int, response: Response):
#     bytes_image = db_get_parking_image(parking_id)
#     if bytes_image is not None:
#         response.status_code = status.HTTP_200_OK
#         return StreamingResponse(BytesIO(bytes_image), media_type="image/jpg")
#     else:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": "There is no parking with such id."}
