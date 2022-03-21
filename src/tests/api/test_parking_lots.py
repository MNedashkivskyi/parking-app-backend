from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_get_parking_lots():
    response = client.get("/parking_lots?city=Warszawa")
    assert response.status_code == 200
    assert response.json() == {"parking_lots": [{
            "id": 0,
            "name": "Parking 0",
            "description": "Opis 0",
            "free_places": 3,
            "address": "Nowowiejska 15/19, Warszawa (00-665)",
            "image_url": "https://images.pexels.com/photos/1756957/pexels-photo-1756957.jpeg?cs=srgb&dl=pexels-brett-sayles-1756957.jpg&fm=jpg"
        }]}

# def test_get_parking_lots_image_1():
#     response = client.get("/parking_lots/image/0")
#     assert response.status_code == 200
#     assert response.json() == b''

# def test_get_parking_lots_image_2():
#     response = client.get("/parking_lots/image/3")
#     assert response.status_code == 404
#     assert response.json() == {"message": "There is no parking with such id."}
