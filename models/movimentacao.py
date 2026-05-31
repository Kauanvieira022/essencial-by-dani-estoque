# models/movimentacao.py

class Movimentacao:
    def __init__(
        self,
        produto_id,
        tipo,
        quantidade,
        observacao="",
        id=None,
        data_movimentacao=None
    ):
        self.id = id
        self.produto_id = produto_id
        self.tipo = tipo
        self.quantidade = quantidade
        self.observacao = observacao
        self.data_movimentacao = data_movimentacao

    def __str__(self):
        return (
            f"{self.tipo} | Produto: {self.produto_id} "
            f"| Quantidade: {self.quantidade}"
        )