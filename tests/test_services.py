import os
import sqlite3
import tempfile
import unittest

from database.connection import get_connection, get_database_path
from database.create_tables import create_tables
from models.produto import Produto
from services.estoque_service import (
    listar_movimentacoes,
    registrar_entrada_estoque,
    registrar_saida_estoque,
)
from services.produto_service import (
    atualizar_produto,
    buscar_produto,
    cadastrar_produto,
    excluir_produto,
)


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.local_app_data_original = os.environ.get("LOCALAPPDATA")
        self.temp_dir = tempfile.TemporaryDirectory()
        os.environ["LOCALAPPDATA"] = self.temp_dir.name
        create_tables()

    def tearDown(self):
        if self.local_app_data_original is None:
            os.environ.pop("LOCALAPPDATA", None)
        else:
            os.environ["LOCALAPPDATA"] = self.local_app_data_original
        self.temp_dir.cleanup()

    def cadastrar_produto(self, quantidade=0):
        return cadastrar_produto(
            Produto(
                nome="Hidratante",
                categoria="Corpo",
                fornecedor="Fornecedor A",
                preco=29.90,
                quantidade=quantidade,
                estoque_minimo=5,
            )
        )

    def test_conexao_ativa_chaves_estrangeiras(self):
        conn = get_connection()
        try:
            self.assertEqual(conn.execute("PRAGMA foreign_keys").fetchone()[0], 1)
        finally:
            conn.close()

    def test_entrada_e_saida_atualizam_saldo_e_historico(self):
        produto_id = self.cadastrar_produto(quantidade=2)

        registrar_entrada_estoque(produto_id, 5, "Reposição")
        registrar_saida_estoque(produto_id, 3, "Venda")

        produto = buscar_produto(produto_id)
        movimentacoes = listar_movimentacoes()
        self.assertEqual(produto["quantidade"], 4)
        self.assertEqual(len(movimentacoes), 2)
        self.assertEqual(
            {movimentacao["tipo"] for movimentacao in movimentacoes},
            {"Entrada", "Saída"},
        )

    def test_movimentacoes_rejeitam_quantidade_invalida(self):
        produto_id = self.cadastrar_produto(quantidade=5)

        for quantidade in (0, -1, "texto", True):
            with self.subTest(quantidade=quantidade):
                with self.assertRaises(ValueError):
                    registrar_entrada_estoque(produto_id, quantidade)

        self.assertEqual(buscar_produto(produto_id)["quantidade"], 5)
        self.assertEqual(listar_movimentacoes(), [])

    def test_saida_maior_que_saldo_nao_altera_estoque(self):
        produto_id = self.cadastrar_produto(quantidade=2)

        with self.assertRaisesRegex(ValueError, "maior que o estoque"):
            registrar_saida_estoque(produto_id, 3)

        self.assertEqual(buscar_produto(produto_id)["quantidade"], 2)
        self.assertEqual(listar_movimentacoes(), [])

    def test_produto_com_movimentacao_nao_pode_ser_excluido(self):
        produto_id = self.cadastrar_produto()
        registrar_entrada_estoque(produto_id, 1)

        with self.assertRaisesRegex(ValueError, "possui movimentações"):
            excluir_produto(produto_id)

        self.assertIsNotNone(buscar_produto(produto_id))
        self.assertEqual(len(listar_movimentacoes()), 1)

    def test_produto_sem_movimentacao_pode_ser_excluido(self):
        produto_id = self.cadastrar_produto()

        excluir_produto(produto_id)

        self.assertIsNone(buscar_produto(produto_id))

    def test_cadastro_rejeita_dados_invalidos(self):
        casos = (
            Produto("", "Corpo", "", 10, 0, 5),
            Produto("Produto", "Corpo", "", -1, 0, 5),
            Produto("Produto", "Corpo", "", float("nan"), 0, 5),
            Produto("Produto", "Corpo", "", 10, -1, 5),
            Produto("Produto", "Corpo", "", 10, 0, -1),
        )

        for produto in casos:
            with self.subTest(produto=produto.__dict__):
                with self.assertRaises(ValueError):
                    cadastrar_produto(produto)

    def test_atualizacao_preserva_quantidade(self):
        produto_id = self.cadastrar_produto(quantidade=8)

        atualizar_produto(
            produto_id,
            "Hidratante Premium",
            "Cuidados",
            "Fornecedor B",
            39.90,
            3,
        )

        produto = buscar_produto(produto_id)
        self.assertEqual(produto["nome"], "Hidratante Premium")
        self.assertEqual(produto["quantidade"], 8)
        self.assertEqual(produto["estoque_minimo"], 3)

    def test_banco_novo_passa_na_verificacao_de_integridade(self):
        conn = sqlite3.connect(get_database_path())
        try:
            resultado = conn.execute("PRAGMA integrity_check").fetchone()[0]
        finally:
            conn.close()

        self.assertEqual(resultado, "ok")


if __name__ == "__main__":
    unittest.main()
