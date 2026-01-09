# utilidades/gerenciador_telas.py
import customtkinter as ctk

screens = {}
footer_main = None
footer_secondary = None
_login_entries = {
    "email": {"widget": None, "placeholder": None},
    "senha": {"widget": None, "placeholder": None},
    "resultado": {"widget": None}
}

def register_screen(name, frame):
    screens[name] = frame

def show_screen(name):
    for frame in screens.values():
        frame.place_forget()

    frame = screens.get(name)
    if frame:
        if name in ["main", "cadastro", "catalogo", "funcionario", "assentos", "pagamento", "thank_you", "relatorio", "gestao_funcionarios"]:
            frame.place(relx=0, rely=0, relwidth=1, relheight=0.975)
        else:
            frame.place(relx=0.5, rely=0.5, anchor="center")

    # Footers (se existirem)
    global footer_main, footer_secondary
    if footer_main and footer_secondary:
        if name == "main":
            footer_secondary.place_forget()
            footer_main.place(relx=0, rely=1, relwidth=1, anchor="sw")
            # Limpar campos de login ao mostrar a tela principal
            try:
                clear_login_entries()
            except Exception:
                pass
        else:
            footer_main.place_forget()
            footer_secondary.place(relx=0.5, rely=1, relwidth=1, anchor="s")

def register_login_entries(email_entry, senha_entry, email_placeholder=None, senha_placeholder=None, resultado_label=None):
    """Registra os widgets de email, senha e opcionalmente o label de resultado para limpeza/restauração."""
    _login_entries["email"]["widget"] = email_entry
    _login_entries["email"]["placeholder"] = email_placeholder
    _login_entries["senha"]["widget"] = senha_entry
    _login_entries["senha"]["placeholder"] = senha_placeholder
    if resultado_label is not None:
        _login_entries["resultado"]["widget"] = resultado_label

def clear_login_entries():
    """Limpa o conteúdo dos widgets de login registrados."""
    email_info = _login_entries.get("email") or {}
    senha_info = _login_entries.get("senha") or {}
    email = email_info.get("widget")
    senha = senha_info.get("widget")
    email_ph = email_info.get("placeholder")
    senha_ph = senha_info.get("placeholder")

    # Limpar conteúdo e restaurar placeholder conhecido
    if email:
        try:
            email.delete(0, 'end')
        except Exception:
            try:
                email.configure(text="")
            except Exception:
                pass
        if email_ph is not None:
            try:
                email.configure(placeholder_text=email_ph)
            except Exception:
                pass

    if senha:
        try:
            senha.delete(0, 'end')
        except Exception:
            try:
                senha.configure(text="")
            except Exception:
                pass
        if senha_ph is not None:
            try:
                senha.configure(placeholder_text=senha_ph)
            except Exception:
                pass
    # Limpar label de resultado (mensagens como 'Bem-vindo')
    resultado_info = _login_entries.get("resultado") or {}
    resultado_widget = resultado_info.get("widget")
    if resultado_widget:
        try:
            resultado_widget.configure(text="")
        except Exception:
            try:
                resultado_widget.configure(value="")
            except Exception:
                pass
