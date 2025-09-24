import customtkinter as ctk
from utilidades.config import *
from utilidades.ui_helpers import carregar_fundo, carregar_logo, carregar_icone, criar_botao, criar_footer
from telas.auth import fazer_login
from telas.abrir_cadastro import abrir_cadastro
from telas.seletor_assento import criar_tela_assentos
from telas.catalogo import mostrar_catalogo_filmes
from telas.sessao import criar_tela_sessoes
from telas.pagamentodocinema import mostrar_confirmacao_pagamento
from telas.agradecimento import mostrar_tela_agradecimento  # Updated to accept callback

from PIL import Image, ImageTk

# --- App setup ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk(fg_color=APP_BG)
screen_width, screen_height = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry(f"{screen_width+20}x{screen_height-80}-10+0")
app.title("menu - Projeto Integrador")

# --- Screen registry ---
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

    # Footer handling
    global footer_main, footer_secondary
    if footer_main and footer_secondary:
        if name == "main":
            footer_secondary.place_forget()
            footer_main.place(relx=0, rely=1, relwidth=1, anchor="sw")
        else:
            footer_main.place_forget()
            footer_secondary.place(relx=0.5, rely=1, relwidth=1, anchor="s")

# --- Payment screen helper ---
def mostrar_pagamento(filme, horario, qtd_ingressos=3, preco_unit=32.50):
    frame = screens["pagamento"]
    mostrar_confirmacao_pagamento(frame, filme, horario, qtd_ingressos, preco_unit)
    
    # Override Finalizar button to show Thank You
    for widget in frame.winfo_children():
        if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "Finalizar":
            widget.configure(command=lambda: [
                mostrar_tela_agradecimento(screens["thank_you"], voltar_callback=lambda: show_screen("main")),
                show_screen("thank_you")
            ])
    show_screen("pagamento")

# --- Seats screen with navigation to payment ---
def criar_tela_assentos_com_pagamento(filme, data, horario):
    frame = criar_tela_assentos(app, lambda: show_screen("sessoes"))

    def avancar_para_pagamento():
        mostrar_pagamento(filme, horario, qtd_ingressos=3, preco_unit=32.50)

    criar_botao(frame, "Avançar", avancar_para_pagamento, width=200).pack(pady=20)
    register_screen("assentos", frame)
    return frame

# --- Sessions screen ---
def criar_sessoes(filme):
    def on_sessao_selecionada(filme, data, horario):
        criar_tela_assentos_com_pagamento(filme, data, horario)
        show_screen("assentos")

    frame = criar_tela_sessoes(
        app,
        filme,
        lambda: show_screen("catalogo"),
        on_sessao_selecionada
    )
    register_screen("sessoes", frame)
    show_screen("sessoes")
    return frame

# --- Initialize all screens ---
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

    register_screen("main", tela_inicial)

    # --- Cadastro screen ---
    cadastro_frame, btn_voltar_cadastro = abrir_cadastro(app)
    btn_voltar_cadastro.configure(command=lambda: show_screen("main"))
    register_screen("cadastro", cadastro_frame)

    # --- Catalog screen ---
    catalogo_frame, btn_voltar_catalogo, btn_confirmar_catalogo = mostrar_catalogo_filmes(app)
    btn_voltar_catalogo.configure(command=lambda: show_screen("main"))

    def on_confirmar_catalogo():
        filme_selecionado = {"titulo": "Filme Exemplo", "descricao": "Descrição", "imagem": ""}
        criar_sessoes(filme_selecionado)

    btn_confirmar_catalogo.configure(command=on_confirmar_catalogo)
    register_screen("catalogo", catalogo_frame)

    # --- Payment and Thank You screens ---
    pagamento_frame = ctk.CTkFrame(app, fg_color="transparent")
    register_screen("pagamento", pagamento_frame)

    thank_you_frame = ctk.CTkFrame(app, fg_color="transparent")
    register_screen("thank_you", thank_you_frame)
    mostrar_tela_agradecimento(thank_you_frame, voltar_callback=lambda: show_screen("main"))

    # --- Footers ---
    footer_main, footer_secondary = criar_footer(app)

# --- Run app ---
inicializar_telas()
show_screen("main")
app.mainloop()
