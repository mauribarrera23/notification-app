from fastapi import status
from faker import Faker

from src.conftest import client, test_db
from src.user.tests.factories import UserFactory

fake = Faker()


def test_signup(test_db):
    signup_data = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": "password"
    }
    response = client.post("/user/signup", json=signup_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "User has been created"}


def test_login(test_db):
    user = UserFactory.create()
    login_data = {
        "username": user.username,
        "password": "password",
    }
    response = client.post("/user/login", json=login_data)
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response_json
    assert response_json["token_type"] == "bearer"
