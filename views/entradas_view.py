import customtkinter as ctk
from tkinter import messagebox

from services.produto_service import listar_produtos
from services.estoque_service import registrar_entrada_estoque


# Paleta Essencial By Dani
AZUL_CLARO = "#A7D8F0"
AZUL_MEDIO = "#5BAFD8"
AZUL_ESCURO = "#2F7FA8"
ROSA = "#F4A7B9"
ROSA_ESCURO = "#E77A98"
FUNDO = "#F7FBFD"
BRANCO = "#FFFFFF"
TEXTO = "#2B2B2B"


class EntradasView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color=FUNDO
        )

        self.produtos = []

        self.criar_widgets()
        self.carregar_produtos()

    def criar_widgets(self):

        titulo = ctk.CTkLabel(
            self,
            text="Entrada de Estoque",
            font=("Arial", 24, "bold"),
            text_color=AZUL_ESCURO
        )
        titulo.pack(pady=(20, 5))

        subtitulo = ctk.CTkLabel(
            self,
            text="Registre a entrada de mercadorias no estoque.",
            font=("Arial", 13),
            text_color=TEXTO
        )
        subtitulo.pack(pady=(0, 15))

        formulario = ctk.CTkFrame(
            self,
            fg_color=BRANCO,
            corner_radius=18
        )
        formulario.pack(
            fill="x",
            padx=20,
            pady=10
        )

        label_produto = ctk.CTkLabel(
            formulario,
            text="Selecione o produto",
            font=("Arial", 14, "bold"),
            text_color=AZUL_ESCURO
        )
        label_produto.pack(pady=(20, 5))

        self.produto_var = ctk.StringVar(
            value="Selecione um produto"
        )

        self.produto_option = ctk.CTkOptionMenu(
            formulario,
            variable=self.produto_var,
            values=["Selecione um produto"],
            height=38,
            fg_color=AZUL_MEDIO,
            button_color=AZUL_ESCURO,
            button_hover_color=ROSA_ESCURO,
            text_color=BRANCO
        )
        self.produto_option.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        self.quantidade_entry = ctk.CTkEntry(
            formulario,
            placeholder_text="Quantidade de entrada",
            height=38,
            border_color=AZUL_CLARO
        )
        self.quantidade_entry.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.observacao_entry = ctk.CTkEntry(
            formulario,
            placeholder_text="Observação opcional",
            height=38,
            border_color=AZUL_CLARO
        )
        self.observacao_entry.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        btn_registrar = ctk.CTkButton(
            formulario,
            text="Registrar Entrada",
            command=self.registrar_entrada,
            height=40,
            corner_radius=16,
            fg_color=AZUL_MEDIO,
            hover_color=AZUL_ESCURO,
            text_color=BRANCO,
            font=("Arial", 14, "bold")
        )
        btn_registrar.pack(
            padx=20,
            pady=20
        )

    def carregar_produtos(self):

        self.produtos = listar_produtos()

        opcoes = []

        for produto in self.produtos:
            opcoes.append(
                f"{produto['id']} - {produto['nome']}"
            )

        if opcoes:
            self.produto_option.configure(values=opcoes)
            self.produto_var.set(opcoes[0])
        else:
            self.produto_option.configure(
                values=["Nenhum produto cadastrado"]
            )
            self.produto_var.set("Nenhum produto cadastrado")

    def registrar_entrada(self):

        try:
            produto_selecionado = self.produto_var.get()

            if produto_selecionado == "Nenhum produto cadastrado":
                messagebox.showwarning(
                    "Aviso",
                    "Nenhum produto cadastrado."
                )
                return

            quantidade_texto = self.quantidade_entry.get()

            if quantidade_texto.strip() == "":
                messagebox.showwarning(
                    "Aviso",
                    "Informe a quantidade de entrada."
                )
                return

            quantidade = int(quantidade_texto)

            if quantidade <= 0:
                messagebox.showwarning(
                    "Aviso",
                    "A quantidade deve ser maior que zero."
                )
                return

            id_produto = int(
                produto_selecionado.split(" - ")[0]
            )

            observacao = self.observacao_entry.get()

            registrar_entrada_estoque(
                id_produto,
                quantidade,
                observacao
            )

            messagebox.showinfo(
                "Sucesso",
                "Entrada registrada com sucesso!"
            )

            self.limpar_campos()
            self.carregar_produtos()

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Quantidade inválida. Digite apenas números inteiros."
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro)
            )

    def limpar_campos(self):

        self.quantidade_entry.delete(0, "end")
        self.observacao_entry.delete(0, "end")