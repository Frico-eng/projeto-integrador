from crud.crud_usuario import verificar_login
from utilidades.gerenciador_telas import show_screen  # import seguro agora

def fazer_login(email_entry, senha_entry, resultado_label):
    email = email_entry.get().strip()
    senha = senha_entry.get().strip()

    if not email or not senha:
        resultado_label.configure(text="Preencha todos os campos.", text_color="red")
        return

    usuario = verificar_login(email, senha)
    if usuario:
        nome = usuario["Nome_Usuario"]
        resultado_label.configure(text=f"Bem-vindo, {nome}!", text_color="green")

        # Sempre vai para catálogo
        show_screen("catalogo")
    else:
        resultado_label.configure(text="Email ou senha incorretos.", text_color="red")
