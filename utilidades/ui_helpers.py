import customtkinter as ctk
from PIL import Image
import os
from utilidades.config import BTN_COLOR, BTN_HOVER, BTN_TEXT

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
def criar_botao(master, texto, comando=None, icone=None, width=150):
    return ctk.CTkButton(
        master=master,
        text=texto,
        image=icone,
        font=("Arial", 16, "bold"),
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
