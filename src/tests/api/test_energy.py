from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_post_energy():
    response = client.post("/energy?value=0")
    assert response.status_code == 200
