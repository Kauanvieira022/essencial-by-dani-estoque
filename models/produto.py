# models/produto.py

class Produto:
    def __init__(
        self,
        nome,
        categoria,
        fornecedor,
        preco,
        quantidade=0,
        estoque_minimo=5,
        id=None
    ):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.fornecedor = fornecedor
        self.preco = preco
        self.quantidade = quantidade
        self.estoque_minimo = estoque_minimo

    def __str__(self):
        return f"{self.nome} - Estoque: {self.quantidade}"