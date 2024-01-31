import json
from fastapi.testclient import TestClient
from .app.main import app

client = TestClient(app)

# Test the read_main endpoint
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


# Test the login endpoint
def test_login():
    # Assuming you have a valid user in your database for testing
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


# Test the create_user endpoint
def test_create_user():
    user_data = {
        "name": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword",
    }
    response = client.post("/api/create-user", json=user_data)
    assert response.status_code == 200
    assert response.json()["name"] == "newuser"


# Test the list_users endpoint
def test_list_users():
    response = client.get("/api/get-all-users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Similarly, you can write tests for other endpoints such as create_goal, list_goals, create_step, list_steps, etc.
