from database.connection import get_connection

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT,
        fornecedor TEXT,
        preco REAL NOT NULL,
        quantidade INTEGER DEFAULT 0,
        estoque_minimo INTEGER DEFAULT 5,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        observacao TEXT,
        data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(produto_id)
            REFERENCES produtos(id)
    )
    """)

    conn.commit()
    conn.close()

    print("Banco criado com sucesso!")