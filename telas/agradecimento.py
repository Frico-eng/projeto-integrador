# telas/agradecimento.py
import customtkinter as ctk
from PIL import Image, ImageTk
import utilidades.config as config
from utilidades.session import logout as session_logout
from utilidades.ui_helpers import alternar_tema
from utilidades.config import BTN_COLOR, BTN_HOVER, BTN_TEXT
import utilidades.config as config_module
import os
import threading
import time

def mostrar_tela_agradecimento(parent, dados_compra=None, voltar_callback=None, feedback_callback=None, fonte_global=None):
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
    frame = ctk.CTkFrame(parent, fg_color=config.COR_FUNDO, width=1800, height=1200)
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
        width=700,
        height=1000
    )
    container_principal.place(relx=0.5, rely=0.5, anchor="center")
    container_principal.pack_propagate(False)

    # ====== CABEÇALHO ======
    header_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    header_frame.pack(fill="x", pady=(20, 12), padx=20)

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
    titulo_agradecimento = ctk.CTkLabel(
        header_frame,
        text="✅ Pagamento Confirmado",
        font=fonte_global if fonte_global else ("Arial", 24, "bold"),
        text_color="#27AE60"
    )
    titulo_agradecimento.pack(pady=5)

    # Se não foi passada `fonte_global`, tentar ler de main.fonte_global
    if fonte_global is None:
        try:
            import main as main_mod
            fonte_global = getattr(main_mod, "fonte_global", None)
        except Exception:
            fonte_global = None

    # Controles de fonte no canto superior direito do header
    def aumentar_fonte():
        nonlocal current_font_size
        if fonte_global:
            if fonte_global.cget("size") < 22:
                fonte_global.configure(size=fonte_global.cget("size") + 2)
        else:
            if current_font_size < 22:
                current_font_size += 2
                aplicar_fonte_local()

    def diminuir_fonte():
        nonlocal current_font_size
        if fonte_global:
            if fonte_global.cget("size") > 6:
                fonte_global.configure(size=fonte_global.cget("size") - 2)
        else:
            if current_font_size > 6:
                current_font_size -= 2
                aplicar_fonte_local()
    
    # Função para atualizar cores baseado no tema
    def atualizar_cores_tema():
        tema_escuro = config_module.tema_atual == "dark"
        
        if tema_escuro:
            bg_color = config.COR_FUNDO
            container_color = "#2B2B2B"
            text_color = "white"
        else:
            bg_color = "#F0F0F0"
            container_color = "#E8E8E8"
            text_color = "black"
        
        # Atualizar cores dos elementos
        frame.configure(fg_color=bg_color)
        container_principal.configure(fg_color=container_color)
        titulo_agradecimento.configure(text_color=text_color)
        mensagem_label.configure(text_color=text_color)
        label_timer.configure(text_color=text_color)

    # Frame para os controles (sempre visível)
    frame_controle_fonte = ctk.CTkFrame(header_frame, fg_color="transparent")
    frame_controle_fonte.pack(side="right")
    ctk.CTkButton(frame_controle_fonte, text="A+", command=aumentar_fonte, width=50, font=fonte_global if fonte_global else None).pack(side="left", padx=5)
    ctk.CTkButton(frame_controle_fonte, text="A-", command=diminuir_fonte, width=50, font=fonte_global if fonte_global else None).pack(side="left", padx=5)
    
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
    
    mensagem_label = ctk.CTkLabel(
        content_frame,
        text=mensagem,
        font=("Arial", 16),
        text_color=config.COR_TEXTO,
        fg_color="transparent",
        justify="center"
    )
    mensagem_label.pack(expand=True, pady=10)

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

    # Aplicar tema inicial
    atualizar_cores_tema()

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
        
        # Fazer logout do usuário quando voltar ao início
        try:
            session_logout()
        except Exception:
            pass

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

    # Fonte local quando fonte_global não for fornecida
    current_font_size = fonte_global.cget("size") if fonte_global else 14

    def aplicar_fonte_local():
        fs = current_font_size
        try:
            for w in container_principal.winfo_children():
                try:
                    w.configure(font=("Arial", fs))
                except Exception:
                    pass
                try:
                    for c in w.winfo_children():
                        try:
                            c.configure(font=("Arial", fs))
                        except Exception:
                            pass
                        try:
                            for d in c.winfo_children():
                                try:
                                    d.configure(font=("Arial", fs))
                                except Exception:
                                    pass
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception:
            pass

    # Aplicar fonte inicial
    aplicar_fonte_local()

    return frame