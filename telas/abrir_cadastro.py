import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from crud.crud_usuario import inserir_usuario

def abrir_cadastro(root):
    """Cria e retorna o frame de cadastro dentro da janela root"""

    frame = ctk.CTkFrame(root, fg_color="#1C1C1C")

    frame_principal = ctk.CTkFrame(frame, fg_color="#1C1C1C", width=1200, height=900)
    frame_principal.pack(anchor="w")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMAGE_DIR = os.path.join(BASE_DIR, "utilidades", "images")
    IMG_PATH = os.path.join(IMAGE_DIR, "cadastro.png")

    try:
        img = ctk.CTkImage(
            light_image=Image.open(IMG_PATH),
            dark_image=Image.open(IMG_PATH),
            size=(1200, 1200)
        )
        label_imagem = ctk.CTkLabel(frame_principal, image=img, text="")
    except:
        label_imagem = ctk.CTkLabel(
            frame_principal,
            text="🎬 CinePlus",
            font=("Arial", 32, "bold"),
            fg_color="#2B2B2B",
            width=450, height=600
        )

    label_imagem.pack(side="left", fill="y", expand=False, anchor="w")

    frame_direito = ctk.CTkFrame(frame_principal, fg_color="#1C1C1C")
    frame_direito.pack(side="right", fill="both", expand=True, padx=40, pady=20)

    titulo = ctk.CTkLabel(
        frame_direito,
        text="Cadastro - CinePlus 🎬",
        font=("Arial", 24, "bold")
    )
    titulo.pack(pady=20)

    # ======== FUNÇÃO REGISTRAR ========
    def registrar():
        nome = entry_nome.get().strip()
        telefone = entry_tel.get().strip()
        usuario = entry_user.get().strip()
        senha = entry_senha.get().strip()
        email = entry_email.get().strip()
        genero = var_genero.get()
        dia = combo_dia.get()
        mes = combo_mes.get()
        ano = combo_ano.get()

        if not (nome and usuario and senha):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return

        # Converter data para formato SQL (YYYY-MM-DD)
        meses_map = {
            "Janeiro": "01", "Fevereiro": "02", "Março": "03", "Abril": "04", "Maio": "05", "Junho": "06",
            "Julho": "07", "Agosto": "08", "Setembro": "09", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
        }
        mes_num = meses_map.get(mes, "01")
        data_nasc_sql = f"{ano}-{mes_num}-{dia}"

        sucesso = inserir_usuario(
            nome=nome,
            nome_login=usuario,
            senha=senha,
            email=email,
            telefone=telefone,
            genero=genero,
            data_nascimento=data_nasc_sql,
            tipo_usuario="cliente"
        )

        if sucesso:
            messagebox.showinfo("Sucesso", f"Usuário {usuario} cadastrado com sucesso!")
            entry_nome.delete(0, "end")
            entry_tel.delete(0, "end")
            entry_email.delete(0, "end")
            entry_user.delete(0, "end")
            entry_senha.delete(0, "end")
        else:
            messagebox.showerror("Erro", "Não foi possível cadastrar o usuário. Verifique o console.")

    # ======== CAMPOS DO FORMULÁRIO ========
    campos_frame = ctk.CTkFrame(frame_direito, fg_color="transparent")
    campos_frame.pack(fill="both", expand=True, pady=10)

    entry_nome = ctk.CTkEntry(campos_frame, placeholder_text="Nome completo", width=300, height=45)
    entry_tel = ctk.CTkEntry(campos_frame, placeholder_text="Telefone", width=300, height=45)
    entry_email = ctk.CTkEntry(campos_frame, placeholder_text="Email", width=300, height=45)
    entry_user = ctk.CTkEntry(campos_frame, placeholder_text="Usuário (login)", width=300, height=45)
    entry_senha = ctk.CTkEntry(campos_frame, placeholder_text="Senha", show="*", width=300, height=45)

    entry_nome.pack(pady=8)
    entry_tel.pack(pady=8)
    entry_email.pack(pady=8)
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

    ctk.CTkRadioButton(frame_genero, text="Feminino", variable=var_genero, value="F").grid(row=0, column=0, padx=10)
    ctk.CTkRadioButton(frame_genero, text="Masculino", variable=var_genero, value="M").grid(row=0, column=1, padx=10)
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
