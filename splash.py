import os
import customtkinter as ctk
from PIL import Image
import login  # Importa login

# ======== CONFIGURAÇÃO INICIAL ======== #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def abrir_login():
    splash.destroy()
    login.abrir_login()

# ======== SPLASH ======== #
splash = ctk.CTk()
splash.overrideredirect(True)
largura, altura = 550, 350

splash.configure(fg_color="black")

# Centralizar na tela
screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()
x = (screen_width // 2) - (largura // 2)
y = (screen_height // 2) - (altura // 2)
splash.geometry(f"{largura}x{altura}+{x}+{y}")
splash.attributes("-alpha", 0)

# ======== LOGO CENTRAL ======== #
try:
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_logo = os.path.join(pasta_atual, "utilidades\\images\\logo_dark.png")  # renomeie sua logo para logo.png
    img = Image.open(caminho_logo)
    img = img.resize((200, 200), Image.Resampling.LANCZOS)  # tamanho da logo
    ctk_img = ctk.CTkImage(light_image=img, size=(200, 200))
    logo_label = ctk.CTkLabel(splash, image=ctk_img, text="", fg_color="black")
    logo_label.place(relx=0.5, rely=0.4, anchor="center")  # logo centralizada
except Exception as e:
    print("Erro ao carregar logo:", e)

# ======== TEXTO DE CARREGAMENTO ======== #
texto_label = ctk.CTkLabel(
    splash,
    text="Carregando CinePlus...",
    text_color="white",
    font=("Arial", 18, "bold")
)
texto_label.place(relx=0.5, rely=0.72, anchor="center")

# ======== BARRA DE PROGRESSO ======== #
progress = ctk.CTkProgressBar(splash, width=largura - 40)
progress.place(x=20, y=altura - 40)

# ======== ANIMAÇÃO FADE-IN ======== #
def fade_in(alpha=0, value=0):
    alpha += 0.02
    value += 1
    if alpha > 1: 
        alpha = 1
    if value > 100: 
        value = 100
    splash.attributes("-alpha", alpha)
    progress.set(value / 100)
    if value < 100:
        splash.after(30, lambda: fade_in(alpha, value))
    else:
        abrir_login()

fade_in()
splash.mainloop()

