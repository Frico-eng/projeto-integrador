import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os

def abrir_cadastro(root):
    """Cria e retorna o frame de cadastro dentro da janela root"""

    frame = ctk.CTkFrame(root, width=950, height=600, corner_radius=15, fg_color="#1C1C1C")
    
    # Frame principal (layout dividido)
    frame_principal = ctk.CTkFrame(frame, fg_color="#1C1C1C")
    frame_principal.pack(fill="both", expand=True, padx=0, pady=0)
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMAGE_DIR = os.path.join(BASE_DIR, "images")
    IMG_PATH = os.path.join(IMAGE_DIR, "funcionariodocinema.jpg")

    # ======== LADO ESQUERDO (IMAGEM) ========
    try:
        # Tente carregar a imagem, se não encontrar use um fundo colorido
        img = ctk.CTkImage(
            light_image=Image.open(IMG_PATH),
            dark_image=Image.open(IMG_PATH),
            size=(450, 600)
        )
        label_imagem = ctk.CTkLabel(frame_principal, image=img, text="")
    except:
        # Fallback se a imagem não for encontrada
        label_imagem = ctk.CTkLabel(frame_principal, text="🎬 CinePlus", 
                                  font=("Arial", 32, "bold"), 
                                  fg_color="#2B2B2B", 
                                  width=450, height=600)
    label_imagem.pack(side="left", padx=0, pady=0)

    # ======== LADO DIREITO (FORMULÁRIO) ========
    frame_direito = ctk.CTkFrame(frame_principal, fg_color="#1C1C1C")
    frame_direito.pack(side="right", fill="both", expand=True, padx=40, pady=20)

    # Título
    titulo = ctk.CTkLabel(
        frame_direito,
        text="Cadastro - CinePlus 🎬",
        font=("Arial", 24, "bold")
    )
    titulo.pack(pady=20)

    # Função de registro
    def registrar():
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        telefone = entry_tel.get()
        usuario = entry_user.get()
        senha = entry_senha.get()
        nascimento = f"{combo_dia.get()}/{combo_mes.get()}/{combo_ano.get()}"
        genero = var_genero.get()

        if not (nome and cpf and telefone and usuario and senha):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        messagebox.showinfo(
            "Sucesso",
            f"Bem-vindo ao CinePlus, {usuario}!\nCadastro realizado com sucesso!\nGênero: {genero}\nNascimento: {nascimento}"
        )

    # Campos do formulário
    campos_frame = ctk.CTkFrame(frame_direito, fg_color="transparent")
    campos_frame.pack(expand=True, fill="both", padx=0, pady=10)

    entry_nome = ctk.CTkEntry(campos_frame, placeholder_text="Nome completo", width=300, height=45)
    entry_cpf = ctk.CTkEntry(campos_frame, placeholder_text="CPF", width=300, height=45)
    entry_tel = ctk.CTkEntry(campos_frame, placeholder_text="Telefone", width=300, height=45)
    entry_user = ctk.CTkEntry(campos_frame, placeholder_text="Usuário", width=300, height=45)
    entry_senha = ctk.CTkEntry(campos_frame, placeholder_text="Senha", show="*", width=300, height=45)

    entry_nome.pack(pady=8)
    entry_cpf.pack(pady=8)
    entry_tel.pack(pady=8)
    entry_user.pack(pady=8)
    entry_senha.pack(pady=8)

    # Data de nascimento
    label_nasc = ctk.CTkLabel(campos_frame, text="Data de nascimento:", font=("Arial", 13))
    label_nasc.pack(pady=(15, 5))

    frame_data = ctk.CTkFrame(campos_frame, fg_color="transparent")
    frame_data.pack(pady=5)

    dias = [str(i) for i in range(1, 32)]
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    anos = [str(i) for i in range(1950, 2025)]

    combo_dia = ctk.CTkComboBox(frame_data, values=dias, width=70, height=35)
    combo_mes = ctk.CTkComboBox(frame_data, values=meses, width=120, height=35)
    combo_ano = ctk.CTkComboBox(frame_data, values=anos, width=90, height=35)

    combo_dia.grid(row=0, column=0, padx=5)
    combo_mes.grid(row=0, column=1, padx=5)
    combo_ano.grid(row=0, column=2, padx=5)

    # Gênero
    label_genero = ctk.CTkLabel(campos_frame, text="Gênero:", font=("Arial", 13))
    label_genero.pack(pady=(15, 5))

    var_genero = ctk.StringVar(value="Outro")
    frame_genero = ctk.CTkFrame(campos_frame, fg_color="transparent")
    frame_genero.pack(pady=5)

    ctk.CTkRadioButton(frame_genero, text="Feminino", variable=var_genero, value="Feminino").grid(row=0, column=0, padx=10)
    ctk.CTkRadioButton(frame_genero, text="Masculino", variable=var_genero, value="Masculino").grid(row=0, column=1, padx=10)
    ctk.CTkRadioButton(frame_genero, text="Outro", variable=var_genero, value="Outro").grid(row=0, column=2, padx=10)

    # Botões
    frame_botoes = ctk.CTkFrame(frame_direito, fg_color="transparent")
    frame_botoes.pack(pady=20)

    btn_registrar = ctk.CTkButton(
        frame_botoes, 
        text="🎟 Registrar", 
        font=("Arial", 16, "bold"),
        command=registrar,
        fg_color="#F6C148", 
        hover_color="#E2952D", 
        text_color="#1C2732", 
        width=180, 
        height=45,
        corner_radius=15,
        border_width=2, 
        border_color="#E2952D"
    )
    
    btn_voltar = ctk.CTkButton(
        frame_botoes, 
        text="Voltar", 
        font=("Arial", 16, "bold"),
        fg_color="#F6C148", 
        hover_color="#E2952D", 
        text_color="#1C2732", 
        width=180, 
        height=45,
        corner_radius=15,
        border_width=2, 
        border_color="#E2952D"
    )

    btn_registrar.grid(row=0, column=0, padx=10)
    btn_voltar.grid(row=0, column=1, padx=10)

    return frame, btn_voltar