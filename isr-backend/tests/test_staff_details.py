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


def test_get_all_staff(db, client):
    
    request = client.get("/all-staff")
    data = request.json()

    assert request.status_code == 200, request.text
    assert len(data) == 10


def test_get_staff_roles(db, client):
    
    staff = models.StaffDetails(
        staff_id=20,
        staff_fname="Sammy",
        staff_lname="Doe",
        dept="IT",
        email="abc@gmail.com",
        phone="12345678",
        biz_address="123, ABC Street",
        sys_role="staff"
    )

    db.add(staff)

    staff_role1 = models.StaffRoles(
        staff_id=20,
        staff_role=1,
        role_type="primary",
        sr_status="active"
    )

    staff_role2 = models.StaffRoles(
        staff_id=20,
        staff_role=2,
        role_type="secondary",
        sr_status="inactive"
    )

    db.add(staff_role1)
    db.add(staff_role2)

    db.commit()

    request = client.get("/staff-roles/20")
    data = request.json()

    assert request.status_code == 200, request.text
    assert len(data) == 1
    assert data[0] == {
        "staff_id": 20,
        "staff_role": 1,
        "role_type": "primary",
        "sr_status": "active",
    }

    request = client.get("/staff-roles/1")

    assert request.status_code == 404, request.text
    


def test_get_staff_ro(db, client):
    staff = models.StaffDetails(
        staff_id=20,
        staff_fname="Sammy",
        staff_lname="Doe",
        dept="IT",
        email="abc@gmail.com",
        phone="12345678",
        biz_address="123, ABC Street",
        sys_role="staff",
    )

    db.add(staff)

    staff_ro = models.StaffReportingOfficer(
        staff_id=20,
        RO_id=1,
    )

    db.add(staff_ro)

    db.commit()

    request = client.get("/staff-ro/20")
    data = request.json()

    assert request.status_code == 200, request.text
    assert data == {
        "staff_id": 20,
        "RO_id": 1,
    }

    request = client.get("/staff-ro/1")
    assert request.status_code == 404, request.text


def test_get_staff_skills(db, client):
    staff = models.StaffDetails(
        staff_id=20,
        staff_fname="Sammy",
        staff_lname="Doe",
        dept="IT",
        email="abc@gmail.com",
        phone="12345678",
        biz_address="123, ABC Street",
        sys_role="staff",
    )

    staff_skill1 = models.StaffSkills(
        staff_id=20,
        skill_id=1,
        ss_status="active",
    )

    staff_skill4 = models.StaffSkills(
        staff_id=20,
        skill_id=4,
        ss_status="active",
    )

    db.add(staff)
    db.add(staff_skill1)
    db.add(staff_skill4)

    db.commit()


    request = client.get("/staff-skills/20")
    data = request.json()

    assert request.status_code == 200, request.text
    assert len(data) == 2


def test_get_staff_details(db, client):
    
    staff = models.StaffDetails(
        staff_id=20,
        staff_fname="Sammy",
        staff_lname="Doe",
        dept="IT",
        email="abc@gmail.com",
        phone="12345678",
        biz_address="123, ABC Street",
        sys_role="staff",
    )

    db.add(staff)

    db.commit()

    request = client.get("/staff?staff_email=abc@gmail.com")
    data = request.json()

    print(data)

    assert request.status_code == 200, request.text
    assert data == {
        "staff_id": 20,
        "staff_fname": "Sammy",
        "staff_lname": "Doe",
        "dept": "IT",
        "email": "abc@gmail.com",
        "phone": "12345678",
        "biz_address": "123, ABC Street",
        "sys_role": "staff"
    }

    request = client.get("/staff?staff_email=abcde@gmail.com")
    assert request.status_code == 404, request.text

    request = client.get("/staff")
    assert request.status_code == 422, request.text
    


def test_get_one_staff_details(db, client):
    staff = models.StaffDetails(
        staff_id=20,
        staff_fname="Sammy",
        staff_lname="Doe",
        dept="IT",
        email="abc@gmail.com",
        phone="12345678",
        biz_address="123, ABC Street",
        sys_role="staff",
    )

    db.add(staff)

    db.commit()

    request = client.get("/staff/20")
    data = request.json()

    print(data)

    assert request.status_code == 200, request.text
    assert data == {
        "staff_id": 20,
        "staff_fname": "Sammy",
        "staff_lname": "Doe",
        "dept": "IT",
        "email": "abc@gmail.com",
        "phone": "12345678",
        "biz_address": "123, ABC Street",
        "sys_role": "staff"
    }

    request = client.get("/staff/21")
    assert request.status_code == 404, request.text
