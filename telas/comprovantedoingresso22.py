import customtkinter as ctk
from tkinter import messagebox
from reportlab.lib.pagesizes import A5, landscape
from reportlab.pdfgen import canvas
from datetime import datetime
import os

# === CONFIGURAÇÕES INICIAIS ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# === FUNÇÃO PARA GERAR COMPROVANTE PDF ===
def gerar_comprovante(filme, horario, assentos, preco_por_assento=25.00, logo_path="logo.png"):
    total = len(assentos) * preco_por_assento
    nome_arquivo = f"Comprovante_{filme.replace(' ', '_')}_{datetime.now().strftime('%H%M%S')}.pdf"

    c = canvas.Canvas(nome_arquivo, pagesize=landscape(A5))

    # === LOGO DO CINEPLUS ===
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 70, 270, width=100, height=100, mask='auto')

    # === TÍTULO DO CINEMA ===
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(100, 350, "🎬 CinePlus - Comprovante de Ingresso 🎬")
    c.line(50, 340, 550, 340)

    # === DADOS DO FILME ===
    c.setFont("Helvetica", 14)
    c.drawString(100, 290, f"Filme: {filme}")
    c.drawString(100, 260, f"Horário: {horario}")
    c.drawString(100, 230, f"Assentos: {', '.join(assentos)}")
    c.drawString(100, 200, f"Preço por assento: R$ {preco_por_assento:.2f}")
    c.drawString(100, 170, f"Total: R$ {total:.2f}")
    c.drawString(100, 140, f"Data da compra: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # === RODAPÉ ===
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(420, 110, "Apresente este comprovante na entrada da sessão.")
    c.drawCentredString(420, 90, "Agradecemos sua preferência! Bom filme! 🍿")

    c.save()
    messagebox.showinfo("Sucesso", f"Comprovante gerado com sucesso!\nArquivo: {nome_arquivo}")

# === JANELA PRINCIPAL ===
app = ctk.CTk()
app.title("CinePlus - Seleção de Assentos")
app.geometry("900x600")

filme = "O Senhor dos Anéis"
horario = "18:00"
preco = 25.00

assentos_disponiveis = []
assentos_ocupados = ["A1", "B3", "C5", "D2", "E7", "F4", "G6"]
assentos_selecionados = []

def selecionar_assento(assento, botao):
    if assento in assentos_ocupados:
        messagebox.showwarning("Assento Ocupado", f"O assento {assento} já está ocupado.")
        return

    if assento in assentos_selecionados:
        assentos_selecionados.remove(assento)
        botao.configure(fg_color="gray")
    else:
        assentos_selecionados.append(assento)
        botao.configure(fg_color="green")

frame = ctk.CTkFrame(master=app)
frame.pack(padx=20, pady=20, fill="both", expand=True)

titulo = ctk.CTkLabel(frame, text=f"{filme}\nHorário: {horario}", font=("Arial", 20, "bold"))
titulo.pack(pady=10)

grid_frame = ctk.CTkFrame(master=frame)
grid_frame.pack(pady=10)

linhas = ["A", "B", "C", "D", "E", "F", "G"]
colunas = range(1, 9)
botao_ref = {}

for i, linha in enumerate(linhas):
    for j, coluna in enumerate(colunas):
        assento = f"{linha}{coluna}"
        cor = "gray"
        if assento in assentos_ocupados:
            cor = "red"

        botao = ctk.CTkButton(
            master=grid_frame,
            text=assento,
            width=50,
            height=40,
            fg_color=cor,
            command=lambda a=assento: selecionar_assento(a, botao_ref[a])
        )
        botao.grid(row=i, column=j, padx=5, pady=5)
        botao_ref[assento] = botao

def confirmar_compra():
    if not assentos_selecionados:
        messagebox.showwarning("Aviso", "Selecione pelo menos um assento antes de confirmar.")
        return
    gerar_comprovante(filme, horario, assentos_selecionados, preco, "logo.png")

btn_confirmar = ctk.CTkButton(master=frame, text="Confirmar Compra", fg_color="gold", text_color="black", command=confirmar_compra)
btn_confirmar.pack(pady=20)

app.mainloop()
