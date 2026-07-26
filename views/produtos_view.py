import customtkinter as ctk
from tkinter import ttk, messagebox

from models.produto import Produto
from services.produto_service import (
    cadastrar_produto,
    listar_produtos,
    excluir_produto,
    listar_estoque_baixo,
    atualizar_produto
)
from services.export_service import exportar_produtos_excel


# 🎨 Paleta clean premium
AZUL = "#4F9CF9"
AZUL_HOVER = "#3B82F6"

CINZA_BG = "#F7F9FC"
CINZA_CARD = "#FFFFFF"
CINZA_BORDA = "#E5EAF0"
CINZA_SOFT = "#EEF2F7"

VERMELHO = "#E5484D"
VERDE = "#22C55E"

TEXTO = "#1F2937"


class ProdutosView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=CINZA_BG)

        self.produtos = []
        self.produto_id_edicao = None

        self.criar_widgets()
        self.carregar_produtos()

    def criar_widgets(self):

        # ✅ HEADER
        ctk.CTkLabel(
            self,
            text="Produtos",
            font=("Segoe UI", 26, "bold"),
            text_color=TEXTO
        ).pack(pady=(20, 4))

        ctk.CTkLabel(
            self,
            text="Gerencie seu estoque de forma simples",
            font=("Segoe UI", 13),
            text_color="#6B7280"
        ).pack()

        self.alerta_label = ctk.CTkLabel(
            self,
            text="",
            font=("Segoe UI", 12),
            text_color=VERMELHO
        )
        self.alerta_label.pack(pady=(6, 10))

        # ✅ BUSCA
        self.busca_entry = ctk.CTkEntry(
            self,
            placeholder_text="Buscar produto...",
            height=42,
            corner_radius=22,
            fg_color="#FFFFFF",
            border_color=CINZA_BORDA
        )
        self.busca_entry.pack(fill="x", padx=160, pady=10)
        self.busca_entry.bind("<KeyRelease>", self.filtrar_produtos)

        # ✅ CARD
        form = ctk.CTkFrame(
            self,
            fg_color=CINZA_CARD,
            corner_radius=14,
            border_width=1,
            border_color=CINZA_BORDA
        )
        form.pack(fill="x", padx=25, pady=15)

        container = ctk.CTkFrame(form, fg_color="transparent")
        container.pack(padx=25, pady=20, fill="x")

        def campo(label, parent):
            ctk.CTkLabel(
                parent,
                text=label,
                font=("Segoe UI", 11),
                text_color="#6B7280"
            ).pack(anchor="w")

            entry = ctk.CTkEntry(
                parent,
                height=36,
                border_color=CINZA_BORDA,
                fg_color="#FFFFFF"
            )
            entry.pack(fill="x", pady=(4, 12))

            return entry

        # ✅ GRID
        for i in range(3):
            linha = ctk.CTkFrame(container, fg_color="transparent")
            linha.pack(fill="x")

            col1 = ctk.CTkFrame(linha, fg_color="transparent")
            col1.pack(side="left", expand=True, fill="x", padx=6)

            col2 = ctk.CTkFrame(linha, fg_color="transparent")
            col2.pack(side="left", expand=True, fill="x", padx=6)

            if i == 0:
                self.nome_entry = campo("Nome", col1)
                self.categoria_entry = campo("Categoria", col2)

            elif i == 1:
                self.fornecedor_entry = campo("Fornecedor", col1)
                self.preco_entry = campo("Preço", col2)

            elif i == 2:
                self.quantidade_entry = campo("Quantidade", col1)
                self.estoque_minimo_entry = campo("Estoque mínimo", col2)

        # ✅ BOTÕES PRINCIPAIS
        botoes_top = ctk.CTkFrame(container, fg_color="transparent")
        botoes_top.pack(pady=(10, 5))

        ctk.CTkButton(
            botoes_top,
            text="Salvar",
            command=self.salvar_produto,
            fg_color=AZUL,
            hover_color=AZUL_HOVER,
            height=38,
            width=140,
            corner_radius=10
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            botoes_top,
            text="Editar",
            command=self.editar_produto,
            fg_color=AZUL,
            hover_color=AZUL_HOVER,
            height=38,
            width=140,
            corner_radius=10
        ).pack(side="left", padx=6)

        # ✅ BOTÕES SECUNDÁRIOS
        botoes_bottom = ctk.CTkFrame(container, fg_color="transparent")
        botoes_bottom.pack(pady=(5, 0))

        def botao_light(texto, comando):
            return ctk.CTkButton(
                botoes_bottom,
                text=texto,
                command=comando,
                fg_color=CINZA_SOFT,
                text_color=TEXTO,
                hover_color="#E5EAF0",
                height=36,
                corner_radius=10
            )

        botao_light("Excluir", self.excluir_produto).pack(side="left", padx=5)
        botao_light("Estoque baixo", self.carregar_estoque_baixo).pack(side="left", padx=5)
        botao_light("Todos", self.carregar_produtos).pack(side="left", padx=5)

        ctk.CTkButton(
            botoes_bottom,
            text="Exportar",
            command=self.exportar_excel,
            fg_color=VERDE,
            hover_color="#16A34A",
            height=36,
            corner_radius=10
        ).pack(side="left", padx=5)

        # ✅ TABELA
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Nome", "Categoria", "Qtd", "Preço", "Min", "Status"),
            show="headings",
            height=12
        )

        for col in ("ID", "Nome", "Categoria", "Qtd", "Preço", "Min", "Status"):
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True, padx=25, pady=15)
        self.tree.bind("<<TreeviewSelect>>", self.carregar_produto_selecionado)

    # ✅ FUNÇÕES

    def exportar_excel(self):
        exportar_produtos_excel(self.produtos)

    def salvar_produto(self):
        if self.produto_id_edicao is not None:
            messagebox.showwarning(
                "Aviso",
                "Você está editando um produto. Use o botão Editar ou "
                "clique em Todos para cancelar."
            )
            return

        try:
            produto = Produto(
                nome=self.nome_entry.get(),
                categoria=self.categoria_entry.get(),
                fornecedor=self.fornecedor_entry.get(),
                preco=float(self.preco_entry.get()),
                quantidade=int(self.quantidade_entry.get()),
                estoque_minimo=int(self.estoque_minimo_entry.get())
            )
            cadastrar_produto(produto)
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_produtos()
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def editar_produto(self):
        if self.produto_id_edicao is None:
            messagebox.showwarning(
                "Aviso",
                "Selecione um produto na tabela para editar."
            )
            return

        try:
            atualizar_produto(
                self.produto_id_edicao,
                self.nome_entry.get(),
                self.categoria_entry.get(),
                self.fornecedor_entry.get(),
                self.preco_entry.get(),
                self.estoque_minimo_entry.get()
            )
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_produtos()
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def excluir_produto(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                "Aviso",
                "Selecione um produto na tabela para excluir."
            )
            return

        valores = self.tree.item(sel[0])["values"]
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir o produto “{valores[1]}”?"
        )
        if not confirmar:
            return

        try:
            excluir_produto(valores[0])
            self.limpar_campos()
            self.carregar_produtos()
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def carregar_produto_selecionado(self, event=None):
        selecao = self.tree.selection()
        if not selecao:
            return

        id_produto = self.tree.item(selecao[0])["values"][0]
        produto = next(
            (p for p in self.produtos if p["id"] == id_produto),
            None
        )
        if produto is None:
            return

        self.produto_id_edicao = id_produto
        self.quantidade_entry.configure(state="normal")
        campos = (
            (self.nome_entry, produto["nome"]),
            (self.categoria_entry, produto["categoria"]),
            (self.fornecedor_entry, produto["fornecedor"]),
            (self.preco_entry, produto["preco"]),
            (self.quantidade_entry, produto["quantidade"]),
            (self.estoque_minimo_entry, produto["estoque_minimo"])
        )
        for campo, valor in campos:
            campo.delete(0, "end")
            campo.insert(0, "" if valor is None else str(valor))
        self.quantidade_entry.configure(state="disabled")

    def limpar_campos(self):
        self.produto_id_edicao = None
        self.quantidade_entry.configure(state="normal")
        for campo in (
            self.nome_entry,
            self.categoria_entry,
            self.fornecedor_entry,
            self.preco_entry,
            self.quantidade_entry,
            self.estoque_minimo_entry
        ):
            campo.delete(0, "end")

    def carregar_produtos(self):
        self.limpar_campos()
        self.produtos = listar_produtos()
        self.preencher_tabela(self.produtos)
        self.atualizar_alerta()

    def carregar_estoque_baixo(self):
        self.preencher_tabela(listar_estoque_baixo())

    def atualizar_alerta(self):
        qtd = len(listar_estoque_baixo())
        self.alerta_label.configure(
            text=f"{qtd} produtos com estoque baixo" if qtd > 0 else "Estoque em dia"
        )

    def filtrar_produtos(self, event):
        termo = self.busca_entry.get().lower()

        filtrados = [
            p for p in self.produtos
            if termo in (p["nome"] or "").lower()
            or termo in (p["categoria"] or "").lower()
            or termo in (p["fornecedor"] or "").lower()
        ]

        self.preencher_tabela(filtrados)

    def preencher_tabela(self, produtos):

        for i in self.tree.get_children():
            self.tree.delete(i)

        for p in produtos:

            status = "Baixo" if p["quantidade"] <= p["estoque_minimo"] else "OK"

            self.tree.insert(
                "",
                "end",
                values=(
                    p["id"],
                    p["nome"],
                    p["categoria"],
                    p["quantidade"],
                    p["preco"],
                    p["estoque_minimo"],
                    status
                )
            )
