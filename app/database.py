"""SQLite database connection for the Virtual Store project."""

import os
import sqlite3

# Default database file used by the application.
DEFAULT_DB_PATH = "virtual_store.db"


def get_connection() -> sqlite3.Connection:
    """Open a connection to the SQLite database.

    The path is read from the DB_PATH environment variable. If it is not
    set, virtual_store.db is used. This lets the automated tests work
    with a temporary database without touching the real data.
    """
    db_path = os.environ.get("DB_PATH", DEFAULT_DB_PATH)
    return sqlite3.connect(db_path)