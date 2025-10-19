import customtkinter as ctk
from tkinter import messagebox

def criar_tela_login(root, voltar_callback=None):
    """
    Cria e retorna o frame de login
    root: janela principal
    voltar_callback: função a ser chamada quando clicar no botão Voltar
    """
    
    frame = ctk.CTkFrame(root, width=400, height=500, fg_color="#1E1E1E", corner_radius=15)
    
    # Título principal
    titulo = ctk.CTkLabel(frame, text="🎬 CinePlus - Login", font=("Arial", 24, "bold"), text_color="white")
    titulo.pack(pady=(0, 10))

    # Subtítulo
    subtitulo = ctk.CTkLabel(frame, text="Faça seu login para acessar", font=("Arial", 14), text_color="lightgray")
    subtitulo.pack(pady=(0, 20))

    # Campo CPF
    cpf_entry = ctk.CTkEntry(frame, placeholder_text="CPF", width=300, height=35)
    cpf_entry.pack(pady=10)

    # Campo Usuário
    usuario_entry = ctk.CTkEntry(frame, placeholder_text="Usuário", width=300, height=35)
    usuario_entry.pack(pady=10)

    # Campo Senha
    senha_entry = ctk.CTkEntry(frame, placeholder_text="Senha", width=300, height=35, show="*")
    senha_entry.pack(pady=10)

    # Função de login
    def realizar_login():
        cpf = cpf_entry.get()
        usuario = usuario_entry.get()
        senha = senha_entry.get()

        if cpf and usuario and senha:
            messagebox.showinfo("Login", f"Bem-vindo ao CinePlus, {usuario}!")
        else:
            messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

    # Frame para botões
    frame_botoes = ctk.CTkFrame(frame, fg_color="transparent")
    frame_botoes.pack(pady=20)

    # Botão de login
    login_button = ctk.CTkButton(
        frame_botoes, 
        text="Entrar", 
        command=realizar_login, 
        width=250,
        height=45,
        fg_color="#F6C148", 
        hover_color="#E2952D",
        border_width=2,
        border_color="#E2952D",
        font=("Arial", 18, "bold"),
        text_color="#1C2732",
    )
    login_button.pack(pady=10)

    # Botão Voltar (se fornecido um callback)
    if voltar_callback:
        btn_voltar = ctk.CTkButton(
            frame_botoes, 
            text="Voltar",
            font=("Arial", 18, "bold"),
            width=250,
            height=45,
            corner_radius=10,
            fg_color="#F6C148",
            hover_color="#E2952D",
            border_width=2,
            border_color="#E2952D",
            text_color="#1C2732",
            command=voltar_callback
        )
        btn_voltar.pack(pady=10)

    return frame