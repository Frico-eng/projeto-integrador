import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

# ================== CONFIGURAÇÃO ==================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================== DADOS INICIAIS ==================
filmes = [
    {
        "titulo": "Predador Terras Selvagens",
        "genero": "Terror, Suspense, Aventura, Ficção Científica",
        "duracao": "98",
        "classificacao": "12",
        "horarios": ["17:30", "20:45", "21:15"],
        "tipo": ["Dublado", "Legendado"]
    },
    {
        "titulo": "Zootopia",
        "genero": "Animação, Comédia, Aventura",
        "duracao": "108",
        "classificacao": "L",
        "horarios": ["14:00", "16:30", "19:00"],
        "tipo": ["Dublado"]
    },
    {
        "titulo": "Matrix",
        "genero": "Ação, Ficção Científica",
        "duracao": "136",
        "classificacao": "16",
        "horarios": ["18:00", "21:00"],
        "tipo": ["Legendado"]
    },
    {
        "titulo": "Interstellar",
        "genero": "Drama, Ficção Científica",
        "duracao": "169",
        "classificacao": "10",
        "horarios": ["15:00", "19:00"],
        "tipo": ["Dublado", "Legendado"]
    },
    {
        "titulo": "Jumanji",
        "genero": "Aventura, Fantasia, Comédia",
        "duracao": "119",
        "classificacao": "10",
        "horarios": ["13:30", "16:00", "20:30"],
        "tipo": ["Dublado"]
    },
    {
        "titulo": "Demon Slayer - Castelo Infinito",
        "genero": "Ação, Animação, Fantasia",
        "duracao": "120",
        "classificacao": "14",
        "horarios": ["17:00", "20:00"],
        "tipo": ["Legendado"]
    },
    {
        "titulo": "Homem-Aranha Sem Volta Para Casa",
        "genero": "Ação, Aventura",
        "duracao": "148",
        "classificacao": "12",
        "horarios": ["14:30", "18:00", "21:00"],
        "tipo": ["Dublado", "Legendado"]
    },
    {
        "titulo": "Invocação do Mal",
        "genero": "Terror, Suspense",
        "duracao": "112",
        "classificacao": "16",
        "horarios": ["22:00"],
        "tipo": ["Legendado"]
    },
]

# ================== FUNÇÕES ==================
def atualizar_lista():
    listbox.delete(0, "end")
    for i, filme in enumerate(filmes, start=1):
        listbox.insert("end", f"{i}. {filme['titulo']} - {filme['genero']} ({filme['duracao']} min)")

def limpar_campos():
    for entry in (entry_titulo, entry_genero, entry_duracao, entry_classificacao, entry_horarios, entry_tipo):
        entry.delete(0, "end")

def cadastrar_filme():
    titulo = entry_titulo.get().strip()
    genero = entry_genero.get().strip()
    duracao = entry_duracao.get().strip()
    classificacao = entry_classificacao.get().strip()
    horarios = entry_horarios.get().strip().split(",")
    tipo = entry_tipo.get().strip().split(",")

    if not titulo or not genero or not duracao or not classificacao:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
        return

    filmes.append({
        "titulo": titulo,
        "genero": genero,
        "duracao": duracao,
        "classificacao": classificacao,
        "horarios": [h.strip() for h in horarios if h.strip()],
        "tipo": [t.strip() for t in tipo if t.strip()]
    })

    atualizar_lista()
    limpar_campos()
    messagebox.showinfo("Sucesso", f"Filme '{titulo}' cadastrado!")

def selecionar_filme(event=None):
    try:
        indice = listbox.curselection()[0]
        filme = filmes[indice]
        limpar_campos()
        entry_titulo.insert(0, filme["titulo"])
        entry_genero.insert(0, filme["genero"])
        entry_duracao.insert(0, filme["duracao"])
        entry_classificacao.insert(0, filme["classificacao"])
        entry_horarios.insert(0, ", ".join(filme["horarios"]))
        entry_tipo.insert(0, ", ".join(filme["tipo"]))
    except IndexError:
        pass

def editar_filme():
    try:
        indice = listbox.curselection()[0]
    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um filme para editar.")
        return

    novo_titulo = entry_titulo.get().strip()
    novo_genero = entry_genero.get().strip()
    nova_duracao = entry_duracao.get().strip()
    nova_classificacao = entry_classificacao.get().strip()
    novos_horarios = entry_horarios.get().strip().split(",")
    novo_tipo = entry_tipo.get().strip().split(",")

    if not novo_titulo or not novo_genero or not nova_duracao or not nova_classificacao:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
        return

    filmes[indice] = {
        "titulo": novo_titulo,
        "genero": novo_genero,
        "duracao": nova_duracao,
        "classificacao": nova_classificacao,
        "horarios": [h.strip() for h in novos_horarios if h.strip()],
        "tipo": [t.strip() for t in novo_tipo if t.strip()]
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
janela.geometry("800x600")

frame_form = ctk.CTkFrame(janela)
frame_form.pack(pady=20, padx=20, fill="x")

campos = [
    ("Título:", "entry_titulo"),
    ("Gênero:", "entry_genero"),
    ("Duração (min):", "entry_duracao"),
    ("Classificação:", "entry_classificacao"),
    ("Horários (separar por vírgula):", "entry_horarios"),
    ("Tipo (Dublado, Legendado):", "entry_tipo")
]

for i, (label, varname) in enumerate(campos):
    ctk.CTkLabel(frame_form, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
    entry = ctk.CTkEntry(frame_form, width=400)
    entry.grid(row=i, column=1, padx=10, pady=5)
    globals()[varname] = entry

frame_botoes = ctk.CTkFrame(janela)
frame_botoes.pack(pady=10)

ctk.CTkButton(frame_botoes, text="Cadastrar", command=cadastrar_filme).grid(row=0, column=0, padx=10)
ctk.CTkButton(frame_botoes, text="Editar", command=editar_filme).grid(row=0, column=1, padx=10)
ctk.CTkButton(frame_botoes, text="Remover", command=remover_filme).grid(row=0, column=2, padx=10)
ctk.CTkButton(frame_botoes, text="Limpar Campos", command=limpar_campos).grid(row=0, column=3, padx=10)

frame_lista = ctk.CTkFrame(janela)
frame_lista.pack(padx=20, pady=20, fill="both", expand=True)

ctk.CTkLabel(frame_lista, text="Filmes cadastrados:", font=("Arial", 16)).pack(pady=10)

listbox = tk.Listbox(frame_lista, height=10, bg="#2b2b2b", fg="white",
                     selectbackground="#1f6aa5", font=("Arial", 12))
listbox.pack(fill="both", expand=True, padx=10, pady=10)
listbox.bind("<<ListboxSelect>>", selecionar_filme)

atualizar_lista()
janela.mainloop()
