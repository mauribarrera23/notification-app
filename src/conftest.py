import pytest

from factory.alchemy import SQLAlchemyModelFactory
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.main import app
from src.settings.database import Base, get_db_session

SQLALCHEMY_DATABASE_URL = "sqlite:///./testing_db.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class BaseModelFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = TestingSessionLocal
        sqlalchemy_session_persistence = 'commit'


app.dependency_overrides[get_db_session] = override_get_db

client = TestClient(app)
