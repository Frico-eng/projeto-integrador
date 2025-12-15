import customtkinter as ctk

# Configurações do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Criar a janela principal
app = ctk.CTk()
app.title("Controle de Fonte")
app.geometry("800x600")

# Criar fonte global usando CTkFont
fonte_global = ctk.CTkFont(family="Arial", size=14)

# Funções para aumentar/diminuir
def aumentar_fonte():
    fonte_global.configure(size=fonte_global.cget("size") + 2)

def diminuir_fonte():
    if fonte_global.cget("size") > 6:
        fonte_global.configure(size=fonte_global.cget("size") - 2)

# Botões para controle de fonte
frame_controle_fonte = ctk.CTkFrame(app)
frame_controle_fonte.pack(pady=5)

ctk.CTkButton(frame_controle_fonte, text="A+", command=aumentar_fonte, width=40).pack(side="left", padx=5)
ctk.CTkButton(frame_controle_fonte, text="A-", command=diminuir_fonte, width=40).pack(side="left", padx=5)

# Exemplo de label usando a fonte global
label_teste = ctk.CTkLabel(app, text="Texto de teste", font=fonte_global)
label_teste.pack(pady=20)

app.mainloop()
