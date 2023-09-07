import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import Base, User


@pytest.fixture
def client(session):
    def get_session_overwrites():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_overwrites

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    _session = sessionmaker(engine)

    yield _session()

    Base.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(username='test', email='test@test.com', password='testtest')

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
