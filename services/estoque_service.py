from database.connection import get_connection


def registrar_entrada_estoque(id_produto, quantidade, observacao=""):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT *
            FROM produtos
            WHERE id = ?
        """, (id_produto,))

        produto = cursor.fetchone()

        if produto is None:
            raise Exception("Produto não encontrado.")

        cursor.execute("""
            UPDATE produtos
            SET quantidade = quantidade + ?
            WHERE id = ?
        """, (
            quantidade,
            id_produto
        ))

        cursor.execute("""
            INSERT INTO movimentacoes (
                produto_id,
                tipo,
                quantidade,
                observacao
            )
            VALUES (?, ?, ?, ?)
        """, (
            id_produto,
            "Entrada",
            quantidade,
            observacao
        ))

        conn.commit()

    except Exception as erro:
        conn.rollback()
        raise erro

    finally:
        conn.close()


def registrar_saida_estoque(id_produto, quantidade, observacao=""):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT *
            FROM produtos
            WHERE id = ?
        """, (id_produto,))

        produto = cursor.fetchone()

        if produto is None:
            raise Exception("Produto não encontrado.")

        quantidade_atual = produto["quantidade"]

        if quantidade > quantidade_atual:
            raise Exception(
                "Quantidade de saída maior que o estoque disponível."
            )

        cursor.execute("""
            UPDATE produtos
            SET quantidade = quantidade - ?
            WHERE id = ?
        """, (
            quantidade,
            id_produto
        ))

        cursor.execute("""
            INSERT INTO movimentacoes (
                produto_id,
                tipo,
                quantidade,
                observacao
            )
            VALUES (?, ?, ?, ?)
        """, (
            id_produto,
            "Saída",
            quantidade,
            observacao
        ))

        conn.commit()

    except Exception as erro:
        conn.rollback()
        raise erro

    finally:
        conn.close()


def listar_movimentacoes():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            movimentacoes.id,
            produtos.nome AS produto,
            movimentacoes.tipo,
            movimentacoes.quantidade,
            movimentacoes.observacao,
            movimentacoes.data_movimentacao
        FROM movimentacoes
        INNER JOIN produtos
            ON produtos.id = movimentacoes.produto_id
        ORDER BY movimentacoes.data_movimentacao DESC
    """)

    movimentacoes = cursor.fetchall()

    conn.close()

    return movimentacoes