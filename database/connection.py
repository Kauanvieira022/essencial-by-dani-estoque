import sqlite3
import os


def get_database_path():
    # ✅ Pasta padrão do usuário
    base_dir = os.path.join(os.environ["LOCALAPPDATA"], "ControleEstoque")

    # ✅ Cria a pasta se não existir
    os.makedirs(base_dir, exist_ok=True)

    return os.path.join(base_dir, "estoque.db")


def get_connection():
    db_path = get_database_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    return conn