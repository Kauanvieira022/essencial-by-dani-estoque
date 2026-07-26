import customtkinter as ctk
from tkinter import StringVar
from datetime import datetime

from services.produto_service import (
    listar_produtos,
    listar_estoque_baixo
)

from services.estoque_service import listar_movimentacoes

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# Paleta
AZUL_MEDIO = "#5BAFD8"
AZUL_ESCURO = "#2F7FA8"
ROSA_ESCURO = "#E77A98"
VERDE = "#4CAF50"
VERMELHO = "#D9534F"
FUNDO = "#F7FBFD"
BRANCO = "#FFFFFF"


class DashboardView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=FUNDO)

        self.mes_var = StringVar()

        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):

        # Título
        titulo = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Arial", 26, "bold"),
            text_color=AZUL_ESCURO
        )
        titulo.pack(pady=(20, 10))

        # ✅ GERAR LISTA DINÂMICA MES/ANO
        movimentacoes = listar_movimentacoes()
        opcoes = {"Todos"}

        for m in movimentacoes:

            m = dict(m)

            data = datetime.strptime(
                m["data_movimentacao"],
                "%Y-%m-%d %H:%M:%S"
            )
            opcoes.add(data.strftime("%m/%Y"))

        opcoes = sorted(list(opcoes))
        self.mes_var.set("Todos")

        # ✅ FILTRO
        filtro_frame = ctk.CTkFrame(self, fg_color="transparent")
        filtro_frame.pack(pady=10)

        ctk.CTkLabel(
            filtro_frame,
            text="Filtrar por mês/ano:"
        ).pack(side="left", padx=5)

        ctk.CTkOptionMenu(
            filtro_frame,
            values=opcoes,
            variable=self.mes_var,
            command=self.atualizar_dashboard
        ).pack(side="left")

        # ✅ CARDS
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", padx=20)

        self.total_produtos_label = self.criar_card("Produtos", AZUL_MEDIO)
        self.estoque_baixo_label = self.criar_card("Estoque Baixo", VERMELHO)
        self.entradas_label = self.criar_card("Entradas", VERDE)
        self.saidas_label = self.criar_card("Saídas", ROSA_ESCURO)

        # ✅ GRÁFICO
        self.grafico_frame = ctk.CTkFrame(self, fg_color=BRANCO)
        self.grafico_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def criar_card(self, titulo, cor):

        frame = ctk.CTkFrame(self.cards_frame, fg_color=cor)
        frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(frame, text=titulo, text_color="white").pack(pady=(10, 0))

        valor = ctk.CTkLabel(
            frame,
            text="0",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        valor.pack()

        return valor

    def carregar_dados(self):
        self.atualizar_dashboard()

    def atualizar_dashboard(self, event=None):

        produtos = listar_produtos()
        estoque_baixo = listar_estoque_baixo()
        movimentacoes = listar_movimentacoes()

        produtos_dict = {p["id"]: p for p in produtos}

        categorias = {}
        entradas = 0
        saidas = 0

        filtro = self.mes_var.get()

        for m in movimentacoes:

            m = dict(m)

            data = datetime.strptime(
                m["data_movimentacao"],
                "%Y-%m-%d %H:%M:%S"
            )
            mes_ano = data.strftime("%m/%Y")

            if filtro != "Todos" and mes_ano != filtro:
                continue

            produto = produtos_dict.get(m["produto_id"])

            if not produto:
                continue

            categoria = produto["categoria"] or "Sem categoria"
            quantidade = m["quantidade"]

            if categoria not in categorias:
                categorias[categoria] = 0

            # ✅ SOMA REAL
            if m["tipo"] == "Entrada":
                entradas += quantidade
                categorias[categoria] += quantidade
            else:
                saidas += quantidade
                categorias[categoria] += quantidade

        # ✅ CARDS
        self.total_produtos_label.configure(text=str(len(produtos)))
        self.estoque_baixo_label.configure(text=str(len(estoque_baixo)))
        self.entradas_label.configure(text=str(entradas))
        self.saidas_label.configure(text=str(saidas))

        # ✅ GRÁFICO
        self.atualizar_grafico(categorias)

    def atualizar_grafico(self, categorias):

        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)

        labels = list(categorias.keys())
        valores = list(categorias.values())

        if sum(valores) == 0:
            labels = ["Sem dados"]
            valores = [1]

        ax.pie(
            valores,
            labels=labels,
            autopct="%1.1f%%"
        )

        ax.set_title("Movimentação por Categoria")

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)
