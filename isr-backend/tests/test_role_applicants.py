from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
import os
import models
import pytest

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


def test_get_all_applicants(db, client):

    # No applicants record
    response = client.get("/applicants")
    data = response.json()

    assert response.status_code == 404, response.text
    assert data["detail"] == "No applicants found"

    # Insert 1 RoleListing and 2 RoleApplications (Expecting 2 items)
    l1 = models.RoleListings(
        role_id=2,
        role_listing_desc="i love to write unit test",
        role_listing_source=1,
        role_listing_open="2023-10-24",
        role_listing_close="2024-12-12",
        role_listing_id=5,
        role_listing_ts_update=None,
        role_listing_creator=1,
    )

    app1 = models.RoleApplications(
        role_listing_id=5,
        staff_id=1,
        role_app_status="applied"
    )

    app2 = models.RoleApplications(
        role_listing_id=5,
        staff_id=2,
        role_app_status="applied"
    )

    db.add(l1)
    db.add(app1)
    db.add(app2)

    db.commit()

    response = client.get("/applicants")
    data = response.json()

    assert response.status_code == 200, response.text
    assert len(data["items"]) == 2


def test_get_applicants(db, client):

    # Insert 1 RoleListing and 2 RoleApplications (Expecting 1 item with role_app_id=1)
    l1 = models.RoleListings(
        role_id=2,
        role_listing_desc="i love to write unit test",
        role_listing_source=1,
        role_listing_open="2023-10-24",
        role_listing_close="2024-12-12",
        role_listing_id=5,
        role_listing_ts_update=None,
        role_listing_creator=1,
    )

    app1 = models.RoleApplications(
        role_app_id = 1,
        role_listing_id=5,
        staff_id=1,
        role_app_status="applied"
    )

    app2 = models.RoleApplications(
        role_app_id = 2,
        role_listing_id=5,
        staff_id=2,
        role_app_status="applied"
    )

    db.add(l1)
    db.add(app1)
    db.add(app2)

    db.commit()

    # Listing ID 5
    response = client.get("/applicants/5")
    data = response.json()

    assert response.status_code == 200, response.text
    assert len(data["items"]) == 2


def test_create_application(db, client):

    l1 = models.RoleListings(
        role_id=2,
        role_listing_desc="i love to write unit test",
        role_listing_source=1,
        role_listing_open="2023-10-24",
        role_listing_close="2024-12-12",
        role_listing_id=5,
        role_listing_ts_update=None,
        role_listing_creator=1,
    )

    app1 = models.RoleApplications(
        role_app_id = 1,
        role_listing_id=5,
        staff_id=1,
        role_app_status="applied"
    )

    db.add(l1)
    db.add(app1)

    db.commit()

    # Insert Role Application with role_listing_id=5 and staff_id=1 (Expecting 409)
    response = client.post("/applicants/create", json={
        "role_listing_id": 5,
        "staff_id": 1
    })

    assert response.status_code == 409, response.text
    assert response.json()["detail"] == "Application already exists"


    # Insert Role Application with role_listing_id=5 and staff_id=2 (Expecting 200)
    response = client.post("/applicants/create", json={
        "role_listing_id": 5,
        "staff_id": 2
    })

    assert response.status_code == 200, response.text
    assert response.json()["message"] == "Application created"

    # Insert Role Application with role_listing_id=6 and staff_id=2 (Expecting 500, role_listing_id=6 does not exist)
    response = client.post("/applicants/create", json={
        "role_listing_id": 6,
        "staff_id": 2
    })

    assert response.status_code == 500, response.text
