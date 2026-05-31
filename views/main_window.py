import customtkinter as ctk

from views.produtos_view import ProdutosView
from views.entradas_view import EntradasView
from views.saidas_view import SaidasView
from views.relatorios_view import RelatoriosView
from views.dashboard_view import DashboardView

# Paleta Essencial By Dani
AZUL_CLARO = "#A7D8F0"
AZUL_MEDIO = "#5BAFD8"
AZUL_ESCURO = "#2F7FA8"
ROSA = "#F4A7B9"
ROSA_ESCURO = "#E77A98"
FUNDO = "#F7FBFD"
BRANCO = "#FFFFFF"
TEXTO = "#2B2B2B"


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Essencial By Dani - Controle de Estoque")
        self.geometry("1100x650")
        self.minsize(950, 550)
        self.configure(fg_color=FUNDO)

        self.criar_layout()

        # ✅ abre o dashboard ao iniciar
        self.abrir_dashboard()

    def criar_layout(self):

        self.menu_lateral = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color=AZUL_CLARO
        )
        self.menu_lateral.pack(side="left", fill="y")
        self.menu_lateral.pack_propagate(False)

        self.area_conteudo = ctk.CTkFrame(
            self,
            fg_color=FUNDO,
            corner_radius=0
        )
        self.area_conteudo.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.criar_menu()

    def criar_menu(self):

        logo_frame = ctk.CTkFrame(
            self.menu_lateral,
            fg_color="transparent"
        )
        logo_frame.pack(pady=(35, 25), padx=15, fill="x")

        titulo_menu = ctk.CTkLabel(
            logo_frame,
            text="Essencial\nBy Dani",
            font=("Arial", 28, "bold"),
            text_color=AZUL_ESCURO
        )
        titulo_menu.pack()

        subtitulo_menu = ctk.CTkLabel(
            logo_frame,
            text="Controle de Estoque",
            font=("Arial", 13),
            text_color=TEXTO
        )
        subtitulo_menu.pack(pady=(6, 0))

        separador = ctk.CTkFrame(
            self.menu_lateral,
            height=2,
            fg_color=ROSA
        )
        separador.pack(fill="x", padx=25, pady=(0, 25))

        # ✅ DASHBOARD
        self.btn_dashboard = self.criar_botao_menu(
            texto="Dashboard",
            comando=self.abrir_dashboard
        )
        self.btn_dashboard.pack(padx=20, pady=7, fill="x")

        # ✅ OUTROS
        self.btn_produtos = self.criar_botao_menu(
            texto="Produtos",
            comando=self.abrir_produtos
        )
        self.btn_produtos.pack(padx=20, pady=7, fill="x")

        self.btn_entradas = self.criar_botao_menu(
            texto="Entrada de Estoque",
            comando=self.abrir_entradas
        )
        self.btn_entradas.pack(padx=20, pady=7, fill="x")

        self.btn_saidas = self.criar_botao_menu(
            texto="Saída de Estoque",
            comando=self.abrir_saidas
        )
        self.btn_saidas.pack(padx=20, pady=7, fill="x")

        self.btn_relatorios = self.criar_botao_menu(
            texto="Relatórios",
            comando=self.abrir_relatorios
        )
        self.btn_relatorios.pack(padx=20, pady=7, fill="x")

        espaco = ctk.CTkFrame(
            self.menu_lateral,
            fg_color="transparent"
        )
        espaco.pack(fill="both", expand=True)

        rodape = ctk.CTkLabel(
            self.menu_lateral,
            text="Essencial By Dani",
            font=("Arial", 11),
            text_color=AZUL_ESCURO
        )
        rodape.pack(pady=(0, 20))

    def criar_botao_menu(self, texto, comando):

        return ctk.CTkButton(
            self.menu_lateral,
            text=texto,
            command=comando,
            height=42,
            corner_radius=18,
            fg_color=BRANCO,
            hover_color=ROSA,
            text_color=AZUL_ESCURO,
            font=("Arial", 14, "bold")
        )

    def marcar_botao_ativo(self, botao):

        botoes = [
            self.btn_dashboard,
            self.btn_produtos,
            self.btn_entradas,
            self.btn_saidas,
            self.btn_relatorios
        ]

        for btn in botoes:
            btn.configure(
                fg_color=BRANCO,
                text_color=AZUL_ESCURO,
                hover_color=ROSA
            )

        botao.configure(
            fg_color=ROSA_ESCURO,
            text_color=BRANCO,
            hover_color=ROSA_ESCURO
        )

    def limpar_conteudo(self):

        for widget in self.area_conteudo.winfo_children():
            widget.destroy()

    # ✅ DASHBOARD
    def abrir_dashboard(self):

        self.limpar_conteudo()
        self.marcar_botao_ativo(self.btn_dashboard)

        tela = DashboardView(self.area_conteudo)
        tela.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_produtos(self):

        self.limpar_conteudo()
        self.marcar_botao_ativo(self.btn_produtos)

        tela = ProdutosView(self.area_conteudo)
        tela.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_entradas(self):

        self.limpar_conteudo()
        self.marcar_botao_ativo(self.btn_entradas)

        tela = EntradasView(self.area_conteudo)
        tela.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_saidas(self):

        self.limpar_conteudo()
        self.marcar_botao_ativo(self.btn_saidas)

        tela = SaidasView(self.area_conteudo)
        tela.pack(fill="both", expand=True, padx=20, pady=20)

    def abrir_relatorios(self):

        self.limpar_conteudo()
        self.marcar_botao_ativo(self.btn_relatorios)

        tela = RelatoriosView(self.area_conteudo)
        tela.pack(fill="both", expand=True, padx=20, pady=20)