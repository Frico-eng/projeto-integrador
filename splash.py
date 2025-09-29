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

# ============ CONFIGURAÇÃO GLOBAL ============ #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- SPLASH SCREEN --- #
splash = ctk.CTk()
splash.overrideredirect(True)
largura, altura = 550, 350
splash.configure(fg_color="black")

# Centralizar
screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()
x = (screen_width // 2) - (largura // 2)
y = (screen_height // 2) - (altura // 2)
splash.geometry(f"{largura}x{altura}+{x}+{y}")
splash.attributes("-alpha", 0)

# Logo
try:
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_logo = os.path.join(pasta_atual, "utilidades\\images\\logo_dark.png")
    img = Image.open(caminho_logo)
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    ctk_img = ctk.CTkImage(light_image=img, size=(200, 200))
    logo_label = ctk.CTkLabel(splash, image=ctk_img, text="", fg_color="black")
    logo_label.place(relx=0.5, rely=0.4, anchor="center")
except Exception as e:
    print("Erro ao carregar logo:", e)

# Texto
texto_label = ctk.CTkLabel(
    splash,
    text="Carregando CinePlus...",
    text_color="white",
    font=("Arial", 18, "bold")
)
texto_label.place(relx=0.5, rely=0.72, anchor="center")

# Barra de progresso
progress = ctk.CTkProgressBar(splash, width=largura - 40)
progress.place(x=20, y=altura - 40)

# ================== MENU PRINCIPAL ================== #
screens = {}
footer_main = None
footer_secondary = None

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

def mostrar_pagamento(filme, horario, qtd_ingressos=3, preco_unit=32.50):
    frame = screens["pagamento"]
    mostrar_confirmacao_pagamento(frame, filme, horario, qtd_ingressos, preco_unit)
    
    for widget in frame.winfo_children():
        if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "Finalizar":
            widget.configure(command=lambda: [
                mostrar_tela_agradecimento(screens["thank_you"], voltar_callback=lambda: show_screen("main")),
                show_screen("thank_you")
            ])
    show_screen("pagamento")

def criar_tela_assentos_com_pagamento(filme, horario):
    def avancar_para_pagamento():
        mostrar_pagamento(filme, horario, qtd_ingressos=3, preco_unit=32.50)

    filme_com_horario = filme.copy()
    filme_com_horario["horario_selecionado"] = horario

    frame = criar_tela_assentos(app, 
                               voltar_callback=lambda: show_screen("catalogo"),
                               avancar_callback=avancar_para_pagamento,
                               filme_selecionado=filme_com_horario)
    register_screen("assentos", frame)
    return frame

def inicializar_telas():
    global footer_main, footer_secondary

    # Main
    tela_inicial = ctk.CTkFrame(app, fg_color="transparent")
    carregar_fundo(tela_inicial, BANNER_PATH)

    right_frame = ctk.CTkFrame(tela_inicial, fg_color="transparent")
    right_frame.place(relx=0.65, rely=0, relwidth=0.25, relheight=1)

    carregar_logo(right_frame, LOGO_PATH).pack(pady=(30, 20))

    icone_user = carregar_icone(ICON_USER_PATH)
    icone_regist = carregar_icone(ICON_REGIST_PATH)
    icone_compra = carregar_icone(ICON_COMPRA_PATH)

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

    criar_botao(right_frame, "Filmes em cartaz", lambda: show_screen("catalogo"), icone_compra, width=250).pack(pady=15)

    register_screen("main", tela_inicial)

    # Cadastro
    cadastro_frame, btn_voltar_cadastro = abrir_cadastro(app)
    btn_voltar_cadastro.configure(command=lambda: show_screen("main"))
    register_screen("cadastro", cadastro_frame)

    # Catalogo
    catalogo_frame = ctk.CTkFrame(app, fg_color="transparent")
    
    def on_voltar_catalogo():
        show_screen("main")
    
    def on_confirmar_catalogo(filme_selecionado, horario_selecionado):
        if filme_selecionado and horario_selecionado:
            criar_tela_assentos_com_pagamento(filme_selecionado, horario_selecionado)
            show_screen("assentos")
    
    catalogo_content, btn_voltar, btn_confirmar = criar_tela_catalogo(
        catalogo_frame, 
        voltar_callback=on_voltar_catalogo,
        confirmar_callback=on_confirmar_catalogo
    )
    catalogo_content.pack(fill="both", expand=True)
    register_screen("catalogo", catalogo_frame)

    pagamento_frame = ctk.CTkFrame(app, fg_color="transparent")
    register_screen("pagamento", pagamento_frame)

    thank_you_frame = ctk.CTkFrame(app, fg_color="transparent")
    register_screen("thank_you", thank_you_frame)
    mostrar_tela_agradecimento(thank_you_frame, voltar_callback=lambda: show_screen("main"))

    footer_main, footer_secondary = criar_footer(app)

# ======== QUANDO TERMINAR O SPLASH ======== #
def abrir_menu():
    global app
    splash.destroy()

    app = ctk.CTk(fg_color=APP_BG)
    screen_width, screen_height = app.winfo_screenwidth(), app.winfo_screenheight()
    app.geometry(f"{screen_width+20}x{screen_height-80}-10+0")
    app.title("menu - Projeto Integrador")

    inicializar_telas()
    show_screen("main")
    app.mainloop()

# ======== ANIMAÇÃO SPLASH ======== #
def fade_in(alpha=0, value=0):
    alpha += 0.02
    value += 1
    if alpha > 1: alpha = 1
    if value > 100: value = 100
    splash.attributes("-alpha", alpha)
    progress.set(value / 100)
    if value < 100:
        splash.after(30, lambda: fade_in(alpha, value))
    else:
        abrir_menu()

fade_in()
splash.mainloop()
