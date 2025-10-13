import os
import customtkinter as ctk
from PIL import Image

# --- IMPORTA TODAS AS TELAS DO MENU --- #
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

# ================== MENU PRINCIPAL ================== #
screens = {}
footer_main = None
footer_secondary = None
app = None

def register_screen(name, frame):
    screens[name] = frame

def show_screen(name):
    for frame in screens.values():
        frame.place_forget()

    frame = screens.get(name)
    if frame:
        if name == "main":
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        else:
            frame.place(relx=0.5, rely=0.5, anchor="center")

    # Footers
    global footer_main, footer_secondary
    if footer_main and footer_secondary:
        if name == "main":
            footer_secondary.place_forget()
            footer_main.place(relx=0, rely=1, relwidth=1, anchor="sw")
        else:
            footer_main.place_forget()
            footer_secondary.place(relx=0.5, rely=1, relwidth=1, anchor="s")

def mostrar_pagamento(dados_compra):
    """Recebe dados completos da compra e mostra tela de pagamento"""
    filme = dados_compra["filme"]
    horario = filme.get("horario_selecionado", "")
    assentos = dados_compra["assentos"]
    qtd_ingressos = len(assentos)
    preco_unit = 32.50
    total = dados_compra["total"]
    
    frame = screens["pagamento"]
    # Limpa o frame antes de mostrar o pagamento
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Define o callback para o botão Finalizar
    def finalizar_callback():
        mostrar_tela_agradecimento(screens["thank_you"], voltar_callback=lambda: show_screen("main"))
        show_screen("thank_you")
    
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
    
    show_screen("pagamento")

def criar_tela_assentos_com_pagamento(filme_completo):
    """Cria tela de assentos recebendo o filme completo com horário"""
    
    def avancar_para_pagamento(dados_compra):
        """Callback que recebe os dados completos da compra"""
        print(f"Indo para pagamento com dados: {dados_compra}")
        mostrar_pagamento(dados_compra)
    
    # Cria a tela de assentos passando o filme completo
    frame = criar_tela_assentos(app, 
                               voltar_callback=lambda: show_screen("catalogo"),
                               avancar_callback=avancar_para_pagamento,
                               filme_selecionado=filme_completo)
    
    register_screen("assentos", frame)
    return frame

# --- Catalog screen callback ---
def on_confirmar_catalogo(filme_selecionado):
    """Callback chamado quando usuário confirma filme e horário no catálogo"""
    print(f"Filme selecionado no catálogo: {filme_selecionado['titulo']}")
    if filme_selecionado and filme_selecionado.get("horario_selecionado"):
        # Cria a tela de assentos passando o filme completo
        criar_tela_assentos_com_pagamento(filme_selecionado)
        show_screen("assentos")
    else:
        print("Selecione um filme e um horário")

def inicializar_telas():
    global footer_main, footer_secondary

    # --- Main screen ---
    tela_inicial = ctk.CTkFrame(app, fg_color="transparent")
    carregar_fundo(tela_inicial, BANNER_PATH)

    right_frame = ctk.CTkFrame(tela_inicial, fg_color="transparent")
    right_frame.place(relx=0.65, rely=0, relwidth=0.25, relheight=1)

    carregar_logo(right_frame, LOGO_PATH).pack(pady=(30, 20))

    icone_user = carregar_icone(ICON_USER_PATH)
    icone_regist = carregar_icone(ICON_REGIST_PATH)
    icone_compra = carregar_icone(ICON_COMPRA_PATH)

    # Login
    login_container = ctk.CTkFrame(right_frame, fg_color="transparent")
    login_container.pack(pady=(0, 15))
    email_entry = ctk.CTkEntry(login_container, placeholder_text="Seu email", width=300, height=35)
    email_entry.pack(pady=5)
    senha_entry = ctk.CTkEntry(login_container, placeholder_text="Sua senha", show="•", width=300, height=35)
    senha_entry.pack(pady=5)
    resultado_label = ctk.CTkLabel(login_container, text="", font=("Arial", 12))
    resultado_label.pack(pady=5)
    botoes_frame = ctk.CTkFrame(login_container, fg_color="transparent")
    botoes_frame.pack(pady=5)
    criar_botao(botoes_frame, "Entrar",
                lambda: fazer_login(email_entry, senha_entry, resultado_label),
                icone_user).pack(side="left", padx=5)
    criar_botao(botoes_frame, "Cadastro",
                lambda: show_screen("cadastro"),
                icone_regist).pack(side="left", padx=5)

    # Extra buttons
    criar_botao(right_frame, "Filmes em cartaz", lambda: show_screen("catalogo"), icone_compra, width=250).pack(pady=15)
    # Frame para agrupar os contatos no rodapé
    # Frame para agrupar os contatos no rodapé
    # Frame para os contatos fixo no rodapé
    criar_botao(right_frame, "Feedback", 
           lambda: show_screen("feedback"), 
           width=250).pack(pady=15)
    criar_botao(right_frame, "Área do Funcionário", 
               lambda: show_screen("funcionario"), 
               width=250).pack(pady=15)
    contato_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
    contato_frame.place(relx=0.5, rely=0.80, anchor="center")

    contato_label = ctk.CTkLabel(contato_frame, text="Entre em contato", font=("Arial", 12))
    contato_label.pack(pady=2)
    
    contato_fone_label = ctk.CTkLabel(contato_frame, text="Telefone: 3022-2002", font=("Arial", 12))
    contato_fone_label.pack(pady=2)

    contato_endereco_label = ctk.CTkLabel(contato_frame, text="Endereço: R. Aristides Lobo, 1058 - Campina, Belém - PA, 66017-010", font=("Arial", 12))
    contato_endereco_label.pack(pady=2)
    contato_email = ctk.CTkLabel(contato_frame, text="E-mail: sistema@cineplus.com.br", font=("Arial", 12))
    contato_email.pack(pady=2)
    register_screen("main", tela_inicial)

    
    feedback_frame = criar_tela_feedback(app, voltar_callback=lambda: show_screen("main"))
    register_screen("feedback", feedback_frame)
    # --- Cadastro screen ---
    cadastro_frame, btn_voltar_cadastro = abrir_cadastro(app)
    btn_voltar_cadastro.configure(command=lambda: show_screen("main"))
    register_screen("cadastro", cadastro_frame)

    # --- Catalog screen ---
    catalogo_frame = ctk.CTkFrame(app, fg_color="transparent")
    
    def on_voltar_catalogo():
        show_screen("main")
    
    # Cria o catálogo dentro do frame
    catalogo_content = criar_tela_catalogo(
        catalogo_frame, 
        voltar_callback=on_voltar_catalogo,
        confirmar_callback=on_confirmar_catalogo
    )
    catalogo_content.pack(fill="both", expand=True)
    
    register_screen("catalogo", catalogo_frame)

    funcionario_frame = ctk.CTkFrame(app, fg_color="transparent")
    def on_voltar_funcionario():
        show_screen("main")
    
    # Cria a tela de funcionário
    funcionario_content = criar_tela_funcionario(
        funcionario_frame,
        voltar_callback=on_voltar_funcionario
    )
    funcionario_content.pack(fill="both", expand=True)
    
    register_screen("funcionario", funcionario_frame)

    # --- Payment and Thank You screens ---
    pagamento_frame = ctk.CTkFrame(app, fg_color="transparent")
    register_screen("pagamento", pagamento_frame)

    thank_you_frame = ctk.CTkFrame(app, fg_color="transparent")
    register_screen("thank_you", thank_you_frame)
    mostrar_tela_agradecimento(thank_you_frame, voltar_callback=lambda: show_screen("main"))

    # --- Footers ---
    footer_main, footer_secondary = criar_footer(app)

def inicializar_app():
    """Função para inicializar a aplicação principal"""
    global app
    
    app = ctk.CTk(fg_color=APP_BG)
    screen_width, screen_height = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry(f"{screen_width+20}x{screen_height-80}-10+0")
    app.title("CinePlus - Sistema de Cinema")

    inicializar_telas()
    show_screen("main")
    app.mainloop()

# Permite executar o main.py diretamente (sem splash)
if __name__ == "__main__":
    inicializar_app()