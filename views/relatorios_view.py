import customtkinter as ctk
from tkinter import ttk

from services.estoque_service import listar_movimentacoes


# Paleta Essencial By Dani
AZUL_CLARO = "#A7D8F0"
AZUL_MEDIO = "#5BAFD8"
AZUL_ESCURO = "#2F7FA8"
ROSA = "#F4A7B9"
ROSA_ESCURO = "#E77A98"
FUNDO = "#F7FBFD"
BRANCO = "#FFFFFF"
TEXTO = "#2B2B2B"


class RelatoriosView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color=FUNDO
        )

        self.criar_widgets()
        self.carregar_movimentacoes()

    def criar_widgets(self):

        titulo = ctk.CTkLabel(
            self,
            text="Histórico de Movimentações",
            font=("Arial", 24, "bold"),
            text_color=AZUL_ESCURO
        )
        titulo.pack(pady=(20, 5))

        subtitulo = ctk.CTkLabel(
            self,
            text="Consulte entradas e saídas registradas no estoque.",
            font=("Arial", 13),
            text_color=TEXTO
        )
        subtitulo.pack(pady=(0, 15))

        btn_atualizar = ctk.CTkButton(
            self,
            text="Atualizar Relatório",
            command=self.carregar_movimentacoes,
            height=38,
            corner_radius=16,
            fg_color=AZUL_MEDIO,
            hover_color=AZUL_ESCURO,
            text_color=BRANCO,
            font=("Arial", 13, "bold")
        )
        btn_atualizar.pack(pady=10)

        tabela_frame = ctk.CTkFrame(
            self,
            fg_color=BRANCO,
            corner_radius=18
        )
        tabela_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        self.tree = ttk.Treeview(
            tabela_frame,
            columns=(
                "ID",
                "Produto",
                "Tipo",
                "Quantidade",
                "Observação",
                "Data"
            ),
            show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Produto", text="Produto")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Observação", text="Observação")
        self.tree.heading("Data", text="Data")

        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Produto", width=220)
        self.tree.column("Tipo", width=100, anchor="center")
        self.tree.column("Quantidade", width=110, anchor="center")
        self.tree.column("Observação", width=250)
        self.tree.column("Data", width=170, anchor="center")

        self.tree.tag_configure(
            "entrada",
            background="#E8F7FF",
            foreground=TEXTO
        )

        self.tree.tag_configure(
            "saida",
            background="#FFEAF0",
            foreground=TEXTO
        )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    def carregar_movimentacoes(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        movimentacoes = listar_movimentacoes()

        for movimentacao in movimentacoes:

            tipo = movimentacao["tipo"]

            if tipo == "Entrada":
                tag = "entrada"
            else:
                tag = "saida"

            self.tree.insert(
                "",
                "end",
                values=(
                    movimentacao["id"],
                    movimentacao["produto"],
                    movimentacao["tipo"],
                    movimentacao["quantidade"],
                    movimentacao["observacao"],
                    movimentacao["data_movimentacao"]
                ),
                tags=(tag,)
            )