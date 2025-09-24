import customtkinter as ctk

def mostrar_frame(app, frame):
    """Oculta todas as frames e mostra apenas a selecionada"""
    for f in app.winfo_children():
        if isinstance(f, ctk.CTkFrame):
            f.pack_forget()
    frame.pack(expand=True, fill="both")
