import customtkinter as ctk
from PIL import Image

def abrir_menu():
    # Escolha inicial de tema ("light" ou "dark")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Janela principal (desktop style)
    menu_app = ctk.CTk(fg_color="#1E1E1E")
    menu_app.geometry("800x600")
    menu_app.title("menu - projeto integrador")
    
    
    main_frame = ctk.CTkFrame(
        master=menu_app,
        width=600,
        height=400,
        corner_radius=15,
        fg_color="#1C2732"
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    tabview = ctk.CTkTabview(master=main_frame, width=500,height=500)
    tabview.pack(pady=20,padx=30)
    
    tabview.add("cadastro")
    tabview.add("login")
    tabview.add("configurações")