import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
from PIL import Image
from crud.crud_filme import listar_filmes
from utilidades.ui_helpers import criar_botao, alternar_tema
from crud.crud_ingressos import conectar
from utilidades.config import BTN_COLOR, BTN_HOVER, BTN_TEXT
from utilidades import gerenciador_telas
import utilidades.config as config_module
import os

def criar_tela_gerente(parent, voltar_callback, fonte_global=None, is_gerente=True):
    """Cria a tela de gerente para visualizar relatórios e estatísticas"""
    
    # Funções para aumentar/diminuir fonte se fonte_global for fornecida
    def aumentar_fonte():
        if fonte_global and fonte_global.cget("size") < 22:  # 14 + (4 * 2)
            fonte_global.configure(size=fonte_global.cget("size") + 2)

    def diminuir_fonte():
        if fonte_global and fonte_global.cget("size") > 6:  # 14 - (4 * 2)
            fonte_global.configure(size=fonte_global.cget("size") - 2)
    
    # Função para atualizar cores baseado no tema
    def atualizar_cores_tema():
        tema_escuro = config_module.tema_atual == "dark"
        
        if tema_escuro:
            bg_frame = "#2B2B2B"
            text_color = "white"
        else:
            bg_frame = "#E8E8E8"
            text_color = "black"
        
        # Atualizar cores dos elementos
        frame_botoes.configure(fg_color=bg_frame)
        titulo_acoes.configure(text_color=text_color)
    
    # Frame principal que ocupa toda a tela
    frame = ctk.CTkFrame(parent, fg_color="transparent",height=120)
    frame.pack(fill="both", expand=True)
    
    # Frame de fundo com imagem (ocupa toda a tela)
    bg_frame = ctk.CTkFrame(frame, fg_color="transparent",height=120)
    bg_frame.pack(fill="both", expand=True)
    
    # Carregar imagem de fundo se existir
    img_path = os.path.join(os.path.dirname(__file__), "..", "utilidades", "images", "gerente.png")
    if os.path.exists(img_path):
        try:
            img = Image.open(img_path)
            # Redimensionar para cobrir a tela
            screen_width = parent.winfo_screenwidth()
            screen_height = parent.winfo_screenheight()
            img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=(screen_width, screen_height))
            
            bg_label = ctk.CTkLabel(bg_frame, image=photo, text="")
            bg_label.image = photo
            bg_label.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            bg_frame.configure(fg_color="#1a1a1a")
    else:
        bg_frame.configure(fg_color="#1a1a1a")
    
    # Frame de botões que se sobrepõe ao fundo (usando place para sobreposição)
    frame_botoes = ctk.CTkFrame(frame, fg_color="#2B2B2B", corner_radius=10,height=120)
    frame_botoes.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.2, relheight=0.5)
    
    # Frame de controle de fonte e tema (no topo do frame_botoes)
    if fonte_global:
        frame_controle_fonte = ctk.CTkFrame(frame_botoes, fg_color="transparent")
        frame_controle_fonte.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkButton(frame_controle_fonte, text="A+", command=aumentar_fonte, width=50, font=fonte_global).pack(side="left", padx=5)
        ctk.CTkButton(frame_controle_fonte, text="A-", command=diminuir_fonte, width=50, font=fonte_global).pack(side="left", padx=5)
        
        # Botão para alternar tema claro e escuro
        botao_tema = ctk.CTkButton(
            frame_controle_fonte,
            text="🌙",
            command=lambda: [alternar_tema(parent, botao_tema), atualizar_cores_tema()],
            width=50,
            font=fonte_global,
            fg_color=BTN_COLOR,
            hover_color=BTN_HOVER,
            text_color=BTN_TEXT
        )
        botao_tema.pack(side="left", padx=5)
    
    titulo_acoes = ctk.CTkLabel(
        frame_botoes,
        text="⚙️ Ações",
        font=fonte_global if fonte_global else ("Arial", 18, "bold"),
        text_color=BTN_COLOR
    )
    titulo_acoes.pack(pady=15, padx=15)
    
    # Atualizar cores iniciais
    atualizar_cores_tema()
    
    # Botões de ações
    botoes_frame = ctk.CTkFrame(frame_botoes, fg_color="transparent",height=420)
    botoes_frame.pack(fill="both", expand=True, padx=15, pady=10)
    
    def gerar_relatorio():
        gerenciador_telas.show_screen("relatorio")
    
    def gerenciar_funcionarios():
        gerenciador_telas.show_screen("gestao_funcionarios")
    
    def gerenciar_sessoes():
        # Importar função de criação da tela de funcionário
        from telas.funcionario import criar_tela_funcionario
        from utilidades.gerenciador_telas import screens
        
        # Limpar o frame de funcionário anterior
        funcionario_frame = screens.get("funcionario")
        if funcionario_frame:
            for widget in funcionario_frame.winfo_children():
                widget.destroy()
        
        # Recriar a tela de funcionário com callback para voltar ao gerente
        criar_tela_funcionario(
            funcionario_frame, 
            voltar_callback=lambda: gerenciador_telas.show_screen("gerente"),
            fonte_global=None
        ).pack(fill="both", expand=True)
        
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
        font=fonte_global if fonte_global else ("Arial", 14, "bold"),
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
        font=fonte_global if fonte_global else ("Arial", 14, "bold"),
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
        font=fonte_global if fonte_global else ("Arial", 14, "bold"),
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
        font=fonte_global if fonte_global else ("Arial", 14, "bold"),
        height=40,
        corner_radius=8
    )
    btn_ingressos.pack(fill="x", pady=8)
    # Botão Visualizar Usuários removido conforme solicitado
    
    # Footer com botão voltar
    footer_frame = ctk.CTkFrame(frame_botoes, fg_color="transparent")
    footer_frame.pack(fill="x", padx=15, pady=15)
    
    def voltar_com_logout():
        """Callback que limpa o login antes de voltar"""
        if is_gerente:
            # Limpar entradas de login
            gerenciador_telas.clear_login_entries()
        voltar_callback()
    
    btn_voltar = ctk.CTkButton(
        footer_frame,
        text="← Voltar",
        command=voltar_com_logout,
        fg_color="#555555",
        hover_color="#777777",
        text_color="white",
        font=fonte_global if fonte_global else ("Arial", 14, "bold"),
        height=40,
        corner_radius=8,
        width=150
    )
    btn_voltar.pack(side="left")
    
    return frame
