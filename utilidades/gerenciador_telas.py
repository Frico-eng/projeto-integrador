# utilidades/gerenciador_telas.py
import customtkinter as ctk

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
        if name in ["main", "cadastro", "catalogo", "funcionario", "assentos", "pagamento", "thank_you"]:
            frame.place(relx=0, rely=0, relwidth=1, relheight=0.975)
        else:
            frame.place(relx=0.5, rely=0.5, anchor="center")

    # Footers (se existirem)
    global footer_main, footer_secondary
    if footer_main and footer_secondary:
        if name == "main":
            footer_secondary.place_forget()
            footer_main.place(relx=0, rely=1, relwidth=1, anchor="sw")
        else:
            footer_main.place_forget()
            footer_secondary.place(relx=0.5, rely=1, relwidth=1, anchor="s")
