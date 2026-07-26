from database.connection import get_connection


def _quantidade_positiva(valor):
    if isinstance(valor, bool):
        raise ValueError("Quantidade inválida.")

    try:
        quantidade = int(valor)
    except (TypeError, ValueError) as erro:
        raise ValueError("Quantidade deve ser um número inteiro.") from erro

    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")
    return quantidade


def _observacao(valor):
    return "" if valor is None else str(valor).strip()


def registrar_entrada_estoque(id_produto, quantidade, observacao=""):
    quantidade = _quantidade_positiva(quantidade)
    observacao = _observacao(observacao)

    conn = get_connection()
    try:
        cursor = conn.execute("""
            UPDATE produtos
            SET quantidade = quantidade + ?
            WHERE id = ?
        """, (quantidade, id_produto))

        if cursor.rowcount == 0:
            raise ValueError("Produto não encontrado.")

        conn.execute("""
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
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def registrar_saida_estoque(id_produto, quantidade, observacao=""):
    quantidade = _quantidade_positiva(quantidade)
    observacao = _observacao(observacao)

    conn = get_connection()
    try:
        cursor = conn.execute("""
            UPDATE produtos
            SET quantidade = quantidade - ?
            WHERE id = ? AND quantidade >= ?
        """, (
            quantidade,
            id_produto,
            quantidade
        ))

        if cursor.rowcount == 0:
            produto = conn.execute("""
                SELECT quantidade
                FROM produtos
                WHERE id = ?
            """, (id_produto,)).fetchone()

            if produto is None:
                raise ValueError("Produto não encontrado.")
            raise ValueError(
                "Quantidade de saída maior que o estoque disponível."
            )

        conn.execute("""
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
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def listar_movimentacoes():
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT
                movimentacoes.id,
                movimentacoes.produto_id,
                COALESCE(produtos.nome, 'Produto removido') AS produto,
                movimentacoes.tipo,
                movimentacoes.quantidade,
                movimentacoes.observacao,
                movimentacoes.data_movimentacao
            FROM movimentacoes
            LEFT JOIN produtos
                ON produtos.id = movimentacoes.produto_id
            ORDER BY movimentacoes.data_movimentacao DESC,
                     movimentacoes.id DESC
        """).fetchall()
    finally:
        conn.close()
