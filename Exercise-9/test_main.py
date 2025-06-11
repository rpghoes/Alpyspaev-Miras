import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from models import User
from auth import get_password_hash

# Тестовая БД в памяти
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_register(client):
    res = client.post("/register", json={"username": "user1", "password": "pass1"})
    assert res.status_code == 200
    assert "user_id" in res.json()


def test_login(client):
    client.post("/register", json={"username": "user2", "password": "pass2"})
    res = client.post("/login", data={"username": "user2", "password": "pass2"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_protected_route_unauthorized(client):
    res = client.get("/users/me")
    assert res.status_code == 401


def get_token(client):
    client.post("/register", json={"username": "noteuser", "password": "pass"})
    res = client.post("/login", data={"username": "noteuser", "password": "pass"})
    return res.json()["access_token"]


def test_create_note(client):
    token = get_token(client)
    res = client.post(
        "/notes/",
        json={"title": "Test Note", "content": "Test Content"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json()["title"] == "Test Note"


def test_get_notes(client):
    token = get_token(client)
    client.post(
        "/notes/",
        json={"title": "Another Note", "content": "Content"},
        headers={"Authorization": f"Bearer {token}"}
    )
    res = client.get("/notes/", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) == 1


def test_delete_note(client):
    token = get_token(client)
    create = client.post(
        "/notes/",
        json={"title": "To Delete", "content": "bye"},
        headers={"Authorization": f"Bearer {token}"}
    )
    note_id = create.json()["id"]
    delete = client.delete(f"/notes/{note_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete.status_code == 200
    assert delete.json()["ok"] is True
