"""User module: registration, login and administration (FR1).

Exposes REST endpoints with FastAPI. Every response omits the password
so that sensitive information is never exposed.
"""

import sqlite3

from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas import UserCreate, UserLogin, UserUpdate
from app.security import hash_password, verify_password

# Router with prefix and tag to group the routes in Swagger UI.
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def row_to_user(row) -> dict:
    """Convert a row of the User table into a dictionary without the password."""
    return {
        "user_id": row[0],
        "name": row[1],
        "email": row[2],
        "role": row[3],
    }


# --- WRITE ENDPOINTS ---

@router.post("", status_code=201)
def register_user(user: UserCreate):
    """Register a new user (user story: register customers)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Make sure the email is not already registered.
        cursor.execute("SELECT user_id FROM User WHERE email = ?", (user.email.lower(),))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email is already registered")

        # The password is stored hashed, never as plain text.
        cursor.execute(
            "INSERT INTO User (name, email, password, role) VALUES (?, ?, ?, ?)",
            (user.name, user.email.lower(), hash_password(user.password), user.role),
        )
        conn.commit()
        new_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        # The table requires unique names; report it to the client.
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()

    return {
        "message": "User registered successfully",
        "user": {"user_id": new_id, "name": user.name,
        "email": user.email.lower(), "role": user.role},
    }


@router.post("/login")
def login_user(credentials: UserLogin):
    """Validate a user's email and password."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, name, email, role, password FROM User WHERE email = ?",
            (credentials.email.lower(),),
        )
        row = cursor.fetchone()
    finally:
        conn.close()

    # Same message whether the email or the password fails, to avoid leaking hints.
    if row is None or not verify_password(credentials.password, row[4]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    return {"message": "Login successful", "user": row_to_user(row)}


@router.put("/{user_id}")
def update_user(user_id: int, changes: UserUpdate):
    """Update the name and/or role of an existing user."""
    data = changes.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields were provided to update")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM User WHERE user_id = ?", (user_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

        # Column names come from the validated schema, not from the client.
        assignments = ", ".join(f"{column} = ?" for column in data)
        cursor.execute(
            f"UPDATE User SET {assignments} WHERE user_id = ?",
            (*data.values(), user_id),
        )
        conn.commit()

        cursor.execute("SELECT user_id, name, email, role FROM User WHERE user_id = ?", (user_id,))
        updated = cursor.fetchone()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()

    return {"message": "User updated", "user": row_to_user(updated)}


@router.delete("/{user_id}")
def delete_user(user_id: int):
    """Delete a user by its identifier."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM User WHERE user_id = ?", (user_id,))
        conn.commit()
        deleted = cursor.rowcount
    finally:
        conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return {"message": f"User {user_id} deleted"}


# --- READ ENDPOINTS ---

@router.get("")
def list_users():
    """Return the list of registered users (without passwords)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, email, role FROM User")
        rows = cursor.fetchall()
    finally:
        conn.close()

    return {"users": [row_to_user(row) for row in rows]}


@router.get("/{user_id}")
def get_single_user(user_id: int):
    """Return a single user by its identifier."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, email, role FROM User WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
    finally:
        conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return row_to_user(row)