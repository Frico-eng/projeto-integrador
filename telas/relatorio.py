import customtkinter as ctk
from crud.crud_ingressos import (
    obter_vendas_por_filme, 
    obter_faturamento_por_periodo, 
    obter_ingressos_por_sessao, 
    obter_filmes_mais_populares,
    obter_estatisticas_gerais
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
from PIL import Image, ImageTk
import io

# ================== CONSTANTES DE CORES ==================
BTN_COLOR = "#F6C148"
BTN_HOVER = "#E2952D"
BTN_TEXT = "#1C2732"
SELECTED_COLOR = "#B6D8F1"

def criar_grafico_vendas_filme(dados, periodo):
    """Cria gráfico de barras para vendas por filme"""
    if not dados:
        return None
    
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='#2B2B2B')
    ax.set_facecolor('#2B2B2B')
    
    # Limitar a top 5 filmes
    dados_top5 = dados[:5]
    
    filmes = [d.get('Titulo_Filme', 'N/A')[:15] + '...' if len(d.get('Titulo_Filme', 'N/A')) > 15 else d.get('Titulo_Filme', 'N/A') for d in dados_top5]
    vendas = [d.get('total_ingressos', 0) or 0 for d in dados_top5]
    
    bars = ax.bar(range(len(filmes)), vendas, color=BTN_COLOR, alpha=0.8)
    
    ax.set_title(f'Vendas por Filme - {periodo.upper()}', color='white', fontsize=12, pad=20)
    ax.set_xlabel('Filmes', color='white', fontsize=10)
    ax.set_ylabel('Ingressos Vendidos', color='white', fontsize=10)
    ax.set_xticks(range(len(filmes)))
    ax.set_xticklabels(filmes, rotation=45, ha='right', color='white', fontsize=8)
    
    # Adicionar valores nas barras
    for bar, venda in zip(bars, vendas):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(venda)}', ha='center', va='bottom', color='white', fontsize=8)
    
    ax.tick_params(colors='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    
    # Aplicar tight_layout com tratamento de erro
    try:
        plt.tight_layout()
    except ValueError:
        # Se tight_layout falhar, ajustar manualmente
        plt.subplots_adjust(bottom=0.2, top=0.9, left=0.1, right=0.95)
    
    return fig

def criar_grafico_faturamento_periodo(dados, periodo):
    """Cria gráfico de linha para faturamento por período"""
    if not dados:
        return None
    
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='#2B2B2B')
    ax.set_facecolor('#2B2B2B')
    
    # Limitar a últimos 5 períodos
    dados_top5 = dados[:5]
    
    periodos = [d.get('periodo', 'N/A') for d in dados_top5]
    faturamento = [d.get('faturamento_total', 0) or 0 for d in dados_top5]
    
    ax.plot(range(len(periodos)), faturamento, marker='o', color=BTN_COLOR, linewidth=2, markersize=6)
    
    ax.set_title(f'Faturamento por Período - {periodo.upper()}', color='white', fontsize=12, pad=20)
    ax.set_xlabel('Períodos', color='white', fontsize=10)
    ax.set_ylabel('Faturamento (R$)', color='white', fontsize=10)
    ax.set_xticks(range(len(periodos)))
    ax.set_xticklabels(periodos, rotation=45, ha='right', color='white', fontsize=8)
    
    # Formatar valores no eixo Y
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:.0f}'))
    
    ax.tick_params(colors='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    
    # Aplicar tight_layout com tratamento de erro
    try:
        plt.tight_layout()
    except ValueError:
        # Se tight_layout falhar, ajustar manualmente
        plt.subplots_adjust(bottom=0.2, top=0.9, left=0.1, right=0.95)
    
    return fig

def criar_grafico_ocupacao_sessoes(dados, periodo):
    """Cria gráfico de barras para ocupação das sessões"""
    if not dados:
        return None
    
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='#2B2B2B')
    ax.set_facecolor('#2B2B2B')
    
    # Limitar a top 5 sessões
    dados_top5 = dados[:5]
    
    sessoes = [f"{d.get('Titulo_Filme', 'N/A')[:10]}...\n{d.get('Data_Sessao', 'N/A')} {d.get('Hora_Sessao', 'N/A')}" for d in dados_top5]
    ocupacao = []
    
    for d in dados_top5:
        vendidos = d.get('ingressos_vendidos', 0) or 0
        capacidade = d.get('capacidade_total', 1) or 1
        perc = (vendidos / capacidade * 100) if capacidade > 0 else 0
        ocupacao.append(perc)
    
    bars = ax.bar(range(len(sessoes)), ocupacao, color=BTN_COLOR, alpha=0.8)
    
    ax.set_title(f'Ocupação das Sessões - {periodo.upper()}', color='white', fontsize=12, pad=20)
    ax.set_xlabel('Sessões', color='white', fontsize=10)
    ax.set_ylabel('Ocupação (%)', color='white', fontsize=10)
    ax.set_xticks(range(len(sessoes)))
    ax.set_xticklabels(sessoes, rotation=45, ha='right', color='white', fontsize=7)
    
    # Adicionar valores nas barras
    for bar, perc in zip(bars, ocupacao):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{perc:.1f}%', ha='center', va='bottom', color='white', fontsize=8)
    
    ax.tick_params(colors='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    
    # Aplicar tight_layout com tratamento de erro
    try:
        plt.tight_layout()
    except ValueError:
        # Se tight_layout falhar, ajustar manualmente
        plt.subplots_adjust(bottom=0.25, top=0.9, left=0.1, right=0.95)
    
    return fig

def criar_grafico_filmes_populares(dados, periodo):
    """Cria gráfico de pizza para filmes mais populares"""
    if not dados:
        return None
    
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='#2B2B2B')
    
    # Limitar a top 5 filmes
    dados_top5 = dados[:5]
    
    filmes = [d.get('Titulo_Filme', 'N/A')[:15] + '...' if len(d.get('Titulo_Filme', 'N/A')) > 15 else d.get('Titulo_Filme', 'N/A') for d in dados_top5]
    vendas = [d.get('total_ingressos', 0) or 0 for d in dados_top5]
    
    # Cores para o gráfico de pizza
    cores = ['#F6C148', '#E2952D', '#B6D8F1', '#8B5CF6', '#10B981']
    
    wedges, texts, autotexts = ax.pie(vendas, labels=filmes, autopct='%1.1f%%', 
                                      colors=cores[:len(vendas)], startangle=90)
    
    ax.set_title(f'Filmes Mais Populares - {periodo.upper()}', color='white', fontsize=12, pad=20)
    
    # Ajustar cores dos textos
    for text in texts:
        text.set_color('white')
        text.set_fontsize(8)
    for autotext in autotexts:
        autotext.set_color('#2B2B2B')
        autotext.set_fontsize(8)
    
    # Aplicar tight_layout com tratamento de erro
    try:
        plt.tight_layout()
    except ValueError:
        # Se tight_layout falhar, ajustar manualmente
        plt.subplots_adjust(bottom=0.1, top=0.9, left=0.1, right=0.9)
    
    return fig

def criar_tela_dashboard(parent, voltar_callback=None, fonte_global=None):
    """Cria e retorna o frame do dashboard de relatórios"""
    
    # Frame principal
    frame = ctk.CTkFrame(parent, fg_color="transparent", width=1800, height=900)
    frame.pack_propagate(False)
    
    # Variável para armazenar o período selecionado
    periodo_selecionado = ctk.StringVar(value="diário")
    
    # ================== LAYOUT PRINCIPAL ==================
    
    # FRAME SUPERIOR: Título
    frame_superior = ctk.CTkFrame(frame, height=100)
    frame_superior.pack(fill="x", padx=12, pady=(12, 6))
    frame_superior.pack_propagate(False)
    
    # Título centralizado
    ctk.CTkLabel(
        frame_superior, 
        text="RELATÓRIOS", 
        font=fonte_global if fonte_global else ("Arial", 24, "bold")
    ).pack(expand=True, fill="both", pady=20)
    
    # FRAME MEIO: Botões de período - DIVIDIDO EM 3 COLUNAS
    frame_meio = ctk.CTkFrame(frame, height=100)
    frame_meio.pack(fill="x", padx=12, pady=6)
    frame_meio.pack_propagate(False)
    
    # Configurar grid para 3 colunas
    frame_meio.grid_columnconfigure(0, weight=1)  # Esquerda - Botão voltar
    frame_meio.grid_columnconfigure(1, weight=2)  # Meio - Botões de período
    frame_meio.grid_columnconfigure(2, weight=1)  # Direita - Botões de fonte
    
    # ===== COLUNA ESQUERDA: Botão Voltar =====
    frame_esquerda = ctk.CTkFrame(frame_meio, fg_color="transparent")
    frame_esquerda.grid(row=0, column=0, sticky="w", padx=(20, 10))
    
    # Botão voltar na coluna esquerda
    if voltar_callback:
        btn_voltar = ctk.CTkButton(
            frame_esquerda,
            text="Voltar",
            fg_color=BTN_COLOR,
            font=fonte_global if fonte_global else ("Arial", 14, "bold"),
            hover_color=BTN_HOVER,
            text_color=BTN_TEXT,
            height=40,
            width=120,
            command=voltar_callback
        )
        btn_voltar.pack(pady=10)
    
    # ===== COLUNA MEIO: Botões de Período =====
    frame_centro = ctk.CTkFrame(frame_meio, fg_color="transparent")
    frame_centro.grid(row=0, column=1, sticky="nsew")
    
    # Container para os botões de período
    frame_botoes_periodo = ctk.CTkFrame(frame_centro, fg_color="transparent")
    frame_botoes_periodo.pack(expand=True, fill="both", pady=10)
    
    # Botões de período
    botoes_periodo = []
    periodos = [
        ("Diário", "diário"),
        ("Mensal", "mensal"),
        ("Quatrenal", "quatrenal"),
        ("Anual", "anual")
    ]
    
    for texto, valor in periodos:
        btn = ctk.CTkButton(
            frame_botoes_periodo,
            text=texto,
            width=120,
            height=40,
            corner_radius=8,
            fg_color=BTN_COLOR if valor != "diário" else SELECTED_COLOR,
            hover_color=BTN_HOVER,
            text_color=BTN_TEXT,
            font=fonte_global if fonte_global else ("Arial", 14, "bold"),
            command=lambda v=valor: selecionar_periodo(v)
        )
        btn.pack(side="left", padx=5, pady=5)
        botoes_periodo.append(btn)
    
    # ===== COLUNA DIREITA: Botões de Fonte =====
    frame_direita = ctk.CTkFrame(frame_meio, fg_color="transparent")
    frame_direita.grid(row=0, column=2, sticky="e", padx=(10, 20))
    
    # Importar funções de fonte do main.py
    try:
        from main import aumentar_fonte, diminuir_fonte
    except ImportError:
        # Fallback se não conseguir importar
        def aumentar_fonte():
            if fonte_global and fonte_global.cget("size") < 22:
                fonte_global.configure(size=fonte_global.cget("size") + 2)
        
        def diminuir_fonte():
            if fonte_global and fonte_global.cget("size") > 6:
                fonte_global.configure(size=fonte_global.cget("size") - 2)
    
    # Botões para controle de fonte
    frame_controle_fonte = ctk.CTkFrame(frame_direita, fg_color="transparent")
    frame_controle_fonte.pack(pady=10)
    ctk.CTkButton(frame_controle_fonte, text="A+", command=aumentar_fonte, width=40, height=35, 
                  font=fonte_global if fonte_global else ("Arial", 12, "bold")).pack(side="left", padx=3)
    ctk.CTkButton(frame_controle_fonte, text="A-", command=diminuir_fonte, width=40, height=35,
                  font=fonte_global if fonte_global else ("Arial", 12, "bold")).pack(side="left", padx=3)
    
    # FRAME INFERIOR: Gráficos
    frame_inferior = ctk.CTkFrame(frame)
    frame_inferior.pack(fill="both", expand=True, padx=12, pady=(6, 12))
    
    # Container para gráficos (2x2 grid)
    frame_graficos_container = ctk.CTkFrame(frame_inferior, fg_color="transparent")
    frame_graficos_container.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Configurar grid para os gráficos
    frame_graficos_container.grid_columnconfigure(0, weight=1)
    frame_graficos_container.grid_columnconfigure(1, weight=1)
    frame_graficos_container.grid_rowconfigure(0, weight=1)
    frame_graficos_container.grid_rowconfigure(1, weight=1)
    
    # Frames para os gráficos (placeholders)
    graficos = []
    for row in range(2):
        for col in range(2):
            frame_grafico = ctk.CTkFrame(
                frame_graficos_container,
                border_width=2,
                border_color="#444444",
                corner_radius=10
            )
            frame_grafico.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Título do gráfico
            titulos = [
                "Vendas por Filme",
                "Faturamento por Período",
                "Ingressos por Sessão",
                "Filmes Mais Populares"
            ]
            ctk.CTkLabel(
                frame_grafico,
                text=titulos[row * 2 + col],
                font=fonte_global if fonte_global else ("Arial", 14, "bold")
            ).pack(pady=10)
            
            # Placeholder para o gráfico
            placeholder_text = f"Gráfico {titulos[row * 2 + col]} será exibido aqui"
            ctk.CTkLabel(
                frame_grafico,
                text=placeholder_text,
                text_color="gray",
                font=fonte_global if fonte_global else ("Arial", 12)
            ).pack(expand=True, fill="both", padx=20, pady=20)
            
            graficos.append(frame_grafico)
    
    # ================== BOTÕES DE NAVEGAÇÃO ==================
    botoes_frame = ctk.CTkFrame(frame, height=50)
    botoes_frame.pack(side="bottom", fill="x", padx=20, pady=10)
    botoes_frame.pack_propagate(False)
    
    # ================== FUNÇÕES ==================
    
    def atualizar_frame_grafico(frame_grafico, fig, titulo):
        """Atualiza um frame de gráfico com uma nova figura matplotlib"""
        # Limpar o frame
        for widget in frame_grafico.winfo_children():
            widget.destroy()
        
        if fig is None:
            # Se não há dados, mostrar mensagem
            ctk.CTkLabel(
                frame_grafico,
                text=f"{titulo}\n\nNenhum dado encontrado\npara o período.",
                text_color="gray",
                font=fonte_global if 'fonte_global' in globals() else ("Arial", 12)
            ).pack(expand=True, fill="both", padx=20, pady=20)
            return
        
        try:
            # Criar canvas para o gráfico
            canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Armazenar referência para evitar garbage collection
            if not hasattr(frame_grafico, '_canvas_refs'):
                frame_grafico._canvas_refs = []
            frame_grafico._canvas_refs.append(canvas)
            
            # Fechar a figura para liberar memória (matplotlib mantém figuras abertas)
            plt.close(fig)
            
        except Exception as e:
            print(f"Erro ao criar gráfico {titulo}: {e}")
            ctk.CTkLabel(
                frame_grafico,
                text=f"{titulo}\n\nErro ao gerar gráfico.",
                text_color="red",
                font=fonte_global if 'fonte_global' in globals() else ("Arial", 12)
            ).pack(expand=True, fill="both", padx=20, pady=20)
    
    def atualizar_graficos():
        """Atualiza todos os gráficos com dados do período selecionado"""
        periodo_atual = periodo_selecionado.get()
        
        # Obter dados
        vendas_filme = obter_vendas_por_filme(periodo_atual)
        faturamento_periodo = obter_faturamento_por_periodo(periodo_atual)
        ingressos_sessao = obter_ingressos_por_sessao(periodo_atual)
        filmes_populares = obter_filmes_mais_populares(periodo_atual)
        estatisticas = obter_estatisticas_gerais(periodo_atual)
        
        # Atualizar gráfico 1: Vendas por Filme
        fig1 = criar_grafico_vendas_filme(vendas_filme, periodo_atual)
        atualizar_frame_grafico(graficos[0], fig1, "Vendas por Filme")
        
        # Atualizar gráfico 2: Faturamento por Período
        fig2 = criar_grafico_faturamento_periodo(faturamento_periodo, periodo_atual)
        atualizar_frame_grafico(graficos[1], fig2, "Faturamento por Período")
        
        # Atualizar gráfico 3: Ocupação das Sessões
        fig3 = criar_grafico_ocupacao_sessoes(ingressos_sessao, periodo_atual)
        atualizar_frame_grafico(graficos[2], fig3, "Ocupação das Sessões")
        
        # Atualizar gráfico 4: Filmes Mais Populares
        fig4 = criar_grafico_filmes_populares(filmes_populares, periodo_atual)
        atualizar_frame_grafico(graficos[3], fig4, "Filmes Mais Populares")
        
        # Atualizar estatísticas gerais no título
        if estatisticas:
            titulo_texto = f"RELATÓRIOS - {periodo_atual.upper()}\n"
            ingressos_total = estatisticas.get('total_ingressos_vendidos', 0) or 0
            faturamento_total = estatisticas.get('faturamento_total', 0) or 0
            clientes_unicos = estatisticas.get('total_clientes_unicos', 0) or 0
            titulo_texto += f"Ingressos: {ingressos_total} | "
            titulo_texto += f"Faturamento: R$ {faturamento_total:.2f} | "
            titulo_texto += f"Clientes: {clientes_unicos}"
            
            # Atualizar o título
            for widget in frame_superior.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "RELATÓRIOS" in widget.cget("text"):
                    widget.configure(text=titulo_texto)
    
    def selecionar_periodo(periodo):
        """Seleciona o período para o relatório"""
        periodo_selecionado.set(periodo)
        
        # Atualizar visual dos botões
        for btn, (texto, valor) in zip(botoes_periodo, periodos):
            if valor == periodo:
                btn.configure(fg_color=SELECTED_COLOR)
            else:
                btn.configure(fg_color=BTN_COLOR)
        
        # Atualizar gráficos com dados do período selecionado
        atualizar_graficos()
    
    # Botão de exportar relatório (opcional)
    btn_exportar = ctk.CTkButton(
        botoes_frame,
        text="Exportar Relatório",
        fg_color=BTN_COLOR,
        font=fonte_global if fonte_global else ("Arial", 14, "bold"),
        hover_color=BTN_HOVER,
        text_color=BTN_TEXT,
        height=40,
        width=150
    )
    btn_exportar.pack(side="right", padx=10)
    
    # Botão de atualizar (opcional)
    btn_atualizar = ctk.CTkButton(
        botoes_frame,
        text="Atualizar Dados",
        fg_color=BTN_COLOR,
        font=fonte_global if fonte_global else ("Arial", 14, "bold"),
        hover_color=BTN_HOVER,
        text_color=BTN_TEXT,
        height=40,
        width=150,
        command=atualizar_graficos
    )
    btn_atualizar.pack(side="right", padx=10)
    
    # Carregar dados iniciais
    atualizar_graficos()
    
    return frame