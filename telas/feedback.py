import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from utilidades.ui_helpers import alternar_tema
from utilidades.config import BTN_COLOR, BTN_HOVER, BTN_TEXT
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Sobe para a pasta pai de 'telas'
IMAGE_DIR = os.path.join(BASE_DIR, "utilidades", "images")
FEEDBACK_IMAGE_PATH = os.path.join(IMAGE_DIR, "feedback.png")


def criar_tela_feedback(parent, voltar_callback=None, fonte_global=None):
    """Cria e retorna o frame da tela de feedback"""
   
    frame = ctk.CTkFrame(parent, fg_color="transparent")
   
    # Funções para aumentar/diminuir fonte se fonte_global for fornecida
    def aumentar_fonte():
        if fonte_global and fonte_global.cget("size") < 22:  # 14 + (4 * 2)
            fonte_global.configure(size=fonte_global.cget("size") + 2)

    def diminuir_fonte():
        if fonte_global and fonte_global.cget("size") > 6:  # 14 - (4 * 2)
            fonte_global.configure(size=fonte_global.cget("size") - 2)
   
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


    # ===== LOGO =====
    # Carregar imagem de feedback se existir, caso contrário usar placeholder
    try:
        if os.path.exists(FEEDBACK_IMAGE_PATH):
            img = Image.open(FEEDBACK_IMAGE_PATH).resize((150, 150), Image.LANCZOS)
        else:
            # Gerar placeholder simples
            img = Image.new('RGBA', (150, 150), (246, 193, 72, 255))
        logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
        logo_label = ctk.CTkLabel(frame, image=logo_img, text="")
        logo_label.pack(pady=20)
    except Exception as e:
        print(f"Erro ao carregar imagem do feedback: {e}")
        logo_label = ctk.CTkLabel(frame, text="💬", font=("Arial", 60))
        logo_label.pack(pady=20)


    titulo = ctk.CTkLabel(frame,
                          text="CAIXA DE SUGESTÕES",
                          font=("Arial Bold", 20))
    titulo.pack(pady=5)


    subtitulo = ctk.CTkLabel(frame,
        text="Envie uma sugestão para a sua área ou para a empresa:",
        font=("Arial", 14))
    subtitulo.pack(pady=10)


    # ===== CAMPOS =====
    campos_frame = ctk.CTkFrame(frame)
    campos_frame.pack(pady=10, padx=20, fill="x")


    label_tema = ctk.CTkLabel(campos_frame, text="Tema da sugestão (obrigatório)")
    label_tema.pack(anchor="w", padx=10, pady=(10,0))


    combo_tema = ctk.CTkComboBox(campos_frame, values=["Outros", "Atendimento", "Filmes", "Estrutura"])
    combo_tema.pack(padx=10, pady=5, fill="x")


    label_desc = ctk.CTkLabel(campos_frame, text="Descreva sua sugestão (obrigatório)")
    label_desc.pack(anchor="w", padx=10, pady=(10,0))


    texto_sugestao = ctk.CTkTextbox(campos_frame, height=150)
    texto_sugestao.pack(padx=10, pady=5, fill="x")


    switch_ident = ctk.CTkSwitch(campos_frame, text="Não", command=toggle_ident)
    switch_ident.pack(anchor="w", padx=10, pady=10)


    # ===== BOTÕES =====
    botoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
    botoes_frame.pack(pady=20)
    
    # Botões para controle de fonte
    if fonte_global:
        frame_controle_fonte = ctk.CTkFrame(botoes_frame, fg_color="transparent")
        frame_controle_fonte.pack(side="left", padx=(10, 20))
        ctk.CTkButton(frame_controle_fonte, text="A+", command=aumentar_fonte, width=50, font=fonte_global).pack(side="left", padx=5)
        ctk.CTkButton(frame_controle_fonte, text="A-", command=diminuir_fonte, width=50, font=fonte_global).pack(side="left", padx=5)
        
        # Botão para alternar tema claro e escuro
        botao_tema = ctk.CTkButton(
            frame_controle_fonte,
            text="🌙",
            command=lambda: alternar_tema(parent, botao_tema),
            width=50,
            font=fonte_global,
            fg_color=BTN_COLOR,
            hover_color=BTN_HOVER,
            text_color=BTN_TEXT
        )
        botao_tema.pack(side="left", padx=5)

    btn_enviar = ctk.CTkButton(botoes_frame, text="ENVIAR SUGESTÃO", command=enviar_sugestao)
    btn_enviar.pack(side="left", padx=10)


    btn_voltar = ctk.CTkButton(botoes_frame, text="VOLTAR", fg_color="gray",
                              command=voltar_callback if voltar_callback else parent.destroy)
    btn_voltar.pack(side="left", padx=10)


    return frame


# Código para teste individual (opcional)
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("CinePlus - Caixa de Sugestões")
    app.geometry("500x600")
   
    frame = criar_tela_feedback(app)
    frame.pack(fill="both", expand=True)
   
    app.mainloop()

