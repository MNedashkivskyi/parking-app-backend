from fastapi.testclient import TestClient
import requests

from src.api.main import app

client = TestClient(app)


def test_get_places():
    response = client.get("/places?parking_id=0")
    assert response.status_code == 200
    assert response.json() == {'places': [{'id': 0, 'level': 0, 'status': 0}, {'id': 1, 'level': 0, 'status': 1}, {'id': 2, 'level': 0, 'status': 2}, {'id': 3, 'level': 0, 'status': 0}, {'id': 4, 'level': 1, 'status': 1}, {'id': 5, 'level': 1, 'status': 2}, {'id': 6, 'level': 1, 'status': 0}, {'id': 7, 'level': 1, 'status': 1}]}

def test_get_place_status():
    response = client.get("/places/0")
    assert response.status_code == 200
    assert response.json() == {'status': 0}

def test_put_place_occupy_1():
    requests.post("http://0.0.0.0:9091/car?place_id=1", json={
        "battery_status": 20.05,
        "battery_volume": 50 * 60 * 1000,
        "charging_speed": 10
    })
    response = client.put("/places/occupy?id=1&car=1")
    assert response.status_code == 200

def test_put_place_occupy_2():
    response = client.put("/places/occupy?id=1&car=1")
    assert response.status_code == 409

def test_put_place_free_1():
    requests.delete("http://0.0.0.0:9091/car?place_id=1")
    response = client.put("/places/free?id=1&car=1")
    assert response.status_code == 200

def test_put_place_free_2():
    response = client.put("/places/free?id=1&car=1")
    assert response.status_code == 409

def test_put_place_reserve_1():
    response = client.put("/places/reserve?id=1&car=1")
    assert response.status_code == 200

def test_put_place_reserve_2():
    response = client.put("/places/reserve?id=1&car=1")
    assert response.status_code == 409
