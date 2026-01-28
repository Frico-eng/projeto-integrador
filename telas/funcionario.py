# cineplus_crud.py (parte atualizada)
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from crud.crud_filme import inserir_filme, listar_filmes, editar_filme, excluir_filme
from crud.crud_sessao import inserir_sessao, listar_todas_sessoes, editar_sessao, excluir_sessao, buscar_sessao_por_id
from crud.crud_sala import listar_salas
from datetime import datetime
from utilidades.ui_helpers import alternar_tema
from utilidades.config import BTN_COLOR, BTN_HOVER, BTN_TEXT

def criar_tela_funcionario(parent, voltar_callback, fonte_global=None):
    """Cria a tela de gerenciamento para funcionários com abas para filmes e sessões"""
    
    # Funções para aumentar/diminuir fonte se fonte_global for fornecida
    def aumentar_fonte():
        if fonte_global and fonte_global.cget("size") < 22:  # 14 + (4 * 2)
            fonte_global.configure(size=fonte_global.cget("size") + 2)

    def diminuir_fonte():
        if fonte_global and fonte_global.cget("size") > 6:  # 14 - (4 * 2)
            fonte_global.configure(size=fonte_global.cget("size") - 2)
    
    # ================== VARIÁVEIS ==================
    filmes = []
    sessoes = []
    salas = []
    imagem_atual = None
    filme_selecionado_id = None
    sessao_selecionada_id = None

    # ================== FUNÇÕES DE FILMES ==================
    def carregar_filmes():
        nonlocal filmes
        filmes = listar_filmes()
        atualizar_lista_filmes()

    def atualizar_lista_filmes():
        listbox_filmes.delete(0, "end")
        for filme in filmes:
            listbox_filmes.insert(
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
        direcao = entry_direcao.get().strip()
        sinopse = text_sinopse.get("1.0", "end-1c").strip()

        if not all([titulo, genero, duracao, classificacao, direcao, sinopse]):
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
            return

        # Definir o caminho da imagem
        cartaz_path = None
        if imagem_atual:
            cartaz_path = imagem_atual

        if inserir_filme(titulo, genero, int(duracao), classificacao, direcao, sinopse, cartaz_path):
            messagebox.showinfo("Sucesso", f"Filme '{titulo}' cadastrado com sucesso!")
            carregar_filmes()
            limpar_campos_filmes()
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar filme!")

    def limpar_campos_filmes():
        nonlocal imagem_atual, filme_selecionado_id
        for entry in [
            entry_titulo, entry_genero, entry_duracao,
            entry_classificacao, entry_direcao
        ]:
            entry.delete(0, "end")
        text_sinopse.delete("1.0", "end")
        imagem_atual = None
        filme_selecionado_id = None
        label_imagem.configure(image=None, text="(sem imagem)")

    def selecionar_filme(event=None):
        nonlocal filme_selecionado_id
        try:
            indice = listbox_filmes.curselection()[0]
            filme = filmes[indice]
            filme_selecionado_id = filme['ID_Filme']

            # Limpar campos
            entry_titulo.delete(0, "end")
            entry_genero.delete(0, "end")
            entry_duracao.delete(0, "end")
            entry_classificacao.delete(0, "end")
            entry_direcao.delete(0, "end")
            text_sinopse.delete("1.0", "end")

            # Preencher campos
            entry_titulo.insert(0, filme["Titulo_Filme"])
            entry_genero.insert(0, filme["Genero"])
            entry_duracao.insert(0, str(filme["Duracao"]))
            entry_classificacao.insert(0, filme["Classificacao"])
            entry_direcao.insert(0, filme.get("Direcao", ""))
            text_sinopse.insert("1.0", filme.get("Sinopse", ""))

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

    def editar_filme_selecionado():
        nonlocal imagem_atual, filme_selecionado_id
        
        if not filme_selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um filme para editar.")
            return

        titulo = entry_titulo.get().strip()
        genero = entry_genero.get().strip()
        duracao = entry_duracao.get().strip()
        classificacao = entry_classificacao.get().strip()
        direcao = entry_direcao.get().strip()
        sinopse = text_sinopse.get("1.0", "end-1c").strip()

        if not all([titulo, genero, duracao, classificacao, direcao, sinopse]):
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
            return

        # Usar o caminho da imagem atual (se foi selecionada uma nova)
        cartaz_path = imagem_atual if imagem_atual else None

        if editar_filme(filme_selecionado_id, titulo, genero, int(duracao), classificacao, direcao, sinopse, cartaz_path):
            messagebox.showinfo("Sucesso", "Filme atualizado com sucesso!")
            carregar_filmes()
            limpar_campos_filmes()
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
                limpar_campos_filmes()
            else:
                messagebox.showerror("Erro", "Erro ao remover filme!")

    # ================== FUNÇÕES DE SESSÕES ==================
    def carregar_sessoes():
        nonlocal sessoes
        sessoes = listar_todas_sessoes()
        atualizar_lista_sessoes()

    def atualizar_lista_sessoes():
        listbox_sessoes.delete(0, "end")
        for sessao in sessoes:
            listbox_sessoes.insert(
                "end",
                f"{sessao['ID_Sessao']}. {sessao['Titulo_Filme']} - {sessao['Nome_Sala']} - {sessao['Data_Sessao']} {sessao.get('Hora_Formatada', sessao['Hora_Sessao'])} ({sessao['Tipo_Sessao']})"
            )

    def carregar_salas():
        nonlocal salas
        salas = listar_salas()
        # Atualizar combobox de salas
        combo_sala.configure(values=[f"{sala['ID_Sala']}. {sala['Nome_Sala']}" for sala in salas])

    def carregar_filmes_combo():
        filmes_combo = listar_filmes()
        combo_filme.configure(values=[f"{filme['ID_Filme']}. {filme['Titulo_Filme']}" for filme in filmes_combo])

    def cadastrar_sessao():
        try:
            # Extrair IDs dos combos
            filme_selecionado = combo_filme.get()
            sala_selecionada = combo_sala.get()
            data = entry_data.get().strip()
            hora = entry_hora.get().strip()
            tipo = combo_tipo.get()

            if not all([filme_selecionado, sala_selecionada, data, hora, tipo]):
                messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
                return

            # Extrair IDs
            id_filme = int(filme_selecionado.split('.')[0])
            id_sala = int(sala_selecionada.split('.')[0])

            # Validar formato da data
            try:
                datetime.strptime(data, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido. Use YYYY-MM-DD")
                return

            # Validar formato da hora
            try:
                datetime.strptime(hora, '%H:%M')
            except ValueError:
                messagebox.showerror("Erro", "Formato de hora inválido. Use HH:MM")
                return

            if inserir_sessao(id_filme, id_sala, data, hora, tipo):
                messagebox.showinfo("Sucesso", "Sessão cadastrada com sucesso!")
                carregar_sessoes()
                limpar_campos_sessoes()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar sessão!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar dados: {e}")

    def limpar_campos_sessoes():
        nonlocal sessao_selecionada_id
        combo_filme.set("")
        combo_sala.set("")
        entry_data.delete(0, "end")
        entry_hora.delete(0, "end")
        combo_tipo.set("")
        sessao_selecionada_id = None

    def selecionar_sessao(event=None):
        nonlocal sessao_selecionada_id
        try:
            indice = listbox_sessoes.curselection()[0]
            sessao = sessoes[indice]
            sessao_selecionada_id = sessao['ID_Sessao']

            # Preencher campos
            combo_filme.set(f"{sessao['ID_Filme']}. {sessao['Titulo_Filme']}")
            combo_sala.set(f"{sessao['ID_Sala']}. {sessao['Nome_Sala']}")
            
            # Formatar data
            data_sessao = sessao['Data_Sessao']
            if isinstance(data_sessao, str):
                entry_data.delete(0, "end")
                entry_data.insert(0, data_sessao)
            else:
                entry_data.delete(0, "end")
                entry_data.insert(0, data_sessao.strftime('%Y-%m-%d'))
            
            # Formatar hora
            hora_sessao = sessao['Hora_Sessao']
            if hasattr(hora_sessao, 'strftime'):
                entry_hora.delete(0, "end")
                entry_hora.insert(0, hora_sessao.strftime('%H:%M'))
            else:
                entry_hora.delete(0, "end")
                entry_hora.insert(0, str(hora_sessao))
            
            combo_tipo.set(sessao['Tipo_Sessao'])

        except IndexError:
            pass

    def editar_sessao_selecionada():
        if not sessao_selecionada_id:
            messagebox.showwarning("Atenção", "Selecione uma sessão para editar.")
            return

        try:
            # Extrair IDs dos combos
            filme_selecionado = combo_filme.get()
            sala_selecionada = combo_sala.get()
            data = entry_data.get().strip()
            hora = entry_hora.get().strip()
            tipo = combo_tipo.get()

            if not all([filme_selecionado, sala_selecionada, data, hora, tipo]):
                messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
                return

            # Extrair IDs
            id_filme = int(filme_selecionado.split('.')[0])
            id_sala = int(sala_selecionada.split('.')[0])

            # Validar formatos
            try:
                datetime.strptime(data, '%Y-%m-%d')
                datetime.strptime(hora, '%H:%M')
            except ValueError:
                messagebox.showerror("Erro", "Formato de data/hora inválido")
                return

            if editar_sessao(sessao_selecionada_id, id_filme, id_sala, data, hora, tipo):
                messagebox.showinfo("Sucesso", "Sessão atualizada com sucesso!")
                carregar_sessoes()
                limpar_campos_sessoes()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar sessão!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar dados: {e}")

    def remover_sessao():
        if not sessao_selecionada_id:
            messagebox.showwarning("Atenção", "Selecione uma sessão para remover.")
            return

        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover esta sessão?"):
            if excluir_sessao(sessao_selecionada_id):
                messagebox.showinfo("Removido", "Sessão removida com sucesso!")
                carregar_sessoes()
                limpar_campos_sessoes()
            else:
                messagebox.showerror("Erro", "Erro ao remover sessão!")

    # ================== INTERFACE ==================
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="both", expand=True)
    
    # Função para ajustar layout conforme tamanho da janela
    def ajustar_layout():
        window_width = frame.winfo_width()
        window_height = frame.winfo_height()
        
        if window_width < 1500:
            # Telas pequenas
            tabview.configure(width=max(300, window_width - 40))
            tabview.configure(height=max(280, int(window_height * 0.5)))
        else:
            # Telas grandes
            tabview.configure(width=900)
            tabview.configure(height=max(380, int(window_height * 0.55)))
    
    # Título
    titulo_frame = ctk.CTkFrame(frame, fg_color="transparent")
    titulo_frame.pack(pady=10)
    
    ctk.CTkLabel(
        titulo_frame, 
        text="🎬 Menu do Funcionário", 
        font=("Arial", 24, "bold")
    ).pack()
    
    ctk.CTkLabel(
        titulo_frame,
        text="Gerencie filmes e sessões do cinema",
        font=("Arial", 14),
        text_color="gray"
    ).pack(pady=5)
    
    # Botões para controle de fonte
    if fonte_global:
        frame_controle_fonte = ctk.CTkFrame(titulo_frame, fg_color="transparent")
        frame_controle_fonte.pack(side="top", padx=10, pady=5)
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

    # Abas - usar frame container para controlar tamanho
    frame_tabview = ctk.CTkFrame(frame, fg_color="transparent")
    frame_tabview.pack(pady=5, padx=20, fill="both", expand=False)
    
    tabview = ctk.CTkTabview(frame_tabview, width=900, height=400)
    tabview.pack(fill="x")
    
    # Aba Filmes
    tab_filmes = tabview.add("🎭 Filmes")
    
    # Frame do formulário de filmes
    frame_form_filmes = ctk.CTkFrame(tab_filmes)
    frame_form_filmes.pack(pady=10, padx=10, fill="x")

    # ===== CAMPOS DE TEXTO FILMES =====
    ctk.CTkLabel(frame_form_filmes, text="Título:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_titulo = ctk.CTkEntry(frame_form_filmes, width=300)
    entry_titulo.grid(row=0, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form_filmes, text="Gênero:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_genero = ctk.CTkEntry(frame_form_filmes, width=300)
    entry_genero.grid(row=1, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form_filmes, text="Duração (min):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_duracao = ctk.CTkEntry(frame_form_filmes, width=300)
    entry_duracao.grid(row=2, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form_filmes, text="Classificação:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_classificacao = ctk.CTkEntry(frame_form_filmes, width=300)
    entry_classificacao.grid(row=3, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form_filmes, text="Direção:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_direcao = ctk.CTkEntry(frame_form_filmes, width=300)
    entry_direcao.grid(row=4, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form_filmes, text="Sinopse:").grid(row=5, column=0, padx=10, pady=5, sticky="ne")
    text_sinopse = ctk.CTkTextbox(frame_form_filmes, width=300, height=100)
    text_sinopse.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    # ==== IMAGEM ====
    frame_imagem = ctk.CTkFrame(frame_form_filmes)
    frame_imagem.grid(row=0, column=2, rowspan=6, padx=30, pady=5)

    label_imagem = ctk.CTkLabel(frame_imagem, text="(sem imagem)", width=120, height=180)
    label_imagem.pack(pady=5)
    ctk.CTkButton(frame_imagem, text="Selecionar Imagem", command=selecionar_imagem).pack(pady=5)

    # ==== BOTÕES FILMES ====
    frame_botoes_filmes = ctk.CTkFrame(tab_filmes)
    frame_botoes_filmes.pack(pady=10)

    ctk.CTkButton(frame_botoes_filmes, text="Cadastrar", command=cadastrar_filme).grid(row=0, column=0, padx=10)
    ctk.CTkButton(frame_botoes_filmes, text="Editar", command=editar_filme_selecionado).grid(row=0, column=1, padx=10)
    ctk.CTkButton(frame_botoes_filmes, text="Remover", command=remover_filme).grid(row=0, column=2, padx=10)
    ctk.CTkButton(frame_botoes_filmes, text="Limpar Campos", command=limpar_campos_filmes).grid(row=0, column=3, padx=10)
    ctk.CTkButton(frame_botoes_filmes, text="Atualizar Lista", command=carregar_filmes).grid(row=0, column=4, padx=10)

    # ==== LISTA DE FILMES ====
    frame_lista_filmes = ctk.CTkFrame(tab_filmes)
    frame_lista_filmes.pack(padx=10, pady=10, fill="both", expand=True)

    ctk.CTkLabel(frame_lista_filmes, text="Filmes cadastrados:", font=("Arial", 16)).pack(pady=10)

    listbox_filmes = tk.Listbox(frame_lista_filmes, height=8, bg="#2b2b2b", fg="white", 
                               selectbackground="#1f6aa5", font=("Arial", 12))
    listbox_filmes.pack(fill="both", expand=True, padx=10, pady=10)
    listbox_filmes.bind("<<ListboxSelect>>", selecionar_filme)

    # Aba Sessões
    tab_sessoes = tabview.add("🎟️ Sessões")
    
    # Frame do formulário de sessões
    frame_form_sessoes = ctk.CTkFrame(tab_sessoes)
    frame_form_sessoes.pack(pady=10, padx=10, fill="x")

    # ===== CAMPOS DE TEXTO SESSÕES =====
    ctk.CTkLabel(frame_form_sessoes, text="Filme:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    combo_filme = ctk.CTkComboBox(frame_form_sessoes, width=300)
    combo_filme.grid(row=0, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form_sessoes, text="Sala:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    combo_sala = ctk.CTkComboBox(frame_form_sessoes, width=300)
    combo_sala.grid(row=1, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form_sessoes, text="Data (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_data = ctk.CTkEntry(frame_form_sessoes, width=300)
    entry_data.grid(row=2, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form_sessoes, text="Horário (HH:MM):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_hora = ctk.CTkEntry(frame_form_sessoes, width=300)
    entry_hora.grid(row=3, column=1, padx=10, pady=5)

    ctk.CTkLabel(frame_form_sessoes, text="Tipo:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    combo_tipo = ctk.CTkComboBox(frame_form_sessoes, values=["dublado", "legendado"], width=300)
    combo_tipo.grid(row=4, column=1, padx=10, pady=5)

    # ==== BOTÕES SESSÕES ====
    frame_botoes_sessoes = ctk.CTkFrame(tab_sessoes)
    frame_botoes_sessoes.pack(pady=10)

    ctk.CTkButton(frame_botoes_sessoes, text="Cadastrar", command=cadastrar_sessao).grid(row=0, column=0, padx=10)
    ctk.CTkButton(frame_botoes_sessoes, text="Editar", command=editar_sessao_selecionada).grid(row=0, column=1, padx=10)
    ctk.CTkButton(frame_botoes_sessoes, text="Remover", command=remover_sessao).grid(row=0, column=2, padx=10)
    ctk.CTkButton(frame_botoes_sessoes, text="Limpar Campos", command=limpar_campos_sessoes).grid(row=0, column=3, padx=10)
    ctk.CTkButton(frame_botoes_sessoes, text="Atualizar Lista", command=carregar_sessoes).grid(row=0, column=4, padx=10)

    # ==== LISTA DE SESSÕES ====
    frame_lista_sessoes = ctk.CTkFrame(tab_sessoes)
    frame_lista_sessoes.pack(padx=10, pady=10, fill="both", expand=True)

    ctk.CTkLabel(frame_lista_sessoes, text="Sessões cadastradas:", font=("Arial", 16)).pack(pady=10)

    listbox_sessoes = tk.Listbox(frame_lista_sessoes, height=8, bg="#2b2b2b", fg="white", 
                                selectbackground="#1f6aa5", font=("Arial", 12))
    listbox_sessoes.pack(fill="both", expand=True, padx=10, pady=10)
    listbox_sessoes.bind("<<ListboxSelect>>", selecionar_sessao)

    # Botão voltar (fora das abas)
    ctk.CTkButton(frame, text="Voltar ao Menu", command=voltar_callback).pack(pady=10)

    # Carregar dados ao iniciar
    carregar_filmes()
    carregar_sessoes()
    carregar_salas()
    carregar_filmes_combo()
    
    # Vincular evento de redimensionamento
    frame.bind("<Configure>", lambda e: ajustar_layout())

    return frame