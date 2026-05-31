import sqlite3
import os
import sys


def get_database_path():
    # ✅ Se estiver rodando como executável (.exe)
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # ✅ Caminho do banco
    return os.path.join(base_dir, "estoque.db")


def get_connection():
    db_path = get_database_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    return conn