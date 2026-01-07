import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
from PIL import Image
from crud.crud_filme import listar_filmes
from utilidades.ui_helpers import criar_botao
from crud.crud_ingressos import conectar
from utilidades.config import BTN_COLOR, BTN_HOVER, BTN_TEXT
from utilidades import gerenciador_telas

def criar_tela_gerente(parent, voltar_callback):
    """Cria a tela de gerente para visualizar relatórios e estatísticas"""
    
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    
    # Título
    titulo_frame = ctk.CTkFrame(frame, fg_color="transparent")
    titulo_frame.pack(fill="x", padx=20, pady=20)
    
    titulo = ctk.CTkLabel(
        titulo_frame,
        text="Painel de Gerente - Relatórios",
        font=("Arial", 28, "bold"),
        text_color="white"
    )
    titulo.pack()
    
    # Frame principal com duas colunas
    conteudo_frame = ctk.CTkFrame(frame, fg_color="transparent")
    conteudo_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Ações (estatísticas removidas)
    
    # Coluna direita - Ações
    col_direita = ctk.CTkFrame(conteudo_frame, fg_color="#2B2B2B", corner_radius=10)
    col_direita.pack(fill="both", expand=True, padx=10, pady=0)
    
    titulo_acoes = ctk.CTkLabel(
        col_direita,
        text="⚙️ Ações",
        font=("Arial", 18, "bold"),
        text_color=BTN_COLOR
    )
    titulo_acoes.pack(pady=15, padx=15)
    
    # Botões de ações
    botoes_frame = ctk.CTkFrame(col_direita, fg_color="transparent")
    botoes_frame.pack(fill="both", expand=True, padx=15, pady=10)
    
    def gerar_relatorio():
        messagebox.showinfo("Relatório", "Gerando relatório de vendas...")
    
    def gerenciar_funcionarios():
        messagebox.showinfo("Funcionários", "Abrindo painel de gerenciamento de funcionários...")
    
    def gerenciar_sessoes():
        gerenciador_telas.show_screen("funcionario")
    
    def visualizar_ingressos():
        # Janela com tabela de ingressos
        janela = ctk.CTkToplevel(frame)
        janela.title("Visualizar Ingressos")
        janela.geometry("900x500")
        janela.grab_set()

        tree_frame = ctk.CTkFrame(janela, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("ID_Ingresso", "ID_Sessao", "ID_Cliente", "ID_Assento_Sessao", "Valor", "Data_Compra", "Data_Sessao", "Hora_Sessao", "Titulo_Filme")

        # Usamos ttk.Treeview para a tabela
        tree = ttk.Treeview(tree_frame, columns=cols, show='headings', height=18)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=100, anchor='center')

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Buscar dados no banco
        try:
            con = conectar()
            if not con:
                messagebox.showerror("Erro", "Falha ao conectar ao banco de dados")
                janela.destroy()
                return

            cur = con.cursor()
            cur.execute("""
                SELECT i.ID_Ingresso, i.ID_Sessao, i.ID_Cliente, i.ID_Assento_Sessao, i.Valor, i.Data_Compra,
                       s.Data_Sessao, s.Hora_Sessao, f.Titulo_Filme
                FROM Ingressos i
                LEFT JOIN Sessoes s ON i.ID_Sessao = s.ID_Sessao
                LEFT JOIN Filmes f ON s.ID_Filme = f.ID_Filme
                ORDER BY i.Data_Compra DESC
            """)

            rows = cur.fetchall()
            for r in rows:
                # garantir que todos os campos sejam strings compatíveis
                tree.insert('', 'end', values=[str(x) if x is not None else '' for x in r])

            cur.close()
            con.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao buscar ingressos: {e}")
            janela.destroy()
            return

        # Botões de ação
        btns = ctk.CTkFrame(janela, fg_color="transparent")
        btns.pack(fill="x", padx=10, pady=(0,10))

        def fechar():
            janela.destroy()

        ctk.CTkButton(btns, text="Fechar", command=fechar, fg_color="#e74c3c").pack(side="right", padx=6)
    # visualizar_usuarios removido conforme solicitado
    
    # Botão Relatório
    btn_relatorio = ctk.CTkButton(
        botoes_frame,
        text="📊 Gerar Relatório",
        command=gerar_relatorio,
        fg_color=BTN_COLOR,
        hover_color=BTN_HOVER,
        text_color=BTN_TEXT,
        font=("Arial", 14, "bold"),
        height=40,
        corner_radius=8
    )
    btn_relatorio.pack(fill="x", pady=8)
    
    # Botão Gerenciar Funcionários
    btn_func = ctk.CTkButton(
        botoes_frame,
        text="👥 Gerenciar Funcionários",
        command=gerenciar_funcionarios,
        fg_color=BTN_COLOR,
        hover_color=BTN_HOVER,
        text_color=BTN_TEXT,
        font=("Arial", 14, "bold"),
        height=40,
        corner_radius=8
    )
    btn_func.pack(fill="x", pady=8)
    
    # Botão Gerenciar Sessões
    btn_sessoes = ctk.CTkButton(
        botoes_frame,
        text="🎬 Gerenciar Sessões",
        command=gerenciar_sessoes,
        fg_color=BTN_COLOR,
        hover_color=BTN_HOVER,
        text_color=BTN_TEXT,
        font=("Arial", 14, "bold"),
        height=40,
        corner_radius=8
    )
    btn_sessoes.pack(fill="x", pady=8)
    
    # Botão Visualizar Ingressos
    btn_ingressos = ctk.CTkButton(
        botoes_frame,
        text="🎟️ Visualizar Ingressos",
        command=visualizar_ingressos,
        fg_color=BTN_COLOR,
        hover_color=BTN_HOVER,
        text_color=BTN_TEXT,
        font=("Arial", 14, "bold"),
        height=40,
        corner_radius=8
    )
    btn_ingressos.pack(fill="x", pady=8)
    # Botão Visualizar Usuários removido conforme solicitado
    
    # Footer com botão voltar
    footer_frame = ctk.CTkFrame(frame, fg_color="transparent")
    footer_frame.pack(fill="x", padx=20, pady=20)
    
    btn_voltar = ctk.CTkButton(
        footer_frame,
        text="← Voltar",
        command=voltar_callback,
        fg_color="#555555",
        hover_color="#777777",
        text_color="white",
        font=("Arial", 14, "bold"),
        height=40,
        corner_radius=8,
        width=150
    )
    btn_voltar.pack(side="left")
    
    return frame
