from database.connection import get_connection


def create_tables():
    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL CHECK (length(trim(nome)) > 0),
            categoria TEXT NOT NULL DEFAULT '',
            fornecedor TEXT NOT NULL DEFAULT '',
            preco REAL NOT NULL CHECK (preco >= 0),
            quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
            estoque_minimo INTEGER NOT NULL DEFAULT 5 CHECK (estoque_minimo >= 0),
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('Entrada', 'Saída')),
            quantidade INTEGER NOT NULL CHECK (quantidade > 0),
            observacao TEXT NOT NULL DEFAULT '',
            data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(produto_id)
                REFERENCES produtos(id)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
        )
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_movimentacoes_produto
        ON movimentacoes(produto_id)
        """)
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_movimentacoes_data
        ON movimentacoes(data_movimentacao)
        """)

        conn.commit()
    finally:
        conn.close()
