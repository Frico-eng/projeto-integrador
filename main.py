import os
import customtkinter as ctk
from PIL import Image

# --- IMPORTAÇÕES DO PROJETO --- #
from utilidades.config import *
from utilidades.ui_helpers import carregar_fundo, carregar_logo, carregar_icone, criar_botao, criar_footer
from telas.auth import fazer_login
from telas.abrir_cadastro import abrir_cadastro
from telas.seletor_assento import criar_tela_assentos
from telas.catalogo import criar_tela_catalogo
from telas.pagamentodocinema import mostrar_confirmacao_pagamento
from telas.agradecimento import mostrar_tela_agradecimento
from telas.feedback import criar_tela_feedback
from telas.funcionario import criar_tela_funcionario

# ============ CONFIGURAÇÃO GLOBAL ============ #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GerenciadorTelas:
    """Gerencia o registro e navegação entre telas da aplicação"""
    
    def __init__(self):
        self.screens = {}
        self.footer_main = None
        self.footer_secondary = None
        self.app = None
    
    def register_screen(self, name, frame):
        """Registra uma tela no gerenciador"""
        self.screens[name] = frame
    
    def show_screen(self, name):
        """Mostra a tela especificada e oculta as demais"""
        # Oculta todas as telas
        for frame in self.screens.values():
            frame.place_forget()
        
        # Mostra a tela solicitada
        frame = self.screens.get(name)
        if frame:
            if name == "main":
                frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            else:
                frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Gerencia os footers
        self._gerenciar_footers(name)
    
    def _gerenciar_footers(self, screen_name):
        """Gerencia a visibilidade dos footers baseado na tela atual"""
        if self.footer_main and self.footer_secondary:
            if screen_name == "main":
                self.footer_secondary.place_forget()
                self.footer_main.place(relx=0, rely=1, relwidth=1, anchor="sw")
            else:
                self.footer_main.place_forget()
                self.footer_secondary.place(relx=0.5, rely=1, relwidth=1, anchor="s")

class AplicacaoCinePlus:
    """Classe principal da aplicação CinePlus"""
    
    def __init__(self):
        self.app = None
        self.telas = GerenciadorTelas()
        self.dados_compra_atual = None
    
    def inicializar_app(self):
        """Inicializa a aplicação principal"""
        self.app = ctk.CTk(fg_color=APP_BG)
        self._configurar_janela()
        self.telas.app = self.app
        
        self.inicializar_telas()
        self.telas.show_screen("main")
        self.app.mainloop()
    
    def _configurar_janela(self):
        """Configura os parâmetros da janela principal"""
        screen_width, screen_height = self.app.winfo_screenwidth(), self.app.winfo_screenheight()
        self.app.geometry(f"{screen_width+20}x{screen_height-80}-10+0")
        self.app.title("CinePlus - Sistema de Cinema")
    
    def inicializar_telas(self):
        """Inicializa todas as telas da aplicação"""
        self._criar_tela_principal()
        self._criar_tela_feedback()
        self._criar_tela_cadastro()
        self._criar_tela_catalogo()
        self._criar_tela_funcionario()
        self._criar_tela_pagamento()
        self._criar_tela_agradecimento()
        self._criar_footers()
    
    def _criar_tela_principal(self):
        """Cria a tela principal/inicial da aplicação"""
        frame = ctk.CTkFrame(self.app, fg_color="transparent")
        carregar_fundo(frame, BANNER_PATH)
        
        right_frame = ctk.CTkFrame(frame, fg_color="transparent")
        right_frame.place(relx=0.65, rely=0, relwidth=0.25, relheight=1)
        
        # Logo
        carregar_logo(right_frame, LOGO_PATH).pack(pady=(30, 20))
        
        # Seção de login
        self._criar_secao_login(right_frame)
        
        # Botões de navegação
        self._criar_botoes_navegacao(right_frame)
        
        # Informações de contato
        self._criar_secao_contato(right_frame)
        
        self.telas.register_screen("main", frame)
    
    def _criar_secao_login(self, parent):
        """Cria a seção de login/cadastro"""
        login_container = ctk.CTkFrame(parent, fg_color="transparent")
        login_container.pack(pady=(0, 15))
        
        # Campos de entrada
        self.email_entry = ctk.CTkEntry(login_container, placeholder_text="Seu email", width=300, height=35)
        self.email_entry.pack(pady=5)
        
        self.senha_entry = ctk.CTkEntry(login_container, placeholder_text="Sua senha", show="•", width=300, height=35)
        self.senha_entry.pack(pady=5)
        
        # Label de resultado
        self.resultado_label = ctk.CTkLabel(login_container, text="", font=("Arial", 12))
        self.resultado_label.pack(pady=5)
        
        # Botões de ação
        botoes_frame = ctk.CTkFrame(login_container, fg_color="transparent")
        botoes_frame.pack(pady=5)
        
        icone_user = carregar_icone(ICON_USER_PATH)
        icone_regist = carregar_icone(ICON_REGIST_PATH)
        
        criar_botao(botoes_frame, "Entrar",
                   lambda: fazer_login(self.email_entry, self.senha_entry, self.resultado_label),
                   icone_user).pack(side="left", padx=5)
        
        criar_botao(botoes_frame, "Cadastro",
                   lambda: self.telas.show_screen("cadastro"),
                   icone_regist).pack(side="left", padx=5)
    
    def _criar_botoes_navegacao(self, parent):
        """Cria os botões de navegação principais"""
        icone_compra = carregar_icone(ICON_COMPRA_PATH)
        
        botoes_config = [
            ("Filmes em cartaz", lambda: self.telas.show_screen("catalogo"), icone_compra),
            ("Feedback", lambda: self.telas.show_screen("feedback"), None),
            ("Área do Funcionário", lambda: self.telas.show_screen("funcionario"), None)
        ]
        
        for texto, comando, icone in botoes_config:
            criar_botao(parent, texto, comando, icone, width=250).pack(pady=15)
    
    def _criar_secao_contato(self, parent):
        """Cria a seção de informações de contato"""
        contato_frame = ctk.CTkFrame(parent, fg_color="transparent")
        contato_frame.place(relx=0.5, rely=0.80, anchor="center")
        
        informacoes_contato = [
            "Entre em contato",
            "Telefone: 3022-2002",
            "Endereço: R. Aristides Lobo, 1058 - Campina, Belém - PA, 66017-010",
            "E-mail: sistema@cineplus.com.br"
        ]
        
        for info in informacoes_contato:
            ctk.CTkLabel(contato_frame, text=info, font=("Arial", 12)).pack(pady=2)
    
    def _criar_tela_feedback(self):
        """Cria a tela de feedback"""
        frame = criar_tela_feedback(self.app, voltar_callback=lambda: self.telas.show_screen("main"))
        self.telas.register_screen("feedback", frame)
    
    def _criar_tela_cadastro(self):
        """Cria a tela de cadastro"""
        frame, btn_voltar = abrir_cadastro(self.app)
        btn_voltar.configure(command=lambda: self.telas.show_screen("main"))
        self.telas.register_screen("cadastro", frame)
    
    def _criar_tela_catalogo(self):
        """Cria a tela de catálogo de filmes"""
        frame = ctk.CTkFrame(self.app, fg_color="transparent")
        
        catalogo_content = criar_tela_catalogo(
            frame, 
            voltar_callback=lambda: self.telas.show_screen("main"),
            confirmar_callback=self._on_confirmar_catalogo
        )
        catalogo_content.pack(fill="both", expand=True)
        
        self.telas.register_screen("catalogo", frame)
    
    def _criar_tela_funcionario(self):
        """Cria a tela do funcionário"""
        frame = ctk.CTkFrame(self.app, fg_color="transparent")
        
        funcionario_content = criar_tela_funcionario(
            frame,
            voltar_callback=lambda: self.telas.show_screen("main")
        )
        funcionario_content.pack(fill="both", expand=True)
        
        self.telas.register_screen("funcionario", frame)
    
    def _criar_tela_pagamento(self):
        """Cria a tela de pagamento"""
        frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.telas.register_screen("pagamento", frame)
    
    def _criar_tela_agradecimento(self):
        """Cria a tela de agradecimento"""
        frame = ctk.CTkFrame(self.app, fg_color="transparent")
        mostrar_tela_agradecimento(frame, voltar_callback=lambda: self.telas.show_screen("main"))
        self.telas.register_screen("thank_you", frame)
    
    def _criar_footers(self):
        """Cria os footers da aplicação"""
        self.telas.footer_main, self.telas.footer_secondary = criar_footer(self.app)
    
    def _on_confirmar_catalogo(self, filme_selecionado):
        """Callback chamado quando usuário confirma filme e horário no catálogo"""
        print(f"Filme selecionado no catálogo: {filme_selecionado['titulo']}")
        
        if filme_selecionado and filme_selecionado.get("horario_selecionado"):
            self._criar_tela_assentos_com_pagamento(filme_selecionado)
            self.telas.show_screen("assentos")
        else:
            print("Selecione um filme e um horário")
    
    def _criar_tela_assentos_com_pagamento(self, filme_completo):
        """Cria tela de assentos recebendo o filme completo com horário"""
        frame = criar_tela_assentos(
            self.app, 
            voltar_callback=lambda: self.telas.show_screen("catalogo"),
            avancar_callback=self._avancar_para_pagamento,
            filme_selecionado=filme_completo
        )
        
        self.telas.register_screen("assentos", frame)
        return frame
    
    def _avancar_para_pagamento(self, dados_compra):
        """Callback que recebe os dados completos da compra e avança para pagamento"""
        print(f"Indo para pagamento com dados: {dados_compra}")
        self.dados_compra_atual = dados_compra
        self._mostrar_pagamento(dados_compra)
    
    def _mostrar_pagamento(self, dados_compra):
        """Recebe dados completos da compra e mostra tela de pagamento"""
        filme = dados_compra["filme"]
        horario = filme.get("horario_selecionado", "")
        assentos = dados_compra["assentos"]
        qtd_ingressos = len(assentos)
        preco_unit = 32.50
        total = dados_compra["total"]
        
        frame = self.telas.screens["pagamento"]
        # Limpa o frame antes de mostrar o pagamento
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Define o callback para o botão Finalizar
        def finalizar_callback():
            mostrar_tela_agradecimento(
                self.telas.screens["thank_you"], 
                voltar_callback=lambda: self.telas.show_screen("main")
            )
            self.telas.show_screen("thank_you")
        
        mostrar_confirmacao_pagamento(
            frame, 
            filme["titulo"], 
            horario, 
            qtd_ingressos, 
            preco_unit, 
            assentos, 
            total,
            finalizar_callback=finalizar_callback
        )
        
        self.telas.show_screen("pagamento")

# Instância global da aplicação
app_cineplus = AplicacaoCinePlus()

def inicializar_app():
    """Função para inicializar a aplicação principal (mantida para compatibilidade)"""
    app_cineplus.inicializar_app()

# Permite executar o main.py diretamente (sem splash)
if __name__ == "__main__":
    inicializar_app()