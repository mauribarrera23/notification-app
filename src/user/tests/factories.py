from factory import lazy_attribute
from faker import Faker

from src.conftest import BaseModelFactory, TestingSessionLocal
from src.user.models import User

FAKER = Faker(locale='es_ES')


class UserFactory(BaseModelFactory):
    class Meta:
        model = User

    username = lazy_attribute(lambda x: FAKER.user_name())
    email = lazy_attribute(lambda x: FAKER.email())
    password = "password"

    @classmethod
    def create(cls, **kwargs):
        db = TestingSessionLocal()
        try:
            user = super().create(**kwargs)
            user.hash_password(user.password)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        finally:
            db.close()
