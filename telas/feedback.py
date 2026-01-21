import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from utilidades.ui_helpers import alternar_tema
from utilidades.config import BTN_COLOR, BTN_HOVER, BTN_TEXT
import utilidades.config as config_module

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Sobe para a pasta pai de 'telas'
IMAGE_DIR = os.path.join(BASE_DIR, "utilidades", "images")
FEEDBACK_IMAGE_PATH = os.path.join(IMAGE_DIR, "feedback.png")


def criar_tela_feedback(parent, voltar_callback=None, fonte_global=None):
    """Cria e retorna o frame da tela de feedback"""
    
    # Funções para aumentar/diminuir fonte se fonte_global for fornecida
    def aumentar_fonte():
        if fonte_global and fonte_global.cget("size") < 22:  # 14 + (4 * 2)
            fonte_global.configure(size=fonte_global.cget("size") + 2)

    def diminuir_fonte():
        if fonte_global and fonte_global.cget("size") > 6:  # 14 - (4 * 2)
            fonte_global.configure(size=fonte_global.cget("size") - 2)
    
    # Função para atualizar cores baseado no tema
    def atualizar_cores_tema():
        tema_escuro = config_module.tema_atual == "dark"
        
        if tema_escuro:
            bg_frame = "#2B2B2B"
            text_color = "white"
        else:
            bg_frame = "#E8E8E8"
            text_color = "black"
        
        # Atualizar cores dos elementos
        frame_conteudo.configure(fg_color=bg_frame)
   
    # ===== FUNÇÕES =====
    def fade_out():
        """Diminui gradualmente a opacidade e volta à tela principal."""
        alpha = parent.attributes("-alpha")
        if alpha > 0:
            alpha -= 0.05
            parent.attributes("-alpha", alpha)
            parent.after(50, fade_out)
        else:
            parent.attributes("-alpha", 1.0)
            if voltar_callback:
                voltar_callback()


    def enviar_sugestao():
        tema = combo_tema.get()
        descricao = texto_sugestao.get("1.0", "end").strip()


        if not tema or not descricao:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return


        # Exibe agradecimento antes do fade
        messagebox.showinfo(
            "Obrigado!",
            "🎬 Obrigado pela sua sugestão!\nSua opinião é muito importante para nós."
        )
        fade_out()


    def toggle_ident():
        switch_ident.configure(text="Sim" if switch_ident.get() else "Não")
    
    # Frame principal - sem pack, será controlado pelo gerenciador_telas
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    
    # Frame de fundo com imagem (ocupa todo o frame)
    bg_frame = ctk.CTkFrame(frame, fg_color="transparent")
    bg_frame.pack(fill="both", expand=True)
    
    # Carregar imagem de fundo se existir
    img_path = os.path.join(IMAGE_DIR, "feedback.png")
    if os.path.exists(img_path):
        try:
            img = Image.open(img_path)
            # Redimensionar para cobrir a tela
            screen_width = parent.winfo_screenwidth()
            screen_height = parent.winfo_screenheight()
            img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=(screen_width, screen_height))
            
            bg_label = ctk.CTkLabel(bg_frame, image=photo, text="")
            bg_label.image = photo
            bg_label.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            bg_frame.configure(fg_color="#1a1a1a")
    else:
        bg_frame.configure(fg_color="#1a1a1a")
    
    # Frame de conteúdo que se sobrepõe ao fundo (usando place para sobreposição)
    frame_conteudo = ctk.CTkFrame(frame, fg_color="#2B2B2B", corner_radius=10)
    frame_conteudo.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.35, relheight=0.7)
    
    # Frame de controle de fonte e tema (no topo do frame_conteudo)
    if fonte_global:
        frame_controle_fonte = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
        frame_controle_fonte.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkButton(frame_controle_fonte, text="A+", command=aumentar_fonte, width=50, font=fonte_global).pack(side="left", padx=5)
        ctk.CTkButton(frame_controle_fonte, text="A-", command=diminuir_fonte, width=50, font=fonte_global).pack(side="left", padx=5)
        
        # Botão para alternar tema claro e escuro
        botao_tema = ctk.CTkButton(
            frame_controle_fonte,
            text="🌙",
            command=lambda: [alternar_tema(parent, botao_tema), atualizar_cores_tema()],
            width=50,
            font=fonte_global,
            fg_color=BTN_COLOR,
            hover_color=BTN_HOVER,
            text_color=BTN_TEXT
        )
        botao_tema.pack(side="left", padx=5)
    
    # Atualizar cores iniciais
    atualizar_cores_tema()

    # ===== LOGO =====
    logo_label = ctk.CTkLabel(frame_conteudo, text="💬", font=("Arial", 40))
    logo_label.pack(pady=10)

    titulo = ctk.CTkLabel(frame_conteudo,
                          text="CAIXA DE SUGESTÕES",
                          font=fonte_global if fonte_global else ("Arial", 20, "bold"))
    titulo.pack(pady=5)

    subtitulo = ctk.CTkLabel(frame_conteudo,
        text="Sua opinião é importante.\n Utilize este espaço para registrar\n sugestões, críticas construtivas ou observações\n que ajudem a melhorar nossos  ambiente de trabalho.",
        font=fonte_global if fonte_global else ("Arial", 12))
    subtitulo.pack(pady=5)

    # ===== CAMPOS =====
    campos_frame = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    campos_frame.pack(pady=5, padx=20, fill="both", expand=True)

    label_tema = ctk.CTkLabel(campos_frame, text="Tema da sugestão (obrigatório)", 
                              font=fonte_global if fonte_global else ("Arial", 10))
    label_tema.pack(anchor="w", padx=10, pady=(5,0))

    combo_tema = ctk.CTkComboBox(campos_frame, values=["Outros", "Atendimento", "Filmes", "Estrutura"])
    combo_tema.pack(padx=10, pady=3, fill="x")

    label_desc = ctk.CTkLabel(campos_frame, text="Descreva sua sugestão (obrigatório)",
                              font=fonte_global if fonte_global else ("Arial", 10))
    label_desc.pack(anchor="w", padx=10, pady=(5,0))

    texto_sugestao = ctk.CTkTextbox(campos_frame, height=80)
    texto_sugestao.pack(padx=10, pady=3, fill="both", expand=True)

    switch_ident = ctk.CTkSwitch(campos_frame, text="Não", command=toggle_ident,
                                 font=fonte_global if fonte_global else ("Arial", 10))
    switch_ident.pack(anchor="w", padx=10, pady=5)

    # ===== BOTÕES =====
    botoes_frame = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    botoes_frame.pack(fill="x", padx=15, pady=10)

    btn_enviar = ctk.CTkButton(botoes_frame, text="ENVIAR SUGESTÃO", command=enviar_sugestao,
                               font=fonte_global if fonte_global else ("Arial", 12, "bold"),
                               fg_color=BTN_COLOR,
                               hover_color=BTN_HOVER,
                               text_color=BTN_TEXT,
                               height=35)
    btn_enviar.pack(side="left", padx=5, fill="x", expand=True)

    btn_voltar = ctk.CTkButton(botoes_frame, text="VOLTAR", 
                              font=fonte_global if fonte_global else ("Arial", 12, "bold"),
                              fg_color="#555555",
                              hover_color="#777777",
                              text_color="white",
                              height=35,
                              command=voltar_callback if voltar_callback else parent.destroy)
    btn_voltar.pack(side="left", padx=5, fill="x", expand=True)

    return frame

