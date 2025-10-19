import customtkinter as ctk
from PIL import Image, ImageTk
import utilidades.config as config
import os

def mostrar_tela_agradecimento(parent, voltar_callback=None):
    """
    Mostra a tela de agradecimento dentro de um frame existente (não cria nova janela)
    
    Args:
        parent: CTkFrame onde o conteúdo será exibido
        voltar_callback: função a ser chamada ao clicar no botão "Voltar para o início"
    """
    # Limpar frame pai
    for widget in parent.winfo_children():
        widget.destroy()

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
        # Fallback para cor de fundo
        frame.configure(fg_color=config.COR_FUNDO)

    # ====== CONTAINER PRINCIPAL PARA CONTEÚDO ======
    container_principal = ctk.CTkFrame(
        frame, 
        fg_color="#2b2b2b",
        bg_color="transparent",
        corner_radius=20,
        width=500,
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

    # ====== MENSAGEM PRINCIPAL ======
    content_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)

    mensagem = (
        "Agradecemos seu pagamento!\n\n"
        "Qualquer dúvida estamos à disposição!\n\n"
        "🎬 Bom filme!"
    )
    
    ctk.CTkLabel(
        content_frame,
        text=mensagem,
        font=("Arial", 18),
        text_color=config.COR_TEXTO,
        fg_color="transparent",
        justify="center"
    ).pack(expand=True, pady=20)

    # ====== BOTÃO VOLTAR ======
    btn_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    btn_frame.pack(fill="x", pady=30, padx=40)

    ctk.CTkButton(
        btn_frame,
        text="Voltar para o Início",
        width=200,
        height=45,
        command=voltar_callback if voltar_callback else lambda: print("Voltar ao início clicado"),
        fg_color=config.COR_DESTAQUE,
        hover_color=config.BTN_HOVER,
        text_color=config.BTN_TEXT,
        font=("Arial", 16, "bold"),
        corner_radius=10
    ).pack(pady=10)

    # Configurar fullscreen
    parent.master.attributes('-fullscreen', True)

    return frame