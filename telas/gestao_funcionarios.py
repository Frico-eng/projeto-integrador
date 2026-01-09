# gestao_funcionarios.py
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from crud.crud_usuario import inserir_usuario, listar_usuarios, editar_usuario, excluir_usuario

def criar_tela_gestao_funcionarios(parent, voltar_callback):
    """Cria a tela de gerenciamento de funcionários para gerentes"""

    # ================== VARIÁVEIS ==================
    usuarios = []
    usuario_selecionado_id = None

    # ================== FUNÇÕES ==================
    def carregar_usuarios():
        nonlocal usuarios
        usuarios = listar_usuarios()
        # Filtrar apenas funcionários
        usuarios = [u for u in usuarios if u.get('Tipo_Usuario') == 'funcionario']
        atualizar_lista()

    def atualizar_lista():
        listbox.delete(0, "end")
        for usuario in usuarios:
            listbox.insert(
                "end",
                f"{usuario['ID_Usuario']}. {usuario['Nome_Usuario']} - {usuario['Email']} ({usuario['Tipo_Usuario']})"
            )

    def cadastrar_usuario():
        nome = entry_nome.get().strip()
        nome_login = entry_nome_login.get().strip()
        senha = entry_senha.get().strip()
        email = entry_email.get().strip()
        telefone = entry_telefone.get().strip()
        genero = entry_genero.get().strip()
        data_nascimento = entry_data_nascimento.get().strip()
        tipo_usuario = 'funcionario'  # Sempre funcionário

        if not all([nome, nome_login, senha, email]):
            messagebox.showwarning("Campos obrigatórios", "Preencha pelo menos nome, nome de login, senha e email!")
            return

        if inserir_usuario(nome, nome_login, senha, email, telefone, genero, data_nascimento, tipo_usuario):
            messagebox.showinfo("Sucesso", f"Funcionário '{nome}' cadastrado com sucesso!")
            carregar_usuarios()
            limpar_campos()
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar funcionário!")

    def limpar_campos():
        nonlocal usuario_selecionado_id
        for entry in [
            entry_nome, entry_nome_login, entry_senha,
            entry_email, entry_telefone, entry_genero, entry_data_nascimento
        ]:
            entry.delete(0, "end")
        usuario_selecionado_id = None

    def selecionar_usuario(event=None):
        nonlocal usuario_selecionado_id
        try:
            indice = listbox.curselection()[0]
            usuario = usuarios[indice]
            usuario_selecionado_id = usuario['ID_Usuario']

            # Limpar campos
            entry_nome.delete(0, "end")
            entry_nome_login.delete(0, "end")
            entry_senha.delete(0, "end")
            entry_email.delete(0, "end")
            entry_telefone.delete(0, "end")
            entry_genero.delete(0, "end")
            entry_data_nascimento.delete(0, "end")

            # Preencher campos
            entry_nome.insert(0, usuario.get("Nome_Usuario", ""))
            entry_nome_login.insert(0, usuario.get("Nome_Login", ""))
            entry_senha.insert(0, usuario.get("Senha", ""))
            entry_email.insert(0, usuario.get("Email", ""))
            entry_telefone.insert(0, usuario.get("Telefone", ""))
            entry_genero.insert(0, usuario.get("Genero", ""))
            entry_data_nascimento.insert(0, str(usuario.get("Data_Nascimento", "")))
        except IndexError:
            pass

    def editar_usuario_selecionado():
        nonlocal usuario_selecionado_id

        if not usuario_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um funcionário para editar.")
            return

        nome = entry_nome.get().strip()
        nome_login = entry_nome_login.get().strip()
        senha = entry_senha.get().strip()
        email = entry_email.get().strip()
        telefone = entry_telefone.get().strip()
        genero = entry_genero.get().strip()
        data_nascimento = entry_data_nascimento.get().strip()
        tipo_usuario = 'funcionario'

        if not all([nome, nome_login, senha, email]):
            messagebox.showwarning("Campos obrigatórios", "Preencha pelo menos nome, nome de login, senha e email!")
            return

        if editar_usuario(usuario_selecionado_id, nome, nome_login, senha, email, telefone, genero, data_nascimento, tipo_usuario):
            messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
            carregar_usuarios()
            limpar_campos()
        else:
            messagebox.showerror("Erro", "Erro ao atualizar funcionário!")

    def remover_usuario():
        nonlocal usuario_selecionado_id

        if not usuario_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um funcionário para remover.")
            return

        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover este funcionário?"):
            if excluir_usuario(usuario_selecionado_id):
                messagebox.showinfo("Removido", "Funcionário removido com sucesso!")
                carregar_usuarios()
                limpar_campos()
            else:
                messagebox.showerror("Erro", "Erro ao remover funcionário!")

    # ================== INTERFACE ==================
    frame = ctk.CTkFrame(parent, fg_color="transparent")

    # Título
    titulo_frame = ctk.CTkFrame(frame, fg_color="transparent")
    titulo_frame.pack(pady=20)

    ctk.CTkLabel(
        titulo_frame,
        text="👥 Gestão de Funcionários",
        font=("Arial", 24, "bold")
    ).pack()

    ctk.CTkLabel(
        titulo_frame,
        text="Cadastre, edite ou remova funcionários",
        font=("Arial", 14),
        text_color="gray"
    ).pack(pady=5)

    # Frame do formulário
    frame_form = ctk.CTkFrame(frame)
    frame_form.pack(pady=20, padx=20, fill="x")

    # ===== CAMPOS DE TEXTO =====
    ctk.CTkLabel(frame_form, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_nome = ctk.CTkEntry(frame_form, width=300)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form, text="Nome de Login:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_nome_login = ctk.CTkEntry(frame_form, width=300)
    entry_nome_login.grid(row=1, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form, text="Senha:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_senha = ctk.CTkEntry(frame_form, width=300, show="*")
    entry_senha.grid(row=2, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form, text="Email:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_email = ctk.CTkEntry(frame_form, width=300)
    entry_email.grid(row=3, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form, text="Telefone:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_telefone = ctk.CTkEntry(frame_form, width=300)
    entry_telefone.grid(row=4, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form, text="Gênero:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    entry_genero = ctk.CTkEntry(frame_form, width=300)
    entry_genero.grid(row=5, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form, text="Data de Nascimento:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
    entry_data_nascimento = ctk.CTkEntry(frame_form, width=300)
    entry_data_nascimento.grid(row=6, column=1, padx=10, pady=5)

    # ==== BOTÕES ====
    frame_botoes = ctk.CTkFrame(frame)
    frame_botoes.pack(pady=10)

    ctk.CTkButton(frame_botoes, text="Cadastrar", command=cadastrar_usuario).grid(row=0, column=0, padx=10)
    ctk.CTkButton(frame_botoes, text="Editar", command=editar_usuario_selecionado).grid(row=0, column=1, padx=10)
    ctk.CTkButton(frame_botoes, text="Remover", command=remover_usuario).grid(row=0, column=2, padx=10)
    ctk.CTkButton(frame_botoes, text="Limpar Campos", command=limpar_campos).grid(row=0, column=3, padx=10)
    ctk.CTkButton(frame_botoes, text="Atualizar Lista", command=carregar_usuarios).grid(row=0, column=4, padx=10)

    # Botão voltar
    ctk.CTkButton(frame_botoes, text="Voltar ao Menu", command=voltar_callback).grid(row=0, column=5, padx=10)

    # ==== LISTA DE FUNCIONÁRIOS ====
    frame_lista = ctk.CTkFrame(frame)
    frame_lista.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(frame_lista, text="Funcionários cadastrados:", font=("Arial", 16)).pack(pady=10)

    listbox = tk.Listbox(frame_lista, height=10, bg="#2b2b2b", fg="white",
                        selectbackground="#1f6aa5", font=("Arial", 12))
    listbox.pack(fill="both", expand=True, padx=10, pady=10)
    listbox.bind("<<ListboxSelect>>", selecionar_usuario)

    # Carregar usuários ao iniciar
    carregar_usuarios()

    return frame