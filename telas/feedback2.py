import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ===== Janela principal =====
app = ctk.CTk()
app.title("CinePlus - Caixa de Sugestões")
app.geometry("500x600")

# ===== FUNÇÕES =====
def fade_out():
    """Diminui gradualmente a opacidade e volta à tela de início."""
    alpha = app.attributes("-alpha")
    if alpha > 0:
        alpha -= 0.05
        app.attributes("-alpha", alpha)
        app.after(50, fade_out)   # chama de novo em 50 ms
    else:
        abrir_tela_inicio()

def abrir_tela_inicio():
    """Tela de início (login simples para exemplo)."""
    app.attributes("-alpha", 1.0)
    for w in app.winfo_children():
        w.destroy()

    ctk.CTkLabel(app, text="🎬 CINEPLUS", font=("Arial Bold", 28)).pack(pady=40)
    ctk.CTkLabel(app, text="Bem-vindo de volta!", font=("Arial", 18)).pack(pady=10)

    ctk.CTkButton(app, text="Sair", command=app.destroy).pack(pady=20)

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

def voltar():
    app.destroy()

def toggle_ident():
    switch_ident.configure(text="Sim" if switch_ident.get() else "Não")

# ===== LOGO =====
logo_img = ctk.CTkImage(
    light_image=Image.open("C:\\Users\\58682496\\Downloads\\githubteste\\feedback.png"),
    dark_image=Image.open("C:\\Users\\58682496\\Downloads\\githubteste\\feedback.png"),
    size=(150,150)
)
logo_label = ctk.CTkLabel(app, image=logo_img, text="")
logo_label.pack(pady=20)

titulo = ctk.CTkLabel(app,
                      text="CAIXA DE SUGESTÕES",
                      font=("Arial Bold", 20))
titulo.pack(pady=5)

subtitulo = ctk.CTkLabel(app,
    text="Envie uma sugestão para a sua área ou para a empresa:",
    font=("Arial", 14))
subtitulo.pack(pady=10)

# ===== CAMPOS =====
frame = ctk.CTkFrame(app)
frame.pack(pady=10, padx=20, fill="x")

label_tema = ctk.CTkLabel(frame, text="Tema da sugestão (obrigatório)")
label_tema.pack(anchor="w", padx=10, pady=(10,0))

combo_tema = ctk.CTkComboBox(frame, values=["Outros", "Atendimento", "Filmes", "Estrutura"])
combo_tema.pack(padx=10, pady=5, fill="x")

label_desc = ctk.CTkLabel(frame, text="Descreva sua sugestão (obrigatório)")
label_desc.pack(anchor="w", padx=10, pady=(10,0))

texto_sugestao = ctk.CTkTextbox(frame, height=150)
texto_sugestao.pack(padx=10, pady=5, fill="x")

switch_ident = ctk.CTkSwitch(frame, text="Não", command=toggle_ident)
switch_ident.pack(anchor="w", padx=10, pady=10)

# ===== BOTÕES =====
botoes_frame = ctk.CTkFrame(app, fg_color="transparent")
botoes_frame.pack(pady=20)

btn_enviar = ctk.CTkButton(botoes_frame, text="ENVIAR SUGESTÃO", command=enviar_sugestao)
btn_enviar.pack(side="left", padx=10)

btn_voltar = ctk.CTkButton(botoes_frame, text="VOLTAR", fg_color="gray", command=voltar)
btn_voltar.pack(side="left", padx=10)

app.mainloop()
