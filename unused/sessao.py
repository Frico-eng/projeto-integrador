import customtkinter as ctk
from PIL import Image, ImageTk
import os
from datetime import datetime, timedelta
from tkcalendar import DateEntry

def criar_tela_sessoes(parent, filme_selecionado, callback_voltar, callback_avancar):
    """Cria tela de seleção de data e sessão para um filme ocupando mais espaço"""
    # Usar toda a área disponível
    frame = ctk.CTkFrame(parent, fg_color="#1E1E1E")
    frame.pack(fill="both", expand=True, padx=40, pady=30)  # Mais padding
    
    # Header apenas com título
    header_frame = ctk.CTkFrame(frame, fg_color="transparent", height=80)  # Mais alto
    header_frame.pack(fill="x", pady=(0, 30))
    header_frame.pack_propagate(False)
    
    ctk.CTkLabel(
        header_frame, 
        text=f"Selecionar Sessão: {filme_selecionado['titulo']}", 
        font=("Arial", 24, "bold")  # Fonte maior
    ).pack(side="left")
    
    # Conteúdo principal - Ocupando mais espaço
    content_frame = ctk.CTkFrame(frame, fg_color="transparent")
    content_frame.pack(fill="both", expand=True)
    
    # Grid principal com mais espaço
    content_frame.grid_columnconfigure(0, weight=7)  # Parte esquerda ainda maior
    content_frame.grid_columnconfigure(1, weight=3)  # Parte direita
    content_frame.grid_rowconfigure(0, weight=1)
    
    # COLUNA 1: Informações do filme (MUITO MAIOR)
    info_coluna = ctk.CTkFrame(content_frame, fg_color="transparent")
    info_coluna.grid(row=0, column=0, sticky="nsew", padx=(0, 40))
    
    # Título do filme (GRANDE)
    ctk.CTkLabel(
        info_coluna,
        text=filme_selecionado["titulo"],
        font=("Arial", 32, "bold"),  # Fonte bem maior
        wraplength=500
    ).pack(anchor="w", pady=(0, 30))
    
    # Container para imagem e descrição
    conteudo_frame = ctk.CTkFrame(info_coluna, fg_color="transparent")
    conteudo_frame.pack(fill="both", expand=True)
    
    # Imagem do filme (MUITO MAIOR)
    try:
        if os.path.exists(filme_selecionado["imagem"]):
            img = Image.open(filme_selecionado["imagem"])
            img = img.resize((350, 500), Image.LANCZOS)  # Imagem bem maior
            foto = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(conteudo_frame, image=foto, text="")
            img_label.image = foto
            img_label.pack(side="left", padx=(0, 30))
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
    
    # Descrição completa (MAIOR)
    descricao_frame = ctk.CTkFrame(conteudo_frame, fg_color="transparent")
    descricao_frame.pack(side="left", fill="both", expand=True)
    
    ctk.CTkLabel(
        descricao_frame,
        text="Sinopse:",
        font=("Arial", 20, "bold")  # Fonte maior
    ).pack(anchor="w", pady=(0, 15))
    
    descricao_texto = ctk.CTkTextbox(
        descricao_frame,
        height=400,  # Muito mais alto
        width=600,
        font=("Arial", 14),  # Fonte maior
        wrap="word",
        fg_color="#2B2B2B",
        border_width=1,
        border_color="#444"
    )
    descricao_texto.pack(fill="both", expand=True)
    descricao_texto.insert("1.0", filme_selecionado["descricao"])
    descricao_texto.configure(state="disabled")
    
    # COLUNA 2: Seleção de data e horário (MAIOR)
    selecao_coluna = ctk.CTkFrame(content_frame, fg_color="transparent")
    selecao_coluna.grid(row=0, column=1, sticky="nsew")
    
    # Título da seção (MAIOR)
    ctk.CTkLabel(
        selecao_coluna,
        text="Selecionar sessão",
        font=("Arial", 26, "bold")  # Fonte maior
    ).pack(anchor="w", pady=(0, 40))
    
    # CONTAINER PARA DATA E HORÁRIOS
    data_horario_frame = ctk.CTkFrame(selecao_coluna, fg_color="transparent")
    data_horario_frame.pack(fill="x", pady=(0, 30))
    
    # SEÇÃO DATA (MAIOR)
    data_frame = ctk.CTkFrame(data_horario_frame, fg_color="transparent")
    data_frame.pack(side="left", fill="y", padx=(0, 50))
    
    ctk.CTkLabel(
        data_frame,
        text="Data:",
        font=("Arial", 18, "bold")  # Fonte maior
    ).pack(anchor="w", pady=(0, 20))
    
    # DateEntry maior
    date_selector_frame = ctk.CTkFrame(data_frame, fg_color="white", height=45, width=220)  # Maior
    date_selector_frame.pack_propagate(False)
    date_selector_frame.pack(pady=(0, 15))
    
    hoje = datetime.now()
    data_var = ctk.StringVar(value=hoje.strftime("%d/%m/%Y"))
    
    date_entry = DateEntry(
        date_selector_frame,
        width=20,
        background='darkblue',
        foreground='white',
        borderwidth=2,
        mindate=hoje,
        maxdate=hoje + timedelta(days=30),
        date_pattern='dd/mm/yyyy',
        textvariable=data_var,
        font=("Arial", 12)  # Fonte maior no calendário
    )
    date_entry.pack(fill="both", expand=True, padx=3, pady=3)
    
    # Navegação de data (MAIOR)
    nav_frame = ctk.CTkFrame(data_frame, fg_color="transparent")
    nav_frame.pack(fill="x")
    
    def data_anterior():
        try:
            data_atual = datetime.strptime(data_var.get(), "%d/%m/%Y")
            nova_data = data_atual - timedelta(days=1)
            if nova_data >= hoje:
                data_var.set(nova_data.strftime("%d/%m/%Y"))
                date_entry.set_date(nova_data)
                atualizar_horarios_disponiveis()
        except:
            pass
    
    def data_seguinte():
        try:
            data_atual = datetime.strptime(data_var.get(), "%d/%m/%Y")
            nova_data = data_atual + timedelta(days=1)
            if nova_data <= hoje + timedelta(days=30):
                data_var.set(nova_data.strftime("%d/%m/%Y"))
                date_entry.set_date(nova_data)
                atualizar_horarios_disponiveis()
        except:
            pass
    
    btn_voltar_data = ctk.CTkButton(
        nav_frame,
        text="←",
        width=60,  # Maior
        height=40,  # Maior
        command=data_anterior,
        fg_color="#444",
        hover_color="#555",
        font=("Arial", 14)  # Fonte maior
    )
    btn_voltar_data.pack(side="left", padx=(0, 15))
    
    btn_avancar_data = ctk.CTkButton(
        nav_frame,
        text="→",
        width=60,  # Maior
        height=40,  # Maior
        command=data_seguinte,
        fg_color="#444",
        hover_color="#555",
        font=("Arial", 14)  # Fonte maior
    )
    btn_avancar_data.pack(side="left")
    
    # SEÇÃO HORÁRIOS (MAIOR)
    horarios_frame = ctk.CTkFrame(data_horario_frame, fg_color="transparent")
    horarios_frame.pack(side="left", fill="both", expand=True)
    
    ctk.CTkLabel(
        horarios_frame,
        text="Horários:",
        font=("Arial", 18, "bold")  # Fonte maior
    ).pack(anchor="w", pady=(0, 20))
    
    # Container para os horários
    horarios_container = ctk.CTkFrame(horarios_frame, fg_color="transparent")
    horarios_container.pack(fill="both", expand=True)
    
    horario_var = ctk.StringVar()
    
    def atualizar_horarios_disponiveis():
        """Atualiza os horários disponíveis baseado na data selecionada"""
        for widget in horarios_container.winfo_children():
            widget.destroy()
        
        try:
            data_selecionada = datetime.strptime(data_var.get(), "%d/%m/%Y")
        except:
            data_selecionada = datetime.now()
        
        todos_horarios = ["10:00", "14:00", "16:30", "19:00", "21:30"]
        horarios_disponiveis = []
        
        agora = datetime.now()
        
        for horario in todos_horarios:
            hora, minuto = map(int, horario.split(':'))
            horario_datetime = data_selecionada.replace(hour=hora, minute=minuto, second=0)
            
            if data_selecionada.date() == agora.date() and horario_datetime <= agora:
                continue
            
            horarios_disponiveis.append(horario)
        
        if not horarios_disponiveis:
            ctk.CTkLabel(
                horarios_container, 
                text="Não há sessões disponíveis",
                text_color="red",
                font=("Arial", 14)  # Fonte maior
            ).pack(expand=True)
            return
        
        # Radio buttons maiores
        for i, horario in enumerate(horarios_disponiveis):
            radio = ctk.CTkRadioButton(
                horarios_container, 
                text=horario, 
                variable=horario_var, 
                value=horario,
                font=("Arial", 16),  # Fonte maior
                fg_color="#F6C148",
                hover_color="#E2952D"
            )
            radio.grid(row=i//2, column=i%2, padx=15, pady=12, sticky="w")  # Mais espaçamento
    
    date_entry.bind("<<DateEntrySelected>>", lambda e: atualizar_horarios_disponiveis())
    atualizar_horarios_disponiveis()
    
    # BOTÕES VOLTAR E AVANÇAR (MAIORES)
    botoes_frame = ctk.CTkFrame(selecao_coluna, fg_color="transparent")
    botoes_frame.pack(fill="x", side="bottom", pady=(50, 0))  # Mais espaço
    
    def avancar_para_assentos():
        if not horario_var.get():
            return
        
        data_selecionada = data_var.get()
        horario_selecionado = horario_var.get()
        callback_avancar(filme_selecionado, data_selecionada, horario_selecionado)
    
    # Botão Voltar (MAIOR)
    btn_voltar = ctk.CTkButton(
        botoes_frame, 
        text="← Voltar", 
        command=callback_voltar,
        width=140,  # Mais largo
        height=50,  # Mais alto
        text_color="#000000",
        fg_color="#F6C148",
        hover_color="#E2952D",
        font=("Arial", 18, "bold")  # Fonte maior
    )
    btn_voltar.pack(side="left", padx=(0, 30))
    
    # Botão Avançar (MAIOR)
    btn_avancar = ctk.CTkButton(
        botoes_frame, 
        text="Avançar →", 
        command=avancar_para_assentos,
        width=140,  # Mais largo
        height=50,  # Mais alto
        text_color="#000000",
        fg_color="#F6C148",
        hover_color="#E2952D",
        font=("Arial", 18, "bold")  # Fonte maior
    )
    btn_avancar.pack(side="right")
    
    return frame