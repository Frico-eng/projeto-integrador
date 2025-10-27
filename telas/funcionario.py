# cineplus_crud.py (parte atualizada)
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from crud.crud_filme import inserir_filme, listar_filmes, editar_filme, excluir_filme

def criar_tela_funcionario(parent, voltar_callback):
    """Cria a tela de gerenciamento de filmes para funcionários"""
    
    # ================== VARIÁVEIS ==================
    filmes = []
    imagem_atual = None
    filme_selecionado_id = None

    # ================== FUNÇÕES ==================
    def carregar_filmes():
        nonlocal filmes
        filmes = listar_filmes()
        atualizar_lista()

    def atualizar_lista():
        listbox.delete(0, "end")
        for filme in filmes:
            listbox.insert(
                "end",
                f"{filme['ID_Filme']}. {filme['Titulo_Filme']} - {filme['Genero']} ({filme['Duracao']} min)"
            )

    def selecionar_imagem():
        nonlocal imagem_atual
        caminho = filedialog.askopenfilename(
            title="Selecionar imagem do filme",
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.webp")]
        )
        if caminho:
            imagem_atual = caminho
            try:
                img = Image.open(caminho)
                img = img.resize((120, 180))
                img_preview = ImageTk.PhotoImage(img)
                label_imagem.configure(image=img_preview, text="")
                label_imagem.image = img_preview
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar imagem: {e}")

    def cadastrar_filme():
        nonlocal imagem_atual
        titulo = entry_titulo.get().strip()
        genero = entry_genero.get().strip()
        duracao = entry_duracao.get().strip()
        classificacao = entry_classificacao.get().strip()

        if not all([titulo, genero, duracao, classificacao]):
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
            return

        # Definir o caminho da imagem
        cartaz_path = None
        if imagem_atual:
            # Aqui você pode implementar a lógica para copiar a imagem para a pasta do projeto
            # Por enquanto, vamos apenas salvar o caminho original
            cartaz_path = imagem_atual

        if inserir_filme(titulo, genero, int(duracao), classificacao, cartaz_path):
            messagebox.showinfo("Sucesso", f"Filme '{titulo}' cadastrado com sucesso!")
            carregar_filmes()
            limpar_campos()
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar filme!")

    def limpar_campos():
        nonlocal imagem_atual, filme_selecionado_id
        for entry in [
            entry_titulo, entry_genero, entry_duracao,
            entry_classificacao
        ]:
            entry.delete(0, "end")
        imagem_atual = None
        filme_selecionado_id = None
        label_imagem.configure(image=None, text="(sem imagem)")

    def selecionar_filme(event=None):
        nonlocal filme_selecionado_id
        try:
            indice = listbox.curselection()[0]
            filme = filmes[indice]
            filme_selecionado_id = filme['ID_Filme']

            entry_titulo.delete(0, "end")
            entry_genero.delete(0, "end")
            entry_duracao.delete(0, "end")
            entry_classificacao.delete(0, "end")

            entry_titulo.insert(0, filme["Titulo_Filme"])
            entry_genero.insert(0, filme["Genero"])
            entry_duracao.insert(0, str(filme["Duracao"]))
            entry_classificacao.insert(0, filme["Classificacao"])

            # Carregar imagem se existir
            if filme.get("Cartaz_Path"):
                try:
                    img = Image.open(filme["Cartaz_Path"])
                    img = img.resize((120, 180))
                    img_preview = ImageTk.PhotoImage(img)
                    label_imagem.configure(image=img_preview, text="")
                    label_imagem.image = img_preview
                except Exception as e:
                    label_imagem.configure(image=None, text="(erro ao carregar)")
            else:
                label_imagem.configure(image=None, text="(sem imagem)")
        except IndexError:
            pass

    def editar_filme():
        nonlocal imagem_atual, filme_selecionado_id
        
        if not filme_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um filme para editar.")
            return

        titulo = entry_titulo.get().strip()
        genero = entry_genero.get().strip()
        duracao = entry_duracao.get().strip()
        classificacao = entry_classificacao.get().strip()

        if not all([titulo, genero, duracao, classificacao]):
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
            return

        # Usar o caminho da imagem atual (se foi selecionada uma nova)
        cartaz_path = imagem_atual if imagem_atual else None

        if editar_filme(filme_selecionado_id, titulo, genero, int(duracao), classificacao, cartaz_path):
            messagebox.showinfo("Sucesso", "Filme atualizado com sucesso!")
            carregar_filmes()
            limpar_campos()
        else:
            messagebox.showerror("Erro", "Erro ao atualizar filme!")

    def remover_filme():
        nonlocal filme_selecionado_id
        
        if not filme_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um filme para remover.")
            return

        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover este filme?"):
            if excluir_filme(filme_selecionado_id):
                messagebox.showinfo("Removido", "Filme removido com sucesso!")
                carregar_filmes()
                limpar_campos()
            else:
                messagebox.showerror("Erro", "Erro ao remover filme!")

    # ================== INTERFACE ==================
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    
    # Título
    titulo_frame = ctk.CTkFrame(frame, fg_color="transparent")
    titulo_frame.pack(pady=20)
    
    ctk.CTkLabel(
        titulo_frame, 
        text="🎬 Menu do Funcionário - Gerenciar Filmes", 
        font=("Arial", 24, "bold")
    ).pack()
    
    ctk.CTkLabel(
        titulo_frame,
        text="Cadastre, edite ou remova filmes do catálogo",
        font=("Arial", 14),
        text_color="gray"
    ).pack(pady=5)

    # Frame do formulário
    frame_form = ctk.CTkFrame(frame)
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

    # ==== IMAGEM ====
    frame_imagem = ctk.CTkFrame(frame_form)
    frame_imagem.grid(row=0, column=2, rowspan=4, padx=30, pady=5)

    label_imagem = ctk.CTkLabel(frame_imagem, text="(sem imagem)", width=120, height=180)
    label_imagem.pack(pady=5)
    ctk.CTkButton(frame_imagem, text="Selecionar Imagem", command=selecionar_imagem).pack(pady=5)

    # ==== BOTÕES ====
    frame_botoes = ctk.CTkFrame(frame)
    frame_botoes.pack(pady=10)

    ctk.CTkButton(frame_botoes, text="Cadastrar", command=cadastrar_filme).grid(row=0, column=0, padx=10)
    ctk.CTkButton(frame_botoes, text="Editar", command=editar_filme).grid(row=0, column=1, padx=10)
    ctk.CTkButton(frame_botoes, text="Remover", command=remover_filme).grid(row=0, column=2, padx=10)
    ctk.CTkButton(frame_botoes, text="Limpar Campos", command=limpar_campos).grid(row=0, column=3, padx=10)
    ctk.CTkButton(frame_botoes, text="Atualizar Lista", command=carregar_filmes).grid(row=0, column=4, padx=10)

    # Botão voltar
    ctk.CTkButton(frame_botoes, text="Voltar ao Menu", command=voltar_callback).grid(row=0, column=5, padx=10)

    # ==== LISTA DE FILMES ====
    frame_lista = ctk.CTkFrame(frame)
    frame_lista.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(frame_lista, text="Filmes cadastrados:", font=("Arial", 16)).pack(pady=10)

    listbox = tk.Listbox(frame_lista, height=10, bg="#2b2b2b", fg="white", 
                        selectbackground="#1f6aa5", font=("Arial", 12))
    listbox.pack(fill="both", expand=True, padx=10, pady=10)
    listbox.bind("<<ListboxSelect>>", selecionar_filme)

    # Carregar filmes ao iniciar
    carregar_filmes()

    return frame