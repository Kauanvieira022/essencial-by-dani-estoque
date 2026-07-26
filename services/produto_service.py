import math

from database.connection import get_connection
from models.produto import Produto


def _texto_obrigatorio(valor, campo):
    texto = str(valor).strip()
    if not texto:
        raise ValueError(f"{campo} é obrigatório.")
    return texto


def _texto_opcional(valor):
    return "" if valor is None else str(valor).strip()


def _preco_valido(valor):
    try:
        preco = float(valor)
    except (TypeError, ValueError) as erro:
        raise ValueError("Preço inválido.") from erro

    if not math.isfinite(preco) or preco < 0:
        raise ValueError("O preço deve ser um número maior ou igual a zero.")
    return preco


def _inteiro_nao_negativo(valor, campo):
    if isinstance(valor, bool):
        raise ValueError(f"{campo} inválido.")

    try:
        numero = int(valor)
    except (TypeError, ValueError) as erro:
        raise ValueError(f"{campo} deve ser um número inteiro.") from erro

    if numero < 0:
        raise ValueError(f"{campo} não pode ser negativo.")
    return numero


def cadastrar_produto(produto: Produto):
    nome = _texto_obrigatorio(produto.nome, "Nome")
    categoria = _texto_opcional(produto.categoria)
    fornecedor = _texto_opcional(produto.fornecedor)
    preco = _preco_valido(produto.preco)
    quantidade = _inteiro_nao_negativo(produto.quantidade, "Quantidade")
    estoque_minimo = _inteiro_nao_negativo(
        produto.estoque_minimo,
        "Estoque mínimo"
    )

    conn = get_connection()
    try:
        cursor = conn.execute("""
            INSERT INTO produtos (
                nome,
                categoria,
                fornecedor,
                preco,
                quantidade,
                estoque_minimo
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            nome,
            categoria,
            fornecedor,
            preco,
            quantidade,
            estoque_minimo
        ))
        conn.commit()
        return cursor.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def listar_produtos():
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT *
            FROM produtos
            ORDER BY nome COLLATE NOCASE
        """).fetchall()
    finally:
        conn.close()


def buscar_produto(id_produto):
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT *
            FROM produtos
            WHERE id = ?
        """, (id_produto,)).fetchone()
    finally:
        conn.close()


def atualizar_produto(
    id_produto,
    nome,
    categoria,
    fornecedor,
    preco,
    estoque_minimo
):
    nome = _texto_obrigatorio(nome, "Nome")
    categoria = _texto_opcional(categoria)
    fornecedor = _texto_opcional(fornecedor)
    preco = _preco_valido(preco)
    estoque_minimo = _inteiro_nao_negativo(
        estoque_minimo,
        "Estoque mínimo"
    )

    conn = get_connection()
    try:
        cursor = conn.execute("""
            UPDATE produtos
            SET
                nome = ?,
                categoria = ?,
                fornecedor = ?,
                preco = ?,
                estoque_minimo = ?
            WHERE id = ?
        """, (
            nome,
            categoria,
            fornecedor,
            preco,
            estoque_minimo,
            id_produto
        ))
        if cursor.rowcount == 0:
            raise ValueError("Produto não encontrado.")
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def excluir_produto(id_produto):
    conn = get_connection()
    try:
        total_movimentacoes = conn.execute("""
            SELECT COUNT(*)
            FROM movimentacoes
            WHERE produto_id = ?
        """, (id_produto,)).fetchone()[0]

        if total_movimentacoes:
            raise ValueError(
                "Este produto possui movimentações e não pode ser excluído. "
                "Edite o cadastro ou mantenha-o para preservar o histórico."
            )

        cursor = conn.execute("""
            DELETE FROM produtos
            WHERE id = ?
        """, (id_produto,))
        if cursor.rowcount == 0:
            raise ValueError("Produto não encontrado.")
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def listar_estoque_baixo():
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT *
            FROM produtos
            WHERE quantidade <= estoque_minimo
            ORDER BY nome COLLATE NOCASE
        """).fetchall()
    finally:
        conn.close()
