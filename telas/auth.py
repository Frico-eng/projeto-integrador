from crud.crud_usuario import verificar_login
from utilidades.gerenciador_telas import show_screen
from utilidades.session import login as session_login

def fazer_login(email_entry, senha_entry, resultado_label):
    email = email_entry.get().strip()
    senha = senha_entry.get().strip()

    if not email or not senha:
        resultado_label.configure(text="Preencha todos os campos.", text_color="red")
        return

    usuario = verificar_login(email, senha)
    if usuario:
        nome = usuario["Nome_Usuario"]
        tipo_usuario = usuario.get("Tipo_Usuario", "cliente")  # Assume "cliente" como padrão se não existir
        
        resultado_label.configure(text=f"Bem-vindo, {nome}!", text_color="green")

        # Registrar usuário na sessão
        try:
            session_login(usuario)
        except Exception:
            pass

        # Lógica de redirecionamento baseada no tipo de usuário
        if tipo_usuario.lower() == "gerente":
            show_screen("gerente")
        elif tipo_usuario.lower() == "funcionario":
            show_screen("funcionario")
        else:
            show_screen("catalogo")
    else:
        resultado_label.configure(text="Email ou senha incorretos.", text_color="red")