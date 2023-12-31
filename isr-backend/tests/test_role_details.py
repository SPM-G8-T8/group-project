from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
import os
import pytest

import models

from database import Base
from main import app, get_db

DB_URI = os.environ["DB_URI"]
SQLALCHEMY_DATABASE_URL = DB_URI[:-3] + "test"


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    connection.begin()
    db = Session(bind=connection)

    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c


def test_get_all_roles(db, client):
    request = client.get("/roles")
    data = request.json()

    assert request.status_code == 200, request.text
    assert len(data) == 10

def test_get_roles(db, client):

    role = models.RoleDetails(
        role_id=11,
        role_name="Data Analyst",
        role_status="active",
    )

    db.add(role)

    db.commit()

    request = client.get("/roles/11")
    data = request.json()

    assert request.status_code == 200, request.text
    assert data["role_id"] == 11
    assert data["role_name"] == "Data Analyst"
    assert data["role_status"] == "active"
