from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_get_admin_places():
    response = client.get("/admin/places?parking_id=0")
    assert response.status_code == 200
    assert response.json() == {"cars_amount": 5, "free_places": 37}

def test_get_admin_battery():
    response = client.get("/admin/battery?parking_id=0")
    assert response.status_code == 200
    assert response.json() == {"average_battery_status": 100.0, "charge_time": 0.0}

def test_get_admin_history():
    response = client.get("/admin/energy")
    assert response.status_code == 200
    assert len(response.json()["yesterday"]) == 1440
    assert len(response.json()["average"]) == 1440
    assert len(response.json()["charging"]) == 1440
    assert len(response.json()["discharging"]) == 1440

def test_get_admin_history():
    response = client.get("/admin/history")
    assert response.status_code == 200
    assert response.json() == "TODO: historia zarobków i strat"
