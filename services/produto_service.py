from database.connection import get_connection
from models.produto import Produto


def cadastrar_produto(produto: Produto):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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
        produto.nome,
        produto.categoria,
        produto.fornecedor,
        produto.preco,
        produto.quantidade,
        produto.estoque_minimo
    ))

    conn.commit()
    conn.close()


def listar_produtos():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM produtos
        ORDER BY nome
    """)

    produtos = cursor.fetchall()

    conn.close()

    return produtos


def buscar_produto(id_produto):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM produtos
        WHERE id = ?
    """, (id_produto,))

    produto = cursor.fetchone()

    conn.close()

    return produto


def atualizar_produto(
    id_produto,
    nome,
    categoria,
    fornecedor,
    preco,
    estoque_minimo
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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

    conn.commit()
    conn.close()


def excluir_produto(id_produto):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM produtos
        WHERE id = ?
    """, (id_produto,))

    conn.commit()
    conn.close()


def listar_estoque_baixo():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM produtos
        WHERE quantidade <= estoque_minimo
        ORDER BY nome
    """)

    produtos = cursor.fetchall()

    conn.close()

    return produtos