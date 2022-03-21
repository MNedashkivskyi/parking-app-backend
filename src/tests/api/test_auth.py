from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_post_register_1():
    response = client.post("/auth/register", json={"username": "NowyTest", "password": "NowyTest", "mail": "nowy@gmail.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Registered successfully!", "id": 1}

def test_post_register_2():
    response = client.post("/auth/register", json={"username": "NowyTest", "password": "NowyTest", "mail": "nowy@gmail.com"})
    assert response.status_code == 409
    assert response.json() == {"message": "Could not register! Username already taken!"}

def test_post_login_1():
    response = client.post("/auth/login", json={"username": "NowyTest", "password": "NowyTest"})
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'message': 'Logged in successfully!', 'user_type': 'user'}

def test_post_login_2():
    response = client.post("/auth/login", json={"username": "InnyTest", "password": "ZłeHasło"})
    assert response.status_code == 401
    assert response.json() == {'message': 'Wrong username or password!'}

def test_post_reset():
    response = client.post("/auth/reset", json={"username": "NowyTest", "mail": "nowy@gmail.com"})
    assert response.status_code == 404
    assert response.json() == {"message": "Not implemented yet."}
