import customtkinter as ctk
from PIL import Image
import os
from utilidades.config import BTN_COLOR, BTN_HOVER, BTN_TEXT, DARK_MODE, LIGHT_MODE

# --- Fundo ---
def carregar_fundo(frame, path):
    if os.path.exists(path):
        original_image = Image.open(path)

        def atualizar_fundo(event):
            largura, altura = event.width, event.height
            img_resized = original_image.resize((largura, altura))
            fundo_ctk = ctk.CTkImage(img_resized, size=(largura, altura))
            fundo_label.configure(image=fundo_ctk)
            fundo_label.image = fundo_ctk

        fundo_label = ctk.CTkLabel(frame, text="", fg_color="transparent")
        fundo_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        frame.bind("<Configure>", atualizar_fundo)
        return fundo_label
    else:
        return ctk.CTkLabel(frame, text="CinePlus", font=("Arial", 40, "bold"), fg_color="transparent")

# --- Logo ---
def carregar_logo(master, path):
    if os.path.exists(path):
        logo_image = ctk.CTkImage(light_image=Image.open(path),
                                  dark_image=Image.open(path),
                                  size=(200, 200))
        return ctk.CTkLabel(master=master, image=logo_image, text="", fg_color="transparent")
    return ctk.CTkLabel(master=master, text="CinePlus", font=("Arial", 24, "bold"), fg_color="transparent")

# --- Ícones ---
def carregar_icone(path, size=(30, 30)):
    return ctk.CTkImage(Image.open(path), size=size) if os.path.exists(path) else None

# --- Botão customizado ---
def criar_botao(master, texto, comando=None, icone=None, width=150, font=("Arial", 16, "bold")):
    return ctk.CTkButton(
        master=master,
        text=texto,
        image=icone,
        font=font,
        width=width,
        height=40,
        corner_radius=15,
        fg_color=BTN_COLOR,
        hover_color=BTN_HOVER,
        border_width=2,
        border_color=BTN_HOVER,
        text_color=BTN_TEXT,
        command=comando
    )

# --- Footer ---
def criar_footer(app):
    footer_inicial = ctk.CTkFrame(master=app, height=40, corner_radius=0, fg_color="#121212")
    footer_inicial.place(relx=0, rely=1, relwidth=1, anchor="sw")
    ctk.CTkLabel(footer_inicial, text="CinePlus © 2025", text_color="gray").pack(side="right", padx=20, pady=5)

    footer_secundario = ctk.CTkFrame(master=app, height=40, corner_radius=0, fg_color="#121212")
    ctk.CTkLabel(footer_secundario, text="CinePlus © 2025", text_color="gray").pack(pady=8)

    return footer_inicial, footer_secundario


def criar_entry_senha(master, placeholder="Sua senha", width=300, height=35, show_char='•', icone_fechado_path=None, icone_aberto_path=None, icon_size=(20, 20)):
    """Cria um frame com `CTkEntry` configurado para senha e um botão para alternar visibilidade.

    Retorna a tupla (container, entry, toggle_button). O botão altera o `show` do entry entre
    `show_char` e '' (visível).
    """
    container = ctk.CTkFrame(master, fg_color="transparent")

    # Usar grid interno para que o `entry` expanda e o botão mantenha largura fixa
    entry = ctk.CTkEntry(container, placeholder_text=placeholder, show=show_char, height=height)
    entry.grid(row=0, column=0, sticky='ew', padx=(0, 6), pady=5)
    container.grid_columnconfigure(0, weight=1)

    # Estado inicial: senha oculta
    estado = {"oculta": True}

    # Tentar carregar ícones se caminhos foram fornecidos
    icone_fechado_ctk = None
    icone_aberto_ctk = None
    if icone_fechado_path:
        icone_fechado_ctk = carregar_icone(icone_fechado_path, size=icon_size)
    if icone_aberto_path:
        icone_aberto_ctk = carregar_icone(icone_aberto_path, size=icon_size)

    def alternar():
        if estado["oculta"]:
            entry.configure(show="")
            if icone_aberto_ctk:
                toggle.configure(image=icone_aberto_ctk, text="")
            else:
                toggle.configure(text="Ocultar")
            estado["oculta"] = False
        else:
            entry.configure(show=show_char)
            if icone_fechado_ctk:
                toggle.configure(image=icone_fechado_ctk, text="")
            else:
                toggle.configure(text="Mostrar")
            estado["oculta"] = True

    # Botão com largura fixa; usa imagem se disponível
    # Estilo: botão mais quadrado e com as cores dos botões principais
    btn_kwargs = {
        'width': 36,
        'height': 36,
        'corner_radius': 8,
        'fg_color': BTN_COLOR,
        'hover_color': BTN_HOVER,
        'text_color': BTN_TEXT,
        'border_width': 0,
        'command': alternar,
    }

    if icone_fechado_ctk:
        toggle = ctk.CTkButton(container, image=icone_fechado_ctk, text="", **btn_kwargs)
    else:
        toggle = ctk.CTkButton(container, text="Mostrar", **btn_kwargs)

    toggle.grid(row=0, column=1, pady=5, padx=(0,2))

    return container, entry, toggle

# --- Alternância de Tema ---
def alternar_tema(app, botao_tema=None):
    """Alterna entre tema claro e escuro e atualiza a aparência da aplicação.
    
    Args:
        app: A janela principal da aplicação
        botao_tema: O botão de alternância de tema (para atualizar seu texto)
    """
    from utilidades import config
    
    # Alternar o tema
    if config.tema_atual == "dark":
        config.tema_atual = "light"
        ctk.set_appearance_mode("light")
        modo_novo = "light"
    else:
        config.tema_atual = "dark"
        ctk.set_appearance_mode("dark")
        modo_novo = "dark"
    
    # Atualizar cores na config
    cores = LIGHT_MODE if modo_novo == "light" else DARK_MODE
    config.APP_BG = cores["APP_BG"]
    config.BTN_COLOR = cores["BTN_COLOR"]
    config.BTN_HOVER = cores["BTN_HOVER"]
    config.BTN_TEXT = cores["BTN_TEXT"]
    config.COR_FUNDO = cores["COR_FUNDO"]
    config.COR_TEXTO = cores["COR_TEXTO"]
    config.COR_DESTAQUE = cores["COR_DESTAQUE"]
    
    # Atualizar a janela principal
    app.configure(fg_color=cores["APP_BG"])
    
    # Atualizar o botão de tema se fornecido
    if botao_tema:
        texto_botao = "🌙" if modo_novo == "dark" else "☀️"
        botao_tema.configure(text=texto_botao)
    
    return modo_novo