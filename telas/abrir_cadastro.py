import customtkinter as ctk
from tkinter import messagebox

def abrir_cadastro(root):
    """Cria e retorna o frame de cadastro dentro da janela root"""

    frame = ctk.CTkFrame(root, width=600, height=400, corner_radius=15, fg_color="#1E1E1E")

    # Função para registrar usuário
    def registrar():
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        telefone = entry_telefone.get()
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        if not nome or not cpf or not telefone or not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
        else:
            messagebox.showinfo("Sucesso", f"Bem-vindo ao CinePlus, {usuario}!\nCadastro realizado com sucesso!")

    # Título
    ctk.CTkLabel(frame, text="Cadastro - CinePlus 🎬",
                 font=("Arial", 26, "bold"), text_color="white").pack(pady=(30, 10))

    # Campos de entrada
    campos_frame = ctk.CTkFrame(frame, fg_color="transparent")
    campos_frame.pack(expand=True, fill="both", padx=40, pady=10)
    
    entry_nome = ctk.CTkEntry(campos_frame, placeholder_text="Nome completo", width=400, height=45)
    entry_nome.pack(pady=10)
    entry_cpf = ctk.CTkEntry(campos_frame, placeholder_text="CPF", width=400, height=45)
    entry_cpf.pack(pady=10)
    entry_telefone = ctk.CTkEntry(campos_frame, placeholder_text="Telefone", width=400, height=45)
    entry_telefone.pack(pady=10)
    entry_usuario = ctk.CTkEntry(campos_frame, placeholder_text="Usuário", width=400, height=45)
    entry_usuario.pack(pady=10)
    entry_senha = ctk.CTkEntry(campos_frame, placeholder_text="Senha", show="*", width=400, height=45)
    entry_senha.pack(pady=10)

    # Botões frame
    botoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
    botoes_frame.pack(pady=80)
    
    # Botão de registrar
    ctk.CTkButton(botoes_frame, text="🎟 Registrar", command=registrar,
                  font=("Arial", 18, "bold"), width=180, height=45,
                  corner_radius=15, fg_color="#F6C148", hover_color="#E2952D",
                  border_width=2, border_color="#E2952D", text_color="#1C2732").pack(side="left", padx=10)

    # Botão Voltar
    btn_voltar = ctk.CTkButton(botoes_frame, text="Voltar",
                               font=("Arial", 18, "bold"), width=180, height=45,
                               corner_radius=15, fg_color="#F6C148", hover_color="#E2952D",
                               border_width=2, border_color="#E2952D", text_color="#1C2732")
    btn_voltar.pack(side="right", padx=10)

    return frame, btn_voltar