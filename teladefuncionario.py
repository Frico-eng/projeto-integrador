import tkinter as tk
from tkinter import ttk, messagebox

# ============================================================
#   ESTILO DOS CAMPOS (TTK)
# ============================================================

def configurar_ttk():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "TEntry",
        foreground="white",
        fieldbackground="#2a2a2a",
        background="#2a2a2a",
        bordercolor="#555555",
        lightcolor="#555555",
        darkcolor="#555555",
        borderwidth=2,
        relief="flat",
        padding=6
    )


# ============================================================
#   BOTÃO ESTILO "PILL" (IGUAL À SUA IMAGEM)
# ============================================================

def criar_botao_pill(janela, texto, comando=None, icone=None):
    frame = tk.Frame(janela, bg="#1d1d1d")
    canvas = tk.Canvas(frame, width=170, height=50, bg="#1d1d1d",
                       highlightthickness=0)
    canvas.pack()

    cor_normal = "#F4B544"
    cor_hover = "#d89b37"

    # Botão arredondado estilo "pílula"
    def desenhar(cor):
        canvas.delete("all")

        # círculos das extremidades
        canvas.create_oval(5, 5, 45, 45, fill=cor, outline=cor)
        canvas.create_oval(125, 5, 165, 45, fill=cor, outline=cor)

        # retângulo central
        canvas.create_rectangle(25, 5, 145, 45, fill=cor, outline=cor)

        # Ícone (emoji opcional)
        if icone:
            canvas.create_text(40, 25, text=icone, font=("Arial", 14), fill="black")
            canvas.create_text(105, 25, text=texto, font=("Arial", 12, "bold"), fill="black")
        else:
            canvas.create_text(85, 25, text=texto, font=("Arial", 12, "bold"), fill="black")

    desenhar(cor_normal)

    # Eventos
    def on_enter(event):
        desenhar(cor_hover)

    def on_leave(event):
        desenhar(cor_normal)

    def on_click(event):
        if comando:
            comando()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)

    return frame


# ============================================================
#   TELA DE LOGIN
# ============================================================

def tela_login():
    janela = tk.Tk()
    janela.title("Login - Funcionário")
    janela.geometry("450x500")
    janela.configure(bg="#1d1d1d")

    configurar_ttk()

    tk.Label(janela, text="Login do Funcionário", font=("Arial", 22, "bold"),
             bg="#1d1d1d", fg="white").pack(pady=25)

    usuario = ttk.Entry(janela, width=40)
    usuario.insert(0, "(login)")
    usuario.pack(pady=12)

    senha = ttk.Entry(janela, width=40, show="*")
    senha.insert(0, "Senha")
    senha.pack(pady=12)

    def entrar():
        messagebox.showinfo("Login", "Login enviado!")

    # Botões estilo imagem
    botao_entrar = criar_botao_pill(janela, "Entrar", comando=entrar, icone="🔐")
    botao_entrar.pack(pady=15)

    botao_cadastro = criar_botao_pill(
        janela,
        "Cadastrar",
        comando=lambda: [janela.destroy(), tela_cadastro()],
        icone="📝"
    )
    botao_cadastro.pack(pady=8)

    janela.mainloop()


# ============================================================
#   TELA DE CADASTRO DE FUNCIONÁRIO
# ============================================================

def tela_cadastro():
    janela = tk.Tk()
    janela.title("Cadastro - Funcionário")
    janela.geometry("480x600")
    janela.configure(bg="#1d1d1d")

    configurar_ttk()

    tk.Label(janela, text="Cadastro de Funcionário", font=("Arial", 22, "bold"),
             bg="#1d1d1d", fg="white").pack(pady=20)

    campos = [
        "Nome completo",
        "Telefone",
        "Email",
        "Usuário (login)",
        "Senha"
    ]

    entradas = {}
    for campo in campos:
        e = ttk.Entry(janela, width=45)
        e.insert(0, campo)
        e.pack(pady=10)
        entradas[campo] = e

    def cadastrar():
        messagebox.showinfo("Cadastro", "Funcionário cadastrado com sucesso!")

    # Botões estilo imagem
    botao_registrar = criar_botao_pill(
        janela,
        "Registrar",
        comando=cadastrar,
        icone="📋"
    )
    botao_registrar.pack(pady=15)

    botao_voltar = criar_botao_pill(
        janela,
        "Voltar",
        comando=lambda: [janela.destroy(), tela_login()],
        icone="↩️"
    )
    botao_voltar.pack(pady=5)

    janela.mainloop()


# ============================================================
#   EXECUTAR PROGRAMA
# ============================================================

if __name__ == "__main__":
    tela_login()
