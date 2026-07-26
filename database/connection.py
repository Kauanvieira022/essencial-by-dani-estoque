import sqlite3
import os


def get_database_path():
    local_app_data = os.getenv("LOCALAPPDATA")
    if not local_app_data:
        local_app_data = os.path.join(os.path.expanduser("~"), "AppData", "Local")

    base_dir = os.path.join(local_app_data, "ControleEstoque")
    os.makedirs(base_dir, exist_ok=True)

    return os.path.join(base_dir, "estoque.db")


def get_connection():
    db_path = get_database_path()

    conn = sqlite3.connect(db_path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 10000")

    return conn
