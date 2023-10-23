from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.pool import StaticPool
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
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# def override_get_db():
#     connection = engine.connect()
#     transaction = connection.begin()
#     db = Session(bind=connection)
#     # db = Session(engine)

#     yield db

#     db.close()
#     transaction.rollback()
#     connection.close()


# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)


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

    # begin a non-ORM transaction
    transaction = connection.begin()
    # bind an individual Session to the connection
    db = Session(bind=connection)

    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


def test_create_listings(db, client):
    response = client.post(
        "/listing/create/",
        json={
            "role_id": 1,
            "role_listing_desc": "string",
            "role_listing_source": 1,
            "role_listing_open": "2023-09-23",
            "role_listing_close": "2023-12-12",
            "role_listing_id": 10,
            "role_listing_creator": 1,
        },
    )
    assert response.status_code == 200
    response2 = client.get("/listing/10")
    assert response2.status_code == 200


def test_get_all_listings(db, client):

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

    l2 = models.RoleListings(
        role_id=2,
        role_listing_desc="i love to write unit test",
        role_listing_source=1,
        role_listing_open="2023-10-12",
        role_listing_close="2024-12-12",
        role_listing_id=4,
        role_listing_ts_update=None,
        role_listing_creator=1,
    )

    db.add(l1)
    db.add(l2)
    db.commit()

    response = client.get("/listing/")
    data = response.json()

    assert response.status_code == 200, response.text
    assert len(data['items']) == 2


def test_get_all_listings_created_by_staff_id(db, client):

    staff_id = 1
    l1 = models.RoleListings(
        role_id=2,
        role_listing_desc="i love to write unit test",
        role_listing_source=1,
        role_listing_open="2023-10-26",
        role_listing_close="2024-12-12",
        role_listing_id=5,
        role_listing_ts_update=None,
        role_listing_creator=staff_id,
    )

    l2 = models.RoleListings(
        role_id=2,
        role_listing_desc="i love to write unit test",
        role_listing_source=1,
        role_listing_open="2023-10-26",
        role_listing_close="2024-12-12",
        role_listing_id=4,
        role_listing_ts_update=None,
        role_listing_creator=staff_id,
    )

    l3 = models.RoleListings(
        role_id=2,
        role_listing_desc="i love to write unit test",
        role_listing_source=1,
        role_listing_open="2023-10-26",
        role_listing_close="2024-12-12",
        role_listing_id=17,
        role_listing_ts_update=None,
        role_listing_creator=2,
    )
    
    db.add(l1)
    db.add(l2)
    db.add(l3)
    db.commit()

    response = client.get("/listing/created-by/1")
    data = response.json()

    assert response.status_code == 200, response.text
    assert len(data['items']) == 2


# def test_get_listing_by_id(db, client):
#     listing_to_insert = models.RoleListings(
#         role_id=2,
#         role_listing_desc="i love to write unit test",
#         role_listing_source=1,
#         role_listing_open="2023-10-26",
#         role_listing_close="2024-12-12",
#         role_listing_id=999,
#         role_listing_ts_create = func.now(),
#         role_listing_ts_update = None,
#         role_listing_creator=1,
#         role_listing_status = "active"
#     )

#     # Add the data to the database
#     db.add(listing_to_insert)
#     db.commit()  # Commit the changes

#     response = client.get("/listing/999")
#     response2 = client.get("/listing/")
#     print("++++++++++++++++++++++++++++")
#     print(response2.json())
#     assert response.status_code == 200, response.text
