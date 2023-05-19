import random

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from fastapi.testclient import TestClient

from pet_store.main import app
from pet_store.db import Base, get_db
from .utils import seed_species

SQLALCHEMY_DATABASE_URL = "sqlite:///pet_store_test.db"


@pytest.fixture(scope="session")
def connection():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    return engine.connect()


@pytest.fixture(scope="session")
def client(connection):
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
    )

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="session")
def setup_database(connection):
    Base.metadata.create_all(bind=connection)
    yield
    Base.metadata.drop_all(bind=connection)


@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin_nested()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()


@pytest.fixture
def species(db_session):
    return random.choice(seed_species(db_session))
