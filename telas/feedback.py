import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Sobe para a pasta pai de 'telas'
IMAGE_DIR = os.path.join(BASE_DIR, "utilidades", "images")
FEEDBACK_IMAGE_PATH = os.path.join(IMAGE_DIR, "feedback.png")


def criar_tela_feedback(parent, voltar_callback=None):
    """Cria e retorna o frame da tela de feedback"""
   
    frame = ctk.CTkFrame(parent, fg_color="transparent")
   
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
    try:
        logo_img = ctk.CTkImage(
            light_image=Image.open(FEEDBACK_IMAGE_PATH),
            dark_image=Image.open(FEEDBACK_IMAGE_PATH),
            size=(150,150)
        )
        logo_label = ctk.CTkLabel(frame, image=logo_img, text="")
        logo_label.pack(pady=20)
    except Exception as e:
        print(f"Erro ao carregar imagem do feedback: {e}")
        # Fallback: label textual se a imagem não carregar
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

