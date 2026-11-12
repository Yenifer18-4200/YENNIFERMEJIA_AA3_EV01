"""Automated tests for the user module.

Each test uses a temporary SQLite database, so the real data in
virtual_store.db is never modified.
"""

import sqlite3

import pytest
from fastapi.testclient import TestClient

# Structure of the User table, identical to the one used by the project.
CREATE_USER_TABLE = """
CREATE TABLE User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    email TEXT,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
"""

VALID_USER = {
    "name": "Ana Torres",
    "email": "ana@example.com",
    "password": "secret123",
    "role": "customer",
}


@pytest.fixture()
def db_path(tmp_path, monkeypatch):
    """Create a temporary database and point the application to it."""
    file_path = tmp_path / "test.db"
    conn = sqlite3.connect(file_path)
    conn.execute(CREATE_USER_TABLE)
    conn.commit()
    conn.close()
    monkeypatch.setenv("DB_PATH", str(file_path))
    return file_path


@pytest.fixture()
def client(db_path):
    """FastAPI test client."""
    from app.server import app
    return TestClient(app)


def test_register_user_ok(client):
    response = client.post("/users", json=VALID_USER)
    assert response.status_code == 201
    body = response.json()
    assert body["user"]["email"] == "ana@example.com"
    assert "password" not in body["user"]


def test_password_is_stored_hashed(client, db_path):
    client.post("/users", json=VALID_USER)
    conn = sqlite3.connect(db_path)
    stored = conn.execute("SELECT password FROM User").fetchone()[0]
    conn.close()
    assert stored != VALID_USER["password"]


def test_register_duplicate_email(client):
    client.post("/users", json=VALID_USER)
    other = {**VALID_USER, "name": "Another Person"}
    response = client.post("/users", json=other)
    assert response.status_code == 400


def test_register_invalid_email(client):
    response = client.post("/users", json={**VALID_USER, "email": "not-an-email"})
    assert response.status_code == 422


def test_register_short_password(client):
    response = client.post("/users", json={**VALID_USER, "password": "123"})
    assert response.status_code == 422


def test_login_ok(client):
    client.post("/users", json=VALID_USER)
    response = client.post(
        "/users/login",
        json={"email": VALID_USER["email"], "password": VALID_USER["password"]},
    )
    assert response.status_code == 200


def test_login_wrong_password(client):
    client.post("/users", json=VALID_USER)
    response = client.post(
        "/users/login",
        json={"email": VALID_USER["email"], "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_list_and_get_user(client):
    created = client.post("/users", json=VALID_USER).json()["user"]
    assert len(client.get("/users").json()["users"]) == 1
    assert client.get(f"/users/{created['user_id']}").status_code == 200
    assert client.get("/users/999").status_code == 404


def test_update_user(client):
    user_id = client.post("/users", json=VALID_USER).json()["user"]["user_id"]
    response = client.put(f"/users/{user_id}", json={"role": "admin"})
    assert response.status_code == 200
    assert response.json()["user"]["role"] == "admin"


def test_delete_user(client):
    user_id = client.post("/users", json=VALID_USER).json()["user"]["user_id"]
    assert client.delete(f"/users/{user_id}").status_code == 200
    assert client.delete(f"/users/{user_id}").status_code == 404