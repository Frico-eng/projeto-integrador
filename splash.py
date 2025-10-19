import os
import customtkinter as ctk
from PIL import Image
import subprocess
import sys

# ============ CONFIGURAÇÃO SPLASH SCREEN ============ #
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
    caminho_logo = os.path.join(pasta_atual, "utilidades", "images", "logo_dark.png")
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

# Label de porcentagem
percent_label = ctk.CTkLabel(splash, text="0%", text_color="white", font=("Arial", 14, "bold"), fg_color="black")
percent_label.place(relx=0.5, y=altura - 60, anchor="center")

# ======== QUANDO TERMINAR O SPLASH ======== #
def abrir_menu_principal():
    """Fecha o splash e abre o menu principal"""
    splash.destroy()
    
    # Importa e executa o main após o splash
    try:
        from main import inicializar_app
        inicializar_app()
    except ImportError as e:
        print(f"Erro ao importar main: {e}")
        # Fallback: executar main.py como subprocesso
        subprocess.Popen([sys.executable, "main.py"])

# ======== ANIMAÇÃO SPLASH COM PORCENTAGEM ======== #
def fade_in(alpha=0, value=0):
    alpha += 0.02
    value += 1
    if alpha > 1: alpha = 1
    if value > 100: value = 100
    splash.attributes("-alpha", alpha)
    progress.set(value / 100)
    percent_label.configure(text=f"{value}%")
    
    if value < 100:
        splash.after(30, lambda: fade_in(alpha, value))
    else:
        splash.after(500, abrir_menu_principal)  # Pequena pausa antes de abrir o main

# Iniciar animação
fade_in()
splash.mainloop()