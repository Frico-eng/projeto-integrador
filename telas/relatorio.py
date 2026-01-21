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
    
    # Se período é mensal, mostrar dia a dia do mês atual
    if periodo == "mensal":
        from datetime import datetime
        agora = datetime.now()
        ano_atual = agora.year
        mes_atual = agora.month
        
        faturamento_por_dia = {}
        
        # Agregar faturamento por dia do mês atual
        for item in dados_relatorio:
            data_compra = item.get('data_compra')
            if data_compra:
                try:
                    if isinstance(data_compra, str):
                        # Parser de string YYYY-MM-DD HH:MM:SS
                        ano = int(data_compra.split('-')[0])
                        mes = int(data_compra.split('-')[1])
                        dia = int(data_compra.split('-')[2].split()[0])
                    else:
                        # datetime object
                        ano = data_compra.year
                        mes = data_compra.month
                        dia = data_compra.day
                    
                    # Filtrar apenas dados do mês e ano atual
                    if ano == ano_atual and mes == mes_atual:
                        if dia not in faturamento_por_dia:
                            faturamento_por_dia[dia] = 0
                        faturamento_por_dia[dia] += item['valor'] or 0
                except:
                    pass
        
        # Calcular número de dias no mês
        import calendar
        num_dias = calendar.monthrange(ano_atual, mes_atual)[1]
        
        # Criar gráfico com todos os dias do mês
        dias = []
        faturamentos = []
        
        for dia in range(1, num_dias + 1):
            dias.append(str(dia))
            faturamentos.append(faturamento_por_dia.get(dia, 0))
        
        fig, ax = plt.subplots(figsize=(14, 5), facecolor='#2B2B2B')
        ax.set_facecolor('#2B2B2B')
        
        # Usar cor consistente
        cor_linha = obter_cor_filme("Faturamento", cache_cores) if dados_relatorio else BTN_COLOR
        ax.plot(range(len(dias)), faturamentos, marker='o', color=cor_linha, linewidth=2.5, markersize=6, label='Faturamento')
        
        # Adicionar preenchimento sob a linha
        ax.fill_between(range(len(dias)), faturamentos, alpha=0.2, color=cor_linha)
        
        meses_nomes = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
                      7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
        ax.set_title(f'Faturamento por Dia - {meses_nomes[mes_atual]} {ano_atual}', color='white', fontsize=14, pad=20, fontweight='bold')
        ax.set_xlabel('Dia', color='white', fontsize=11)
        ax.set_ylabel('Faturamento (R$)', color='white', fontsize=11)
        
        # Configurar ticks a cada 5 dias para não ficar muito cheio
        tick_positions = range(0, len(dias), max(1, len(dias) // 10))
        ax.set_xticks(tick_positions)
        ax.set_xticklabels([dias[i] for i in tick_positions], color='white', fontsize=8)
        
        # Formatar valores no eixo Y
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}K' if x >= 1000 else f'R$ {x:.0f}'))
        
        # Adicionar grid
        ax.grid(axis='y', alpha=0.3, color='white', linestyle='--', linewidth=0.5)
        
        # Adicionar valores nos pontos (apenas alguns para não ficar poluído)
        max_valor = float(max(faturamentos)) if faturamentos else 1
        if max_valor > 0:
            for i, (x, y) in enumerate(zip(range(len(dias)), faturamentos)):
                if y > 0 and i % 2 == 0:  # Mostrar a cada 2 dias
                    y_float = float(y)
                    ax.text(x, y_float + max_valor * 0.03, f'R$ {y_float:.0f}', 
                           ha='center', va='bottom', color='white', fontsize=6)
        
        ax.tick_params(colors='white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        
        try:
            plt.tight_layout()
        except ValueError:
            plt.subplots_adjust(bottom=0.15, top=0.9, left=0.1, right=0.95)
        
        return fig
    
    # Se período é quatrenal, mostrar 4 trimestres
    elif periodo == "quatrenal":
        faturamento_por_trimestre = {}
        trimestres_nomes = {
            1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'
        }
        
        # Agregar faturamento por trimestre
        for item in dados_relatorio:
            data_compra = item.get('data_compra')
            if data_compra:
                try:
                    if isinstance(data_compra, str):
                        mes = int(data_compra.split('-')[1])
                    else:
                        mes = data_compra.month
                    
                    trimestre = ((mes - 1) // 3) + 1
                    
                    if trimestre not in faturamento_por_trimestre:
                        faturamento_por_trimestre[trimestre] = 0
                    faturamento_por_trimestre[trimestre] += item['valor'] or 0
                except:
                    pass
        
        # Criar gráfico com todos os 4 trimestres
        trimestres = []
        faturamentos = []
        
        for trimestre in range(1, 5):
            trimestres.append(trimestres_nomes[trimestre])
            faturamentos.append(faturamento_por_trimestre.get(trimestre, 0))
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#2B2B2B')
        ax.set_facecolor('#2B2B2B')
        
        # Usar cor consistente
        cor_linha = obter_cor_filme("Faturamento", cache_cores) if dados_relatorio else BTN_COLOR
        ax.plot(range(len(trimestres)), faturamentos, marker='o', color=cor_linha, linewidth=2.5, markersize=10, label='Faturamento')
        
        # Adicionar preenchimento sob a linha
        ax.fill_between(range(len(trimestres)), faturamentos, alpha=0.2, color=cor_linha)
        
        ax.set_title('Faturamento por Trimestre', color='white', fontsize=14, pad=20, fontweight='bold')
        ax.set_xlabel('Trimestre', color='white', fontsize=11)
        ax.set_ylabel('Faturamento (R$)', color='white', fontsize=11)
        
        # Configurar ticks
        ax.set_xticks(range(len(trimestres)))
        ax.set_xticklabels(trimestres, color='white', fontsize=11)
        
        # Formatar valores no eixo Y
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}K' if x >= 1000 else f'R$ {x:.0f}'))
        
        # Adicionar grid
        ax.grid(axis='y', alpha=0.3, color='white', linestyle='--', linewidth=0.5)
        
        # Adicionar valores nos pontos
        max_valor = float(max(faturamentos)) if faturamentos else 1
        if max_valor > 0:
            for i, (x, y) in enumerate(zip(range(len(trimestres)), faturamentos)):
                if y > 0:
                    y_float = float(y)
                    ax.text(x, y_float + max_valor * 0.03, f'R$ {y_float:.0f}', 
                           ha='center', va='bottom', color='white', fontsize=9, fontweight='bold')
        
        ax.tick_params(colors='white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        
        try:
            plt.tight_layout()
        except ValueError:
            plt.subplots_adjust(bottom=0.15, top=0.9, left=0.1, right=0.95)
        
        return fig
    
    # Se período é anual, mostrar últimos 12 meses
    if periodo == "anual":
        faturamento_por_mes = {}
        
        # Agregar faturamento por mês
        for item in dados_relatorio:
            data_compra = item.get('data_compra')
            if data_compra:
                try:
                    if isinstance(data_compra, str):
                        # Parser de string YYYY-MM-DD HH:MM:SS
                        ano_mes = data_compra[:7]  # YYYY-MM
                    else:
                        # datetime object
                        ano_mes = data_compra.strftime('%Y-%m')
                    
                    if ano_mes not in faturamento_por_mes:
                        faturamento_por_mes[ano_mes] = 0
                    faturamento_por_mes[ano_mes] += item['valor'] or 0
                except:
                    pass
        
        # Ordenar por data
        meses_ordenados = sorted(faturamento_por_mes.keys())
        
        meses_labels = []
        faturamentos = []
        
        for mes_key in meses_ordenados:
            meses_labels.append(mes_key[:7].replace('-', '/'))
            faturamentos.append(faturamento_por_mes[mes_key])
        
        fig, ax = plt.subplots(figsize=(14, 5), facecolor='#2B2B2B')
        ax.set_facecolor('#2B2B2B')
        
        # Usar cor consistente
        cor_linha = obter_cor_filme("Faturamento", cache_cores) if dados_relatorio else BTN_COLOR
        ax.plot(range(len(meses_labels)), faturamentos, marker='o', color=cor_linha, linewidth=2.5, markersize=8, label='Faturamento')
        
        # Adicionar preenchimento sob a linha
        ax.fill_between(range(len(meses_labels)), faturamentos, alpha=0.2, color=cor_linha)
        
        ax.set_title('Faturamento por Mês (Últimos 12 Meses)', color='white', fontsize=14, pad=20, fontweight='bold')
        ax.set_xlabel('Mês', color='white', fontsize=11)
        ax.set_ylabel('Faturamento (R$)', color='white', fontsize=11)
        
        # Configurar ticks
        ax.set_xticks(range(len(meses_labels)))
        ax.set_xticklabels(meses_labels, color='white', fontsize=9, rotation=45, ha='right')
        
        # Formatar valores no eixo Y
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}K' if x >= 1000 else f'R$ {x:.0f}'))
        
        # Adicionar grid
        ax.grid(axis='y', alpha=0.3, color='white', linestyle='--', linewidth=0.5)
        
        # Adicionar valores nos pontos
        max_valor = float(max(faturamentos)) if faturamentos else 1
        if max_valor > 0:
            for i, (x, y) in enumerate(zip(range(len(meses_labels)), faturamentos)):
                if y > 0:
                    y_float = float(y)
                    ax.text(x, y_float + max_valor * 0.03, f'R$ {y_float:.0f}', 
                           ha='center', va='bottom', color='white', fontsize=7)
        
        ax.tick_params(colors='white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        
        try:
            plt.tight_layout()
        except ValueError:
            plt.subplots_adjust(bottom=0.15, top=0.9, left=0.1, right=0.95)
        
        return fig
    
    # ============ PARA OUTROS PERÍODOS (diário) ============
    faturamento_por_periodo = {}
    for item in dados_relatorio:
        if periodo == "diário":
            if item['hora_sessao']:
                horas = int(item['hora_sessao'].total_seconds() // 3600)
                periodo_key = f"{horas:02d}"
            else:
                periodo_key = '00'
        else:
            periodo_key = item['data_sessao'].strftime('%Y-%m-%d') if item['data_sessao'] else 'N/A'
        
        if periodo_key not in faturamento_por_periodo:
            faturamento_por_periodo[periodo_key] = 0
        faturamento_por_periodo[periodo_key] += item['valor'] or 0
    
    sorted_periodos = sorted(faturamento_por_periodo.items(), key=lambda x: x[0])
    
    if periodo == "diário":
        limite = 5
        figsize = (6, 4)
    else:
        limite = 5
        figsize = (6, 4)
    
    dados_top = sorted_periodos[-limite:] if len(sorted_periodos) > limite else sorted_periodos
    
    if not dados_top:
        return None
    
    fig, ax = plt.subplots(figsize=figsize, facecolor='#2B2B2B')
    ax.set_facecolor('#2B2B2B')
    
    periodos = [p for p, _ in dados_top]
    faturamento = [f for _, f in dados_top]
    
    if periodo == "diário":
        periodos_labels = [f"{int(p):02d}:00" if p != 'N/A' else 'N/A' for p in periodos]
    else:
        periodos_labels = periodos
    
    cor_linha = obter_cor_filme("Faturamento", cache_cores) if dados_relatorio else BTN_COLOR
    ax.plot(range(len(periodos)), faturamento, marker='o', color=cor_linha, linewidth=2, markersize=6)
    
    # Adicionar preenchimento sob a linha
    ax.fill_between(range(len(periodos)), faturamento, alpha=0.2, color=cor_linha)
    
    ax.set_title(f'Faturamento por Período - {periodo.upper()}', color='white', fontsize=12, pad=20)
    ax.set_xlabel('Períodos', color='white', fontsize=10)
    ax.set_ylabel('Faturamento (R$)', color='white', fontsize=10)
    
    ax.set_xticks(range(len(periodos)))
    ax.set_xticklabels(periodos_labels, rotation=45, ha='right', color='white', fontsize=8)
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:.0f}'))
    
    # Adicionar valores nos pontos
    max_valor = float(max(faturamento)) if faturamento else 1
    if max_valor > 0:
        for i, (x, y) in enumerate(zip(range(len(periodos)), faturamento)):
            if y > 0:
                y_float = float(y)
                ax.text(x, y_float + max_valor * 0.03, f'R$ {y_float:.0f}', 
                       ha='center', va='bottom', color='white', fontsize=8)
    
    ax.tick_params(colors='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    
    try:
        plt.tight_layout()
    except ValueError:
        plt.subplots_adjust(bottom=0.2, top=0.9, left=0.1, right=0.95)
    
    return fig

def criar_grafico_ocupacao_sessoes(dados_relatorio, periodo, cache_cores=None):
    """Cria gráfico de barras para vendas por sessão com cores por filme"""
    if not dados_relatorio:
        return None
    
    if cache_cores is None:
        cache_cores = {}
    
    # Se período é mensal, agregar por dia do mês atual
    if periodo == "mensal":
        from datetime import datetime
        import calendar
        agora = datetime.now()
        ano_atual = agora.year
        mes_atual = agora.month
        
        vendas_por_dia = {}
        
        # Agregar vendas por dia do mês atual
        for item in dados_relatorio:
            data_compra = item.get('data_compra')
            if data_compra:
                try:
                    if isinstance(data_compra, str):
                        ano = int(data_compra.split('-')[0])
                        mes = int(data_compra.split('-')[1])
                        dia = int(data_compra.split('-')[2].split()[0])
                    else:
                        ano = data_compra.year
                        mes = data_compra.month
                        dia = data_compra.day
                    
                    # Filtrar apenas dados do mês e ano atual
                    if ano == ano_atual and mes == mes_atual:
                        if dia not in vendas_por_dia:
                            vendas_por_dia[dia] = 0
                        vendas_por_dia[dia] += 1
                except:
                    pass
        
        # Calcular número de dias no mês
        num_dias = calendar.monthrange(ano_atual, mes_atual)[1]
        
        # Criar estrutura com todos os dias do mês
        dias = []
        vendas_lista = []
        labels_dias = []
        
        for dia in range(1, num_dias + 1):
            dias.append(dia)
            vendas_lista.append(vendas_por_dia.get(dia, 0))
            labels_dias.append(str(dia))
        
        fig, ax = plt.subplots(figsize=(14, 5), facecolor='#2B2B2B')
        ax.set_facecolor('#2B2B2B')
        
        # Cores alternadas para dias
        cores_barras = ['#F6C148' if i % 2 == 0 else '#E2952D' for i in range(num_dias)]
        bars = ax.bar(labels_dias, vendas_lista, color=cores_barras, width=0.7, alpha=0.8)
        
        meses_nomes = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
                      7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
        ax.set_title(f'Ocupação por Dia - {meses_nomes[mes_atual]} {ano_atual}', color='white', fontsize=14, pad=20, fontweight='bold')
        ax.set_xlabel('Dia', color='white', fontsize=11)
        ax.set_ylabel('Ingressos Vendidos', color='white', fontsize=11)
        ax.tick_params(colors='white', labelsize=8)
        
        # Adicionar valores nas barras (apenas para dias com vendas)
        for bar, venda in zip(bars, vendas_lista):
            if venda > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + max(vendas_lista)*0.02,
                        f'{int(venda)}', ha='center', va='bottom', color='white', fontsize=7, fontweight='bold')
        
        # Configurar grid
        ax.grid(axis='y', alpha=0.3, color='white', linestyle='--', linewidth=0.5)
        
        ax.tick_params(colors='white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        
        try:
            plt.tight_layout()
        except ValueError:
            plt.subplots_adjust(bottom=0.15, top=0.9, left=0.1, right=0.95)
        
        return fig
    
    # Se período é quatrenal, agregar por trimestre
    elif periodo == "quatrenal":
        vendas_por_trimestre = {}
        trimestres_nomes = {
            1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'
        }
        
        # Agregar vendas por trimestre
        for item in dados_relatorio:
            data_compra = item.get('data_compra')
            if data_compra:
                try:
                    if isinstance(data_compra, str):
                        mes = int(data_compra.split('-')[1])
                    else:
                        mes = data_compra.month
                    
                    trimestre = ((mes - 1) // 3) + 1
                    
                    if trimestre not in vendas_por_trimestre:
                        vendas_por_trimestre[trimestre] = 0
                    vendas_por_trimestre[trimestre] += 1
                except:
                    pass
        
        # Criar estrutura com todos os 4 trimestres
        trimestres = []
        vendas_lista = []
        labels_trimestres = []
        
        for trimestre in range(1, 5):
            trimestres.append(trimestre)
            vendas_lista.append(vendas_por_trimestre.get(trimestre, 0))
            labels_trimestres.append(trimestres_nomes[trimestre])
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#2B2B2B')
        ax.set_facecolor('#2B2B2B')
        
        cores_barras = ['#F6C148' if i % 2 == 0 else '#E2952D' for i in range(4)]
        bars = ax.bar(labels_trimestres, vendas_lista, color=cores_barras, width=0.6, alpha=0.8)
        
        ax.set_title('Ocupação por Trimestre', color='white', fontsize=14, pad=20, fontweight='bold')
        ax.set_xlabel('Trimestre', color='white', fontsize=11)
        ax.set_ylabel('Ingressos Vendidos', color='white', fontsize=11)
        ax.tick_params(colors='white', labelsize=11)
        
        # Adicionar valores nas barras com conversão float
        for bar, venda in zip(bars, vendas_lista):
            if venda > 0:
                height = float(bar.get_height())
                venda_float = float(venda)
                ax.text(bar.get_x() + bar.get_width()/2., height + venda_float * 0.03,
                        f'{int(venda_float)}', ha='center', va='bottom', color='white', fontsize=10, fontweight='bold')
        
        # Configurar grid
        ax.grid(axis='y', alpha=0.3, color='white', linestyle='--', linewidth=0.5)
        
        ax.tick_params(colors='white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        
        try:
            plt.tight_layout()
        except ValueError:
            plt.subplots_adjust(bottom=0.15, top=0.9, left=0.1, right=0.95)
        
        return fig
    
    # Se período é anual, agregar por mês dos últimos 12 meses
    elif periodo == "anual":
        vendas_por_mes = {}
        
        # Agregar vendas por mês
        for item in dados_relatorio:
            data_compra = item.get('data_compra')
            if data_compra:
                try:
                    if isinstance(data_compra, str):
                        # Parser de string YYYY-MM-DD HH:MM:SS
                        ano_mes = data_compra[:7]  # YYYY-MM
                    else:
                        # datetime object
                        ano_mes = data_compra.strftime('%Y-%m')
                    
                    if ano_mes not in vendas_por_mes:
                        vendas_por_mes[ano_mes] = 0
                    vendas_por_mes[ano_mes] += 1
                except:
                    pass
        
        # Ordenar por data
        meses_ordenados = sorted(vendas_por_mes.keys())
        
        meses_labels = []
        vendas_lista = []
        
        for mes_key in meses_ordenados:
            meses_labels.append(mes_key[:7].replace('-', '/'))
            vendas_lista.append(vendas_por_mes[mes_key])
        
        fig, ax = plt.subplots(figsize=(14, 5), facecolor='#2B2B2B')
        ax.set_facecolor('#2B2B2B')
        
        # Cores alternadas
        cores_barras = ['#F6C148' if i % 2 == 0 else '#E2952D' for i in range(len(meses_labels))]
        bars = ax.bar(meses_labels, vendas_lista, color=cores_barras, width=0.6, alpha=0.8)
        
        ax.set_title('Ocupação por Mês (Últimos 12 Meses)', color='white', fontsize=14, pad=20, fontweight='bold')
        ax.set_xlabel('Mês', color='white', fontsize=11)
        ax.set_ylabel('Ingressos Vendidos', color='white', fontsize=11)
        ax.tick_params(colors='white', labelsize=9)
        
        # Adicionar valores nas barras
        for bar, venda in zip(bars, vendas_lista):
            if venda > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + max(vendas_lista)*0.02,
                        f'{int(venda)}', ha='center', va='bottom', color='white', fontsize=8, fontweight='bold')
        
        # Configurar grid
        ax.grid(axis='y', alpha=0.3, color='white', linestyle='--', linewidth=0.5)
        
        ax.tick_params(colors='white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        
        try:
            plt.tight_layout()
        except ValueError:
            plt.subplots_adjust(bottom=0.15, top=0.9, left=0.1, right=0.95)
        
        return fig
    
    # PARA OUTROS PERÍODOS (não mensal, não anual, não quatrenal)
    # Agregar vendas por sessão mantendo referência ao filme e horário
    vendas_por_sessao = {}
    filme_por_sessao = {}
    horario_por_sessao = {}
    for item in dados_relatorio:
        data_sessao = item.get('data_sessao')
        if isinstance(data_sessao, str):
            data_str = data_sessao
        else:
            data_str = str(data_sessao)
        
        sessao_key = f"{item['nome_filme'][:10]}... {data_str} {item['hora_sessao']}"
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
        ("Trimestral", "quatrenal"),
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