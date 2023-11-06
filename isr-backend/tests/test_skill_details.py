import json
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


def test_update_skill_name_positive(client):
    skill_id = 1  # Valid skill_id
    new_name = "New Programming Skill Name"
    old_status = "active"  # The existing status before update
    request_body = {"skill_name": new_name, "skill_status": old_status}
    print(json.dumps(request_body))
    response = client.put(f"/skills/editSkill/{skill_id}", json=request_body)
    print("----response----")
    print(json.dumps(response.json()))
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "message": "Skill updated",
        "skill": {
            "skill_id": skill_id,
            "skill_name": new_name,
            "skill_status": old_status,
        },
    }


def test_update_skill_status_positive(client):
    skill_id = 1  # Valid skill_id
    new_status = "inactive"
    old_name = "Programming"  # The existing skill name before update
    request_body = {"skill_name": old_name, "skill_status": new_status}
    print(json.dumps(request_body))
    response = client.put(f"/skills/editSkill/{skill_id}", json=request_body)
    print("----response----")
    print(json.dumps(response.json()))
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "message": "Skill updated",
        "skill": {
            "skill_id": skill_id,
            "skill_name": old_name,
            "skill_status": new_status,
        },
    }


def test_update_skill_name_and_status_positive(client):
    skill_id = 1  # Valid skill_id
    new_name = "New Programming Skill Name"
    new_status = "inactive"
    request_body = {"skill_name": new_name, "skill_status": new_status}
    print(json.dumps(request_body))
    response = client.put(f"/skills/editSkill/{skill_id}", json=request_body)
    print("----response----")
    print(json.dumps(response.json()))
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "message": "Skill updated",
        "skill": {
            "skill_id": skill_id,
            "skill_name": new_name,
            "skill_status": new_status,
        },
    }


def test_update_skill_not_found(client):
    skill_id = 9999  # Non-existent skill_id
    new_name = "New Programming Skill Name"
    new_status = "inactive"
    request_body = {"skill_name": new_name, "skill_status": new_status}
    print(json.dumps(request_body))
    response = client.put(f"/skills/editSkill/{skill_id}", json=request_body)
    print("----response----")
    print(json.dumps(response.json()))
    assert response.status_code == 404
    assert response.json() == {"detail": "Skill not found"}


def test_get_all_skills(db, client):
    
    response = client.get("/skills")
    data = response.json()

    assert response.status_code == 200, response.text
    assert len(data) == 10


def test_get_skill_by_id(db, client):
    
    skill = models.SkillDetails(
        skill_id=20,
        skill_name="Test Skill",
        skill_status="active",
    )

    db.add(skill)
    db.commit()

    response = client.get("/skills/20")
    data = response.json()

    assert response.status_code == 200, response.text
    assert data == {
        "skill_id": 20,
        "skill_name": "Test Skill",
        "skill_status": "active",
    }

    response = client.get("/skills/21")
    assert response.status_code == 404, response.text

    
def test_delete_skill(db,client):
    test_skill = models.SkillDetails(
        skill_id=999,
        skill_name="Test Skill",
        skill_status="active"
    )

    db.add(test_skill)

    skill_id=999
    skill_name="Test Skill"
    skill_status="active"

    response = client.delete(f"/skills/deleteSkill/{skill_id}")
    print("----response----")
    print(json.dumps(response.json()))
    assert response.status_code == 200
    assert {"message": "Skill deleted", "skill": {"skill_id": skill_id, "skill_name": skill_name, "skill_status": skill_status}} == response.json()

def test_delete_skill_not_found(client):
    skill_id=9999

    response = client.delete(f"/skills/deleteSkill/{skill_id}")
    print("----response----")
    print(json.dumps(response.json()))
    assert response.status_code == 404
    assert response.json() == {"detail": "Skill not found"}

