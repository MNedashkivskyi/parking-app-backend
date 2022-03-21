from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_get_cars():
    response = client.get("/cars?owner=1")
    assert response.status_code == 200
    assert response.json() == [{'id': 3, 'manufacturer': 'Ferrari', 'model': 'LaFerrari', 'registration_number': 'W0 TEST3', "preferred_battery_percent": 20.0,'charging_info': None}]

def test_get_cars_info():
    response = client.get("/cars/info?id=0")
    assert response.status_code == 200
    assert response.json() == {"battery_status": 100.0, "charging_status": 600000}

def test_post_cars():
    response = client.post("/cars", json={"owner_id": 0, "manufacturer": "FIAT", "model": "500", "registration_number": "WO 500FI"})
    assert response.status_code == 201

def test_delete_cars():
    response = client.delete("/cars", json={"registration_number": "WO 500FI"})
    assert response.status_code == 202

def test_post_cars_preferences():
    response = client.post("/cars/preferences?id=0", json={"preferred_battery_percent": 50.0})
    assert response.status_code == 200

def test_get_cars_preferences():
    response = client.get("/cars/preferences?id=0")
    assert response.status_code == 200
    assert response.json() == {"preferred_battery_percent": 50.0}