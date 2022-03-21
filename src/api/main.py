from fastapi import FastAPI, Depends

from src.api.dependencies import authorize
from src.api.resources.parking_lots import make_aggregated_parking_data_dictionary
from src.api.resources.parking_lots import get_all_parking_lots_with_levels_and_places
from src.api.routers import places, parking_lots, auth, energy, cars, admin

app = FastAPI()
app.include_router(places.router, prefix="/places", tags=["places"], dependencies=[Depends(authorize)])
app.include_router(parking_lots.router, prefix="/parking_lots", tags=["parking_lots"], dependencies=[Depends(authorize)])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(energy.router, prefix="/energy", tags=["energy"], dependencies=[Depends(authorize)])
app.include_router(cars.router, prefix="/cars", tags=["cars"], dependencies=[Depends(authorize)])
app.include_router(admin.router, prefix="/admin", tags=["admin"], dependencies=[Depends(authorize)])


@app.get("/")
def hello_world():
    return {"message": "Hello World"}


# Its just for parking simulator, it's not a proper feature
@app.get("/all")
def get_parking():
    data = get_all_parking_lots_with_levels_and_places()
    r = make_aggregated_parking_data_dictionary(data)
    return {"parking_lots": r}
