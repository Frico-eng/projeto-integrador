import re

def validar_email(email: str) -> bool:
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def fazer_login(email_entry, senha_entry, resultado_label):
    email = email_entry.get()
    senha = senha_entry.get()
    
    if not email or not senha:
        resultado_label.configure(text="Por favor, preencha todos os campos.", text_color="red")
        return
    
    if not validar_email(email):
        resultado_label.configure(text="Por favor, insira um email válido.", text_color="red")
        return
    
    if email == "admin@exemplo.com" and senha == "senha123":
        resultado_label.configure(text="Login bem-sucedido!", text_color="green")
    else:
        resultado_label.configure(text="Email ou senha incorretos.", text_color="red")
