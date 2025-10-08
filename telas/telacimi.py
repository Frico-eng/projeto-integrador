import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

# ================== CONFIGURAÇÃO ==================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================== DADOS ==================
filmes = []
imagem_atual = None  # variável para armazenar o caminho da imagem temporariamente

# ================== FUNÇÕES ==================
def atualizar_lista():
    listbox.delete(0, "end")
    for i, filme in enumerate(filmes, start=1):
        listbox.insert(
            "end",
            f"{i}. {filme['titulo']} - {filme['genero']} ({filme['duracao']} min)"
        )

def selecionar_imagem():
    global imagem_atual, img_preview
    caminho = filedialog.askopenfilename(
        title="Selecionar imagem do filme",
        filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.webp")]
    )
    if caminho:
        imagem_atual = caminho
        img = Image.open(caminho)
        img = img.resize((120, 180))
        img_preview = ImageTk.PhotoImage(img)
        label_imagem.configure(image=img_preview, text="")
        label_imagem.image = img_preview

def cadastrar_filme():
    global imagem_atual
    titulo = entry_titulo.get().strip()
    genero = entry_genero.get().strip()
    duracao = entry_duracao.get().strip()
    classificacao = entry_classificacao.get().strip()
    direcao = entry_direcao.get().strip()
    lancamento = entry_lancamento.get().strip()

    if not all([titulo, genero, duracao, classificacao, direcao, lancamento]):
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
        return

    filmes.append({
        "titulo": titulo,
        "genero": genero,
        "duracao": duracao,
        "classificacao": classificacao,
        "direcao": direcao,
        "lancamento": lancamento,
        "imagem": imagem_atual
    })

    atualizar_lista()
    limpar_campos()
    messagebox.showinfo("Sucesso", f"Filme '{titulo}' cadastrado com sucesso!")

def limpar_campos():
    global imagem_atual
    for entry in [
        entry_titulo, entry_genero, entry_duracao,
        entry_classificacao, entry_direcao, entry_lancamento
    ]:
        entry.delete(0, "end")
    imagem_atual = None
    label_imagem.configure(image=None, text="(sem imagem)")

def selecionar_filme(event=None):
    try:
        indice = listbox.curselection()[0]
        filme = filmes[indice]

        entry_titulo.delete(0, "end")
        entry_genero.delete(0, "end")
        entry_duracao.delete(0, "end")
        entry_classificacao.delete(0, "end")
        entry_direcao.delete(0, "end")
        entry_lancamento.delete(0, "end")

        entry_titulo.insert(0, filme["titulo"])
        entry_genero.insert(0, filme["genero"])
        entry_duracao.insert(0, filme["duracao"])
        entry_classificacao.insert(0, filme["classificacao"])
        entry_direcao.insert(0, filme["direcao"])
        entry_lancamento.insert(0, filme["lancamento"])

        if filme.get("imagem"):
            img = Image.open(filme["imagem"])
            img = img.resize((120, 180))
            img_preview = ImageTk.PhotoImage(img)
            label_imagem.configure(image=img_preview, text="")
            label_imagem.image = img_preview
        else:
            label_imagem.configure(image=None, text="(sem imagem)")
    except IndexError:
        pass

def editar_filme():
    global imagem_atual
    try:
        indice = listbox.curselection()[0]
    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um filme para editar.")
        return

    novo_titulo = entry_titulo.get().strip()
    novo_genero = entry_genero.get().strip()
    nova_duracao = entry_duracao.get().strip()
    nova_classificacao = entry_classificacao.get().strip()
    nova_direcao = entry_direcao.get().strip()
    novo_lancamento = entry_lancamento.get().strip()

    if not all([novo_titulo, novo_genero, nova_duracao, nova_classificacao, nova_direcao, novo_lancamento]):
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
        return

    filmes[indice] = {
        "titulo": novo_titulo,
        "genero": novo_genero,
        "duracao": nova_duracao,
        "classificacao": nova_classificacao,
        "direcao": nova_direcao,
        "lancamento": novo_lancamento,
        "imagem": imagem_atual
    }

    atualizar_lista()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Filme atualizado com sucesso!")

def remover_filme():
    try:
        indice = listbox.curselection()[0]
        removido = filmes.pop(indice)
        atualizar_lista()
        limpar_campos()
        messagebox.showinfo("Removido", f"Filme '{removido['titulo']}' foi removido!")
    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um filme para remover.")

# ================== INTERFACE ==================
janela = ctk.CTk()
janela.title("Menu do Funcionário - Gerenciar Filmes")
janela.geometry("950x650")

frame_form = ctk.CTkFrame(janela)
frame_form.pack(pady=20, padx=20, fill="x")

# ===== CAMPOS DE TEXTO =====
ctk.CTkLabel(frame_form, text="Título:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_titulo = ctk.CTkEntry(frame_form, width=300)
entry_titulo.grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(frame_form, text="Gênero:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_genero = ctk.CTkEntry(frame_form, width=300)
entry_genero.grid(row=1, column=1, padx=10, pady=5)

ctk.CTkLabel(frame_form, text="Duração (min):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_duracao = ctk.CTkEntry(frame_form, width=300)
entry_duracao.grid(row=2, column=1, padx=10, pady=5)

ctk.CTkLabel(frame_form, text="Classificação:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_classificacao = ctk.CTkEntry(frame_form, width=300)
entry_classificacao.grid(row=3, column=1, padx=10, pady=5)

ctk.CTkLabel(frame_form, text="Direção:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_direcao = ctk.CTkEntry(frame_form, width=300)
entry_direcao.grid(row=4, column=1, padx=10, pady=5)

ctk.CTkLabel(frame_form, text="Data de Lançamento:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
entry_lancamento = ctk.CTkEntry(frame_form, width=300)
entry_lancamento.grid(row=5, column=1, padx=10, pady=5)

# ==== IMAGEM ====
frame_imagem = ctk.CTkFrame(frame_form)
frame_imagem.grid(row=0, column=2, rowspan=6, padx=30, pady=5)

label_imagem = ctk.CTkLabel(frame_imagem, text="(sem imagem)", width=120, height=180)
label_imagem.pack(pady=5)
ctk.CTkButton(frame_imagem, text="Selecionar Imagem", command=selecionar_imagem).pack(pady=5)

# ==== BOTÕES ====
frame_botoes = ctk.CTkFrame(janela)
frame_botoes.pack(pady=10)

ctk.CTkButton(frame_botoes, text="Cadastrar", command=cadastrar_filme).grid(row=0, column=0, padx=10)
ctk.CTkButton(frame_botoes, text="Editar", command=editar_filme).grid(row=0, column=1, padx=10)
ctk.CTkButton(frame_botoes, text="Remover", command=remover_filme).grid(row=0, column=2, padx=10)
ctk.CTkButton(frame_botoes, text="Limpar Campos", command=limpar_campos).grid(row=0, column=3, padx=10)

# ==== LISTA DE FILMES ====
frame_lista = ctk.CTkFrame(janela)
frame_lista.pack(padx=20, pady=20, fill="both", expand=True)

ctk.CTkLabel(frame_lista, text="Filmes cadastrados:", font=("Arial", 16)).pack(pady=10)

listbox = tk.Listbox(frame_lista, height=10, bg="#2b2b2b", fg="white", selectbackground="#1f6aa5", font=("Arial", 12))
listbox.pack(fill="both", expand=True, padx=10, pady=10)
listbox.bind("<<ListboxSelect>>", selecionar_filme)

janela.mainloop()
