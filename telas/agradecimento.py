# telas/agradecimento.py
import customtkinter as ctk
from PIL import Image, ImageTk
import utilidades.config as config
import os
import threading
import time

def mostrar_tela_agradecimento(parent, dados_compra=None, voltar_callback=None, feedback_callback=None):
    """
    Mostra a tela de agradecimento dentro de um frame existente
    
    Args:
        parent: CTkFrame onde o conteúdo será exibido
        dados_compra: dicionário com informações da compra
        voltar_callback: função para voltar ao início
        feedback_callback: função para abrir tela de feedback
    """
    # Limpar frame pai
    for widget in parent.winfo_children():
        widget.destroy()

    # ====== VARIÁVEIS DE CONTROLE ======
    tempo_restante = 15  # 15 segundos para redirecionamento automático
    timer_ativo = True

    # ====== CONFIGURAR FRAME PRINCIPAL ======
    frame = ctk.CTkFrame(parent, fg_color=config.COR_FUNDO, width=1800, height=900)
    frame.pack_propagate(False)
    frame.pack(fill="both", expand=True)

    # ====== IMAGEM DE FUNDO ======
    agradecimento_path = os.path.join(config.IMAGE_DIR, "agradecimento.png")
    
    try:
        bg_image = Image.open(agradecimento_path)
        bg_photo = ctk.CTkImage(bg_image, size=(1800, 900))
        
        bg_label = ctk.CTkLabel(frame, image=bg_photo, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_photo
        
    except Exception as e:
        print(f"Erro ao carregar imagem de fundo: {e}")
        frame.configure(fg_color=config.COR_FUNDO)

    # ====== CONTAINER PRINCIPAL PARA CONTEÚDO ======
    container_principal = ctk.CTkFrame(
        frame, 
        fg_color="#2b2b2b",
        bg_color="transparent",
        corner_radius=20,
        width=550,  # Largura aumentada para botões
        height=700
    )
    container_principal.place(relx=0.5, rely=0.5, anchor="center")
    container_principal.pack_propagate(False)

    # ====== CABEÇALHO ======
    header_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    header_frame.pack(fill="x", pady=(40, 20), padx=40)

    # === LOGO CINEPLUS ===
    try:
        img_logo = Image.open(config.LOGO_PATH)
        img_logo = img_logo.resize((120, 120), Image.LANCZOS)
        logo_tk = ctk.CTkImage(img_logo, size=(120, 120))
        
        logo_label = ctk.CTkLabel(header_frame, image=logo_tk, text="", fg_color="transparent")
        logo_label.image = logo_tk
        logo_label.pack(pady=10)
    except Exception as e:
        print(f"Erro ao carregar logo: {e}")

    # === Mensagem de agradecimento ===
    ctk.CTkLabel(
        header_frame,
        text="✅ Pagamento Confirmado",
        font=("Arial", 24, "bold"),
        text_color="#27AE60"
    ).pack(pady=5)

    # ====== TIMER DE REDIRECIONAMENTO ======
    timer_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    timer_frame.pack(fill="x", pady=(0, 10), padx=40)

    label_timer = ctk.CTkLabel(
        timer_frame,
        text=f"Redirecionando em {tempo_restante} segundos...",
        font=("Arial", 12),
        text_color="#F6C148",
        fg_color="transparent"
    )
    label_timer.pack()

    # ====== MENSAGEM PRINCIPAL ======
    content_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)

    mensagem = (
        "Agradecemos seu pagamento!\n\n"
        "Seu ingresso foi reservado com sucesso.\n\n"
        "Qualquer dúvida estamos à disposição!\n\n"
        "🎬 Bom filme!"
    )
    
    ctk.CTkLabel(
        content_frame,
        text=mensagem,
        font=("Arial", 16),
        text_color=config.COR_TEXTO,
        fg_color="transparent",
        justify="center"
    ).pack(expand=True, pady=10)

    # ====== RESUMO DA COMPRA ======
    if dados_compra:
        resumo_frame = ctk.CTkFrame(content_frame, fg_color="#1C2732", corner_radius=10)
        resumo_frame.pack(fill="x", pady=10)
        
        filme_titulo = dados_compra.get('filme', {}).get('Titulo_Filme', 'Filme')
        assentos = ', '.join(dados_compra.get('assentos', []))
        total = dados_compra.get('total', 0)
        
        resumo_texto = f"📽️ {filme_titulo}\n🎫 Assentos: {assentos}\n💵 Total: R$ {total:.2f}"
        
        ctk.CTkLabel(
            resumo_frame,
            text=resumo_texto,
            font=("Arial", 14),
            text_color=config.COR_TEXTO,
            justify="left"
        ).pack(padx=15, pady=10)

    # ====== BOTÕES DE AÇÃO ======
    btn_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    btn_frame.pack(fill="x", pady=20, padx=40)

    # Botão Avaliar Experiência
    btn_feedback = ctk.CTkButton(
        btn_frame,
        text="⭐ Avaliar Experiência",
        width=250,
        height=45,
        command=lambda: abrir_feedback(),
        fg_color="#F39C12",
        hover_color="#E67E22",
        text_color="white",
        font=("Arial", 14, "bold"),
        corner_radius=10
    )
    btn_feedback.pack(pady=8)

    # Botão Voltar ao Início
    btn_voltar = ctk.CTkButton(
        btn_frame,
        text="🏠 Voltar para o Início",
        width=250,
        height=45,
        command=lambda: voltar_ao_inicio(),
        fg_color=config.COR_DESTAQUE,
        hover_color=config.BTN_HOVER,
        text_color=config.BTN_TEXT,
        font=("Arial", 14, "bold"),
        corner_radius=10
    )
    btn_voltar.pack(pady=8)

    # ====== FUNÇÕES ======
    def atualizar_timer():
        """Atualiza o timer a cada segundo"""
        nonlocal tempo_restante, timer_ativo
        
        if timer_ativo and tempo_restante > 0:
            tempo_restante -= 1
            label_timer.configure(text=f"Redirecionando em {tempo_restante} segundos...")
            frame.after(1000, atualizar_timer)
        elif timer_ativo and tempo_restante <= 0:
            voltar_ao_inicio()

    def voltar_ao_inicio():
        """Volta para a tela inicial"""
        nonlocal timer_ativo
        timer_ativo = False  # Para o timer
        
        if voltar_callback:
            voltar_callback()

    def abrir_feedback():
        """Abre a tela de feedback"""
        nonlocal timer_ativo
        timer_ativo = False  # Para o timer ao ir para feedback
        
        if feedback_callback:
            feedback_callback()

    # ====== INICIAR TIMER ======
    frame.after(1000, atualizar_timer)

    # Configurar fullscreen
    parent.master.attributes('-fullscreen', True)

    return frame