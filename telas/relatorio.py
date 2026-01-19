import customtkinter as ctk
from crud.crud_ingressos import (
    get_dados_relatorio
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
from PIL import Image, ImageTk
import io
import math
from utilidades.ui_helpers import alternar_tema
import hashlib

# ================== CONSTANTES DE CORES ==================
BTN_COLOR = "#F6C148"
BTN_HOVER = "#E2952D"
BTN_TEXT = "#1C2732"
SELECTED_COLOR = "#B6D8F1"

# ================== PALETTE DE CORES PARA FILMES ==================
CORES_FILMES_PALETTE = [
    '#F6C148', '#E2952D', '#B6D8F1', '#8B5CF6', '#10B981', 
    '#F59E0B', '#EF4444', '#06B6D4', '#84CC16', '#EC4899',
    '#14B8A6', '#F97316', '#6366F1', '#22C55E', '#3B82F6',
    '#A855F7', '#D946EF', '#F43F5E', '#64748B', '#0891B2'
]

def obter_cor_filme(nome_filme, cache_cores=None):
    """
    Obtém uma cor consistente para um filme baseado no seu nome.
    Usa hash para garantir que o mesmo filme sempre tenha a mesma cor.
    """
    if cache_cores is None:
        cache_cores = {}
    
    if nome_filme in cache_cores:
        return cache_cores[nome_filme]
    
    # Gerar hash do nome do filme para determinar índice consistente
    hash_obj = hashlib.md5(nome_filme.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    indice_cor = hash_int % len(CORES_FILMES_PALETTE)
    
    cor = CORES_FILMES_PALETTE[indice_cor]
    cache_cores[nome_filme] = cor
    
    return cor

def criar_grafico_vendas_filme(dados_relatorio, periodo, cache_cores=None):
    """Cria gráfico de barras para vendas por filme com cores consistentes"""
    if not dados_relatorio:
        return None
    
    if cache_cores is None:
        cache_cores = {}
    
    # Agregar vendas por filme
    vendas_por_filme = {}
    for item in dados_relatorio:
        filme = item['nome_filme']
        if filme not in vendas_por_filme:
            vendas_por_filme[filme] = 0
        vendas_por_filme[filme] += 1
    
    # Ordenar todos os filmes (sem limite)
    sorted_filmes = sorted(vendas_por_filme.items(), key=lambda x: x[1], reverse=True)
    
    if not sorted_filmes:
        return None
    
    fig, ax = plt.subplots(figsize=(6, 5), facecolor='#2B2B2B')
    ax.set_facecolor('#2B2B2B')
    
    ids_filmes = [f"ID {i+1}" for i in range(len(sorted_filmes))]
    nomes_filmes = [filme[:20] + '...' if len(filme) > 20 else filme for filme, _ in sorted_filmes]
    vendas = [venda for _, venda in sorted_filmes]
    
    # Obter cores consistentes para cada filme
    cores_barras = [obter_cor_filme(filme, cache_cores) for filme, _ in sorted_filmes]

    bars = ax.bar(range(len(ids_filmes)), vendas, 
                color=cores_barras, 
                width=0.8,
                alpha=0.85)
    
    ax.set_title(f'Vendas por Filme - {periodo.upper()}', color='white', fontsize=12, pad=20)
    ax.set_xlabel('Filme', color='white', fontsize=10)
    ax.set_ylabel('Ingressos Vendidos', color='white', fontsize=10)
    ax.set_xticks(range(len(ids_filmes)))
    ax.set_xticklabels(nomes_filmes, rotation=45, ha='right', color='white', fontsize=8)
    
    # Adicionar legenda com os nomes dos filmes abaixo do gráfico
    legend_patches = [plt.matplotlib.patches.Patch(color=cores_barras[i], label=nomes_filmes[i]) 
                      for i in range(len(nomes_filmes))]
    ax.legend(handles=legend_patches, title="Filmes", loc="upper center", bbox_to_anchor=(0.5, -0.15), 
              fontsize=6, framealpha=0.9, facecolor='white', edgecolor='white', labelcolor='black', ncol=3)
    
    # Adicionar valores nas barras
    for bar, venda in zip(bars, vendas):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/3., height + 0.1,
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
        plt.subplots_adjust(bottom=0.25, top=0.9, left=0.1, right=0.75)
    
    return fig

def criar_grafico_faturamento_periodo(dados_relatorio, periodo, cache_cores=None):
    """Cria gráfico de linha para faturamento por período"""
    if not dados_relatorio:
        return None
    
    if cache_cores is None:
        cache_cores = {}
    
    # Agregar faturamento por período
    faturamento_por_periodo = {}
    for item in dados_relatorio:
        if periodo == "diário":
            # Para diário, agrupar por hora (hora_sessao é timedelta)
            if item['hora_sessao']:
                horas = int(item['hora_sessao'].total_seconds() // 3600)
                periodo_key = f"{horas:02d}"
            else:
                periodo_key = '00'
        elif periodo == "mensal":
            periodo_key = item['data_sessao'].strftime('%Y-%m') if item['data_sessao'] else 'N/A'
        elif periodo == "quatrenal":
            periodo_key = f"{item['data_sessao'].year}-Q{((item['data_sessao'].month-1)//3)+1}" if item['data_sessao'] else 'N/A'
        elif periodo == "anual":
            periodo_key = str(item['data_sessao'].year) if item['data_sessao'] else 'N/A'
        else:
            periodo_key = item['data_sessao'].strftime('%Y-%m-%d') if item['data_sessao'] else 'N/A'
        
        if periodo_key not in faturamento_por_periodo:
            faturamento_por_periodo[periodo_key] = 0
        faturamento_por_periodo[periodo_key] += item['valor'] or 0
    
    # Ordenar períodos
    sorted_periodos = sorted(faturamento_por_periodo.items(), key=lambda x: x[0])
    
    # Limitar a últimos períodos conforme o tipo de período
    if periodo == "diário":
        limite = 5
        figsize = (6, 4)
    elif periodo == "mensal":
        limite = 12  # Mostrar últimos 12 meses
        figsize = (10, 4)  # Figura mais larga para acomodar os meses
    elif periodo == "quatrenal":
        limite = 5  # Trimestres
        figsize = (6, 4)
    elif periodo == "anual":
        limite = 10  # Últimos 10 anos
        figsize = (8, 4)
    else:
        limite = 5
        figsize = (6, 4)
    
    dados_top5 = sorted_periodos[-limite:] if len(sorted_periodos) > limite else sorted_periodos
    
    if not dados_top5:
        return None
    
    fig, ax = plt.subplots(figsize=figsize, facecolor='#2B2B2B')
    ax.set_facecolor('#2B2B2B')
    
    periodos = [p for p, _ in dados_top5]
    
    # Formatar rótulos conforme o tipo de período
    if periodo == "diário":
        periodos_labels = [f"{int(p):02d}:00" if p != 'N/A' else 'N/A' for p in periodos]
    elif periodo == "mensal":
        # Converter YYYY-MM para formato mais legível (Mês/Ano)
        periodos_labels = []
        meses_nomes = {
            1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
        }
        for p in periodos:
            if p != 'N/A':
                try:
                    ano, mes = p.split('-')
                    periodos_labels.append(f"{meses_nomes[int(mes)]}/{ano[-2:]}")
                except:
                    periodos_labels.append(p)
            else:
                periodos_labels.append(p)
    else:
        periodos_labels = periodos
    
    faturamento = [f for _, f in dados_top5]
    
    # Usar cor consistente (cor do primeiro filme, ou BTN_COLOR como fallback)
    cor_linha = obter_cor_filme("Faturamento", cache_cores) if dados_relatorio else BTN_COLOR
    ax.plot(range(len(periodos)), faturamento, marker='o', color=cor_linha, linewidth=2, markersize=6)
    
    ax.set_title(f'Faturamento por Período - {periodo.upper()}', color='white', fontsize=12, pad=20)
    ax.set_xlabel('Períodos', color='white', fontsize=10)
    ax.set_ylabel('Faturamento (R$)', color='white', fontsize=10)
    
    # Configurar ticks para mostrar todos os períodos
    ax.set_xticks(range(len(periodos)))
    ax.set_xticklabels(periodos_labels, rotation=45, ha='right', color='white', fontsize=8)
    
    # Para período mensal, usar locator para forçar exibição de todos os meses
    if periodo == "mensal":
        ax.xaxis.set_major_locator(plt.matplotlib.ticker.MaxNLocator(integer=True, nbins=len(periodos)))
    
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

def criar_grafico_ocupacao_sessoes(dados_relatorio, periodo, cache_cores=None):
    """Cria gráfico de barras para vendas por sessão com cores por filme"""
    if not dados_relatorio:
        return None
    
    if cache_cores is None:
        cache_cores = {}
    
    # Agregar vendas por sessão mantendo referência ao filme e horário
    vendas_por_sessao = {}
    filme_por_sessao = {}
    horario_por_sessao = {}
    for item in dados_relatorio:
        sessao_key = f"{item['nome_filme'][:10]}... {item['data_sessao']} {item['hora_sessao']}"
        if sessao_key not in vendas_por_sessao:
            vendas_por_sessao[sessao_key] = 0
            filme_por_sessao[sessao_key] = item['nome_filme']
            horario_por_sessao[sessao_key] = item['hora_sessao']
        vendas_por_sessao[sessao_key] += 1
    
    # Ordenar e limitar top 10 sessões
    sorted_sessoes = sorted(vendas_por_sessao.items(), key=lambda x: x[1], reverse=True)[:10]
    
    if not sorted_sessoes:
        return None
    
    fig, ax = plt.subplots(figsize=(6, 5), facecolor='#2B2B2B')
    ax.set_facecolor('#2B2B2B')
    
    # Criar legendas com filme e horário
    legendas = []
    for i, (sessao, _) in enumerate(sorted_sessoes):
        filme_nome = filme_por_sessao[sessao]
        horario = horario_por_sessao[sessao]
        # Formatar: "Filme... HH:MM"
        if horario:
            if isinstance(horario, str):
                horario_str = horario[:5]  # Pegar HH:MM da string
            else:
                total_seconds = int(horario.total_seconds())
                horas = total_seconds // 3600
                minutos = (total_seconds % 3600) // 60
                horario_str = f"{horas:02d}:{minutos:02d}"
        else:
            horario_str = "00:00"
        
        filme_curto = filme_nome[:18] + "..." if len(filme_nome) > 21 else filme_nome
        legendas.append(f"{filme_curto} - {horario_str}")
    
    vendas = [venda for _, venda in sorted_sessoes]
    
    # Obter cores consistentes baseadas no filme de cada sessão
    cores_barras = [obter_cor_filme(filme_por_sessao[sessao], cache_cores) for sessao, _ in sorted_sessoes]

    bars = ax.bar(range(len(legendas)), vendas, color=cores_barras, width=0.5, alpha=0.8, label=legendas)
    
    ax.set_title(f'Vendas por Sessão - {periodo.upper()}', color='white', fontsize=12, pad=20)
    ax.set_xlabel('Sessões', color='white', fontsize=10)
    ax.set_ylabel('Ingressos Vendidos', color='white', fontsize=10)
    ax.set_xticks(range(len(legendas)))
    ax.set_xticklabels([f"Sessão {i+1}" for i in range(len(legendas))], rotation=45, ha='right', color='white', fontsize=8)
    
    # Adicionar legenda com filme e horário abaixo do gráfico
    legend_patches = [plt.matplotlib.patches.Patch(color=cores_barras[i], label=legendas[i]) 
                      for i in range(len(legendas))]
    ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.15), 
              fontsize=6, framealpha=0.9, facecolor='white', edgecolor='white', labelcolor='black', ncol=2)
    
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
        plt.subplots_adjust(bottom=0.2, top=0.9, left=0.1, right=0.75)
    
    return fig

def criar_grafico_filmes_populares(dados_relatorio, periodo, cache_cores=None):
    """Cria gráfico de pizza para filmes mais populares com cores consistentes"""
    if not dados_relatorio:
        return None
    
    if cache_cores is None:
        cache_cores = {}
    
    # Agregar vendas por filme
    vendas_por_filme = {}
    for item in dados_relatorio:
        filme = item['nome_filme']
        if filme not in vendas_por_filme:
            vendas_por_filme[filme] = 0
        vendas_por_filme[filme] += 1
    
    # Filtrar filmes com vendas > 0 (sem limite de quantidade)
    sorted_filmes = sorted([(f, v) for f, v in vendas_por_filme.items() if v > 0], key=lambda x: x[1], reverse=True)
    
    if not sorted_filmes:
        fig, ax = plt.subplots(figsize=(6, 5), facecolor='#2B2B2B')
        ax.text(0.5, 0.5, 'Nenhum filme\ncom vendas\nno período', 
                ha='center', va='center', color='white', fontsize=12, transform=ax.transAxes)
        ax.set_title(f'Filmes Mais Populares - {periodo.upper()}', color='white', fontsize=12, pad=20)
        return fig
    
    fig, ax = plt.subplots(figsize=(6, 5), facecolor='#2B2B2B')
    
    filmes_completos = [f for f, _ in sorted_filmes]
    filmes = [filme[:15] + '...' if len(filme) > 15 else filme for filme, _ in sorted_filmes]
    vendas = [venda for _, venda in sorted_filmes]
    
    # Obter cores consistentes para cada filme
    cores = [obter_cor_filme(filme_nome, cache_cores) for filme_nome in filmes_completos]
    
    wedges, texts, autotexts = ax.pie(vendas, labels=None, autopct='%1.1f%%', 
                                      colors=cores, startangle=90)
    
    ax.set_title(f'Filmes Mais Populares - {periodo.upper()}', color='white', fontsize=12, pad=20)
    
    # Adicionar legenda com os nomes dos filmes abaixo do gráfico
    ax.legend(wedges, filmes, title="Filmes", loc="upper center", bbox_to_anchor=(0.5, -0.1), 
              fontsize=6, framealpha=0.9, facecolor='white', edgecolor='white', labelcolor='black', ncol=2)
    
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
        plt.subplots_adjust(bottom=0.15, top=0.9, left=0.1, right=0.8)
    
    return fig

def criar_grafico_ingressos_horario(dados_relatorio, periodo, cache_cores=None):
    """Cria gráfico de barras para ingressos vendidos por horário com cores por filme"""
    if not dados_relatorio:
        return None
    
    if cache_cores is None:
        cache_cores = {}
    
    # Agregar vendas por horário mantendo filme
    vendas_por_horario = {}
    filme_por_horario = {}
    for item in dados_relatorio:
        horario = item['hora_sessao']
        if horario not in vendas_por_horario:
            vendas_por_horario[horario] = 0
            filme_por_horario[horario] = item['nome_filme']
        vendas_por_horario[horario] += 1
    
    # Ordenar por horário
    sorted_horarios = sorted(vendas_por_horario.items(), key=lambda x: x[0])
    
    if not sorted_horarios:
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#2B2B2B')
        ax.text(0.5, 0.5, 'Nenhum ingresso\nvendido\nno período', 
                ha='center', va='center', color='white', fontsize=12, transform=ax.transAxes)
        ax.set_title(f'Ingressos por Horário da sessão - {periodo.upper()}', color='white', fontsize=12, pad=20)
        return fig
    
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='#2B2B2B')
    ax.set_facecolor('#2B2B2B')
    
    # Converter horários para strings formatadas
    horarios_str = []
    vendas = []
    cores_barras = []
    for horario, venda in sorted_horarios:
        if horario:
            # Converter timedelta para string HH:MM
            total_seconds = int(horario.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            horario_str = f"{hours:02d}:{minutes:02d}"
        else:
            horario_str = "00:00"
        horarios_str.append(horario_str)
        vendas.append(venda)
        # Obter cor consistente para o filme deste horário
    cores_barras.append(obter_cor_filme(filme_por_horario[horario], cache_cores))
    
    bars = ax.bar(horarios_str, vendas, color=cores_barras, width=0.6)
    
    ax.set_title(f'Ingressos por Horário da sessão - {periodo.upper()}', color='white', fontsize=12, pad=20)
    ax.set_xlabel('Horário', color='white', fontsize=10)
    ax.set_ylabel('Ingressos Vendidos', color='white', fontsize=10)
    ax.tick_params(colors='white', labelsize=8)
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', color='white', fontsize=8)
    
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
        plt.subplots_adjust(bottom=0.15, top=0.9, left=0.1, right=0.95)
    
    return fig

def criar_grafico_vendas_cliente(dados_relatorio, periodo, cache_cores=None):
    """Cria gráfico de barras horizontais para top 10 clientes com mais vendas"""
    if not dados_relatorio:
        return None
    
    if cache_cores is None:
        cache_cores = {}
    
    # Agregar vendas por cliente
    vendas_por_cliente = {}
    for item in dados_relatorio:
        cliente_id = item['id_cliente']
        if cliente_id not in vendas_por_cliente:
            vendas_por_cliente[cliente_id] = 0
        vendas_por_cliente[cliente_id] += 1
    
    # Top 10 clientes
    sorted_clientes = sorted([(c, v) for c, v in vendas_por_cliente.items()], key=lambda x: x[1], reverse=True)[:10]
    
    if not sorted_clientes:
        fig, ax = plt.subplots(figsize=(6, 5), facecolor='#2B2B2B')
        ax.text(0.5, 0.5, 'Nenhum cliente\ncom vendas\nno período', 
                ha='center', va='center', color='white', fontsize=12, transform=ax.transAxes)
        ax.set_title(f'Top Clientes - {periodo.upper()}', color='white', fontsize=12, pad=20)
        return fig
    
    fig, ax = plt.subplots(figsize=(6, 5), facecolor='#2B2B2B')
    ax.set_facecolor('#2B2B2B')
    
    clientes = [f"Cliente {cliente}" for cliente, _ in sorted_clientes]
    vendas = [venda for _, venda in sorted_clientes]
    
    # Usar cores do cache para os clientes
    cores = [obter_cor_filme(f"Cliente {cliente}", cache_cores) for cliente, _ in sorted_clientes]
    
    bars = ax.barh(clientes, vendas, color=cores, height=0.6)
    
    ax.set_title(f'Top Clientes - {periodo.upper()}', color='white', fontsize=12, pad=20)
    ax.set_xlabel('Ingressos Vendidos', color='white', fontsize=10)
    ax.tick_params(colors='white', labelsize=9)
    
    # Adicionar valores nas barras
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                f'{int(width)}', ha='left', va='center', color='white', fontsize=9)
    
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
        plt.subplots_adjust(bottom=0.15, top=0.9, left=0.2, right=0.95)
    
    return fig

def criar_tela_dashboard(parent, voltar_callback=None, fonte_global=None):
    """Cria e retorna o frame do dashboard de relatórios"""
    
    # Frame principal
    frame = ctk.CTkFrame(parent, fg_color="transparent", width=1800, height=900)
    frame.pack_propagate(False)
    
    # Variável para armazenar o período selecionado
    periodo_selecionado = ctk.StringVar(value="diário")
    
    # Cache de cores para manter consistência entre gráficos
    cache_cores_filmes = {}
    
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
    
    # Container interno para centralizar os botões
    frame_botoes_interno = ctk.CTkFrame(frame_botoes_periodo, fg_color="transparent")
    frame_botoes_interno.pack(expand=True)
    
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
            frame_botoes_interno,
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
    
    # Funções para aumentar/diminuir fonte em TODA a tela
    def aumentar_fonte_relatorio():
        if fonte_global and fonte_global.cget("size") < 22:
            fonte_global.configure(size=fonte_global.cget("size") + 2)
            # Atualizar fonte das abas também
            fonte_abas.configure(size=fonte_global.cget("size") + 2)
            tabview._segmented_button.configure(font=fonte_abas)
    
    def diminuir_fonte_relatorio():
        if fonte_global and fonte_global.cget("size") > 6:
            fonte_global.configure(size=fonte_global.cget("size") - 2)
            # Atualizar fonte das abas também
            fonte_abas.configure(size=fonte_global.cget("size") + 2)
            tabview._segmented_button.configure(font=fonte_abas)
    
    # Botões para controle de fonte
    frame_controle_fonte = ctk.CTkFrame(frame_direita, fg_color="transparent")
    frame_controle_fonte.pack(pady=10)
    ctk.CTkButton(frame_controle_fonte, text="A+", command=aumentar_fonte_relatorio, width=40, height=35, 
                  font=fonte_global if fonte_global else ("Arial", 12, "bold")).pack(side="left", padx=3)
    ctk.CTkButton(frame_controle_fonte, text="A-", command=diminuir_fonte_relatorio, width=40, height=35,
                  font=fonte_global if fonte_global else ("Arial", 12, "bold")).pack(side="left", padx=3)    
    # Botão para alternar tema claro e escuro
    botao_tema = ctk.CTkButton(
        frame_controle_fonte,
        text="🌙",
        command=lambda: alternar_tema(parent, botao_tema),
        width=40,
        height=35,
        font=fonte_global,
        fg_color=BTN_COLOR,
        hover_color=BTN_HOVER,
        text_color=BTN_TEXT
    )
    botao_tema.pack(side="left", padx=3)    
    # FRAME INFERIOR: Abas para Gráficos
    frame_inferior = ctk.CTkFrame(frame)
    frame_inferior.pack(fill="both", expand=True, padx=12, pady=(0, 0))
    
    # Criar tabview para os gráficos
    tabview = ctk.CTkTabview(frame_inferior, width=1800, height=600)
    tabview.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Aumentar fonte das abas
    if fonte_global:
        fonte_abas = ctk.CTkFont(family=fonte_global.cget("family"), size=fonte_global.cget("size") + 2)
    else:
        fonte_abas = ctk.CTkFont(family="Arial", size=16)
    tabview._segmented_button.configure(font=fonte_abas)
    
    # Criar abas para cada gráfico
    abas = [
        "Vendas por Filme",
        "Faturamento por Período", 
        "Ocupação das Sessões",
        "Filmes Mais Populares",
        "Ingressos por Horário da sessão",
        "Vendas por Cliente"
    ]
    
    frames_abas = {}
    for aba in abas:
        tabview.add(aba)
        frame_aba = ctk.CTkFrame(tabview.tab(aba), fg_color="transparent")
        frame_aba.pack(fill="both", expand=True, padx=10, pady=20)
        
        # Frame para o gráfico
        frame_grafico_aba = ctk.CTkFrame(frame_aba, border_width=2, border_color="#444444", corner_radius=10)
        frame_grafico_aba.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Placeholder para o gráfico
        ctk.CTkLabel(
            frame_grafico_aba,
            text=f"Gráfico {aba} será exibido aqui",
            text_color="gray",
            font=fonte_global if fonte_global else ("Arial", 18)
        ).pack(expand=True, fill="both", padx=20, pady=20)
        
        frames_abas[aba] = frame_grafico_aba
    
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
        dados_relatorio = get_dados_relatorio(periodo_atual)
        
        # Atualizar gráfico 1: Vendas por Filme (com cache de cores)
        fig1 = criar_grafico_vendas_filme(dados_relatorio, periodo_atual, cache_cores_filmes)
        atualizar_frame_grafico(frames_abas["Vendas por Filme"], fig1, "Vendas por Filme")
        
        # Atualizar gráfico 2: Faturamento por Período (com cache de cores)
        fig2 = criar_grafico_faturamento_periodo(dados_relatorio, periodo_atual, cache_cores_filmes)
        atualizar_frame_grafico(frames_abas["Faturamento por Período"], fig2, "Faturamento por Período")
        
        # Atualizar gráfico 3: Ocupação das Sessões (com cache de cores)
        fig3 = criar_grafico_ocupacao_sessoes(dados_relatorio, periodo_atual, cache_cores_filmes)
        atualizar_frame_grafico(frames_abas["Ocupação das Sessões"], fig3, "Ocupação das Sessões")
        
        # Atualizar gráfico 4: Filmes Mais Populares (com cache de cores)
        fig4 = criar_grafico_filmes_populares(dados_relatorio, periodo_atual, cache_cores_filmes)
        atualizar_frame_grafico(frames_abas["Filmes Mais Populares"], fig4, "Filmes Mais Populares")
        
        # Atualizar gráfico 5: Ingressos por Horário da sessão (com cache de cores)
        fig5 = criar_grafico_ingressos_horario(dados_relatorio, periodo_atual, cache_cores_filmes)
        atualizar_frame_grafico(frames_abas["Ingressos por Horário da sessão"], fig5, "Ingressos por Horário da sessão")
        
        # Atualizar gráfico 6: Vendas por Cliente (com cache de cores)
        fig6 = criar_grafico_vendas_cliente(dados_relatorio, periodo_atual, cache_cores_filmes)
        atualizar_frame_grafico(frames_abas["Vendas por Cliente"], fig6, "Vendas por Cliente")
        
        # Calcular estatísticas gerais dos dados
        if dados_relatorio:
            ingressos_total = len(dados_relatorio)
            faturamento_total = sum(item['valor'] or 0 for item in dados_relatorio)
            clientes_unicos = len(set(item['id_cliente'] for item in dados_relatorio))
            
            titulo_texto = f"RELATÓRIOS - {periodo_atual.upper()}\n"
            titulo_texto += f"Ingressos: {ingressos_total:,}".replace(",", ".") + " | "
            titulo_texto += f"Faturamento: R$ {faturamento_total:,.2f}".replace(",", ".") + " | "
            titulo_texto += f"Clientes: {clientes_unicos:,}".replace(",", ".")
            
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
    
    # Carregar dados iniciais
    atualizar_graficos()
    
    return frame