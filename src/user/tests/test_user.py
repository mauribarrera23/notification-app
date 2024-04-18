from src.user.models import User


def test_create_user():
    user = User(username="test_user", email="user@test.com", password="password")
    assert user.username == "test_user"
    assert user.email == "user@test.com"
    assert user.password == "password"
