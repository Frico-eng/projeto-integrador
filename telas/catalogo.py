import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime, timedelta
from crud.crud_filme import listar_filmes
from crud.crud_sessao import listar_sessoes_por_filme
from crud.crud_sessao_assento import obter_sessoes_com_disponibilidade, alertar_pouca_disponibilidade
from utilidades.ui_helpers import alternar_tema
from utilidades.config import BTN_COLOR, BTN_HOVER, BTN_TEXT

# ================== CONSTANTES DE CORES ==================
BTN_COLOR = "#F6C148"
BTN_HOVER = "#E2952D"
BTN_TEXT = "#1C2732"
FILME_SELECIONADO_COLOR = "#B6D8F1"
FILME_NORMAL_COLOR = "#F6C148"
SELECTED_COLOR = "#B6D8F1"

# ================== CONSTANTES DE CAMINHOS ==================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "utilidades", "images")

CLASSIFICACOES = {
    "LIVRE": os.path.join(IMAGE_DIR, "livre.png"),
    "10": os.path.join(IMAGE_DIR, "dez.png"),
    "12": os.path.join(IMAGE_DIR, "doze.png"),
    "14": os.path.join(IMAGE_DIR, "catorze.jpg"),
    "16": os.path.join(IMAGE_DIR, "dezesseis.png"),
    "18": os.path.join(IMAGE_DIR, "dezoito.png"),
}

def carregar_filmes_do_banco():
    try:
        filmes_db = listar_filmes()
        filmes_formatados = []
        
        for filme in filmes_db:
            filme_formatado = {
                "ID_Filme": filme["ID_Filme"],
                "titulo": filme["Titulo_Filme"],
                "genero": filme["Genero"],
                "duracao": f"{filme['Duracao']} min",
                "classificacao": CLASSIFICACOES.get(filme["Classificacao"], ""),
                "cartaz_path": filme.get("Cartaz_Path", ""),
                "direcao": filme.get("Direcao", "Direção não informada"),
                "sinopse": filme.get("Sinopse", "Sinopse não disponível.")
            }
            filmes_formatados.append(filme_formatado)
        
        return filmes_formatados
    except Exception as e:
        print(f"Erro ao carregar filmes do banco: {e}")
        return []

def carregar_sessoes_do_banco(id_filme):
    try:
        sessoes_db = listar_sessoes_por_filme(id_filme)
        sessoes_formatadas = {
            "dublado": [],
            "legendado": []
        }
        
        for sessao in sessoes_db:
            hora = sessao.get("Hora_Formatada", "")
            tipo = sessao["Tipo_Sessao"]
            
            if tipo == "dublado" and hora:
                sessoes_formatadas["dublado"].append(hora)
            elif tipo == "legendado" and hora:
                sessoes_formatadas["legendado"].append(hora)
        
        sessoes_formatadas["dublado"].sort()
        sessoes_formatadas["legendado"].sort()
        
        return sessoes_formatadas
    except Exception as e:
        print(f"Erro ao carregar sessões do banco: {e}")
        return {"dublado": [], "legendado": []}

def criar_tela_catalogo(parent, voltar_callback=None, confirmar_callback=None, fonte_global=None):
    """Cria e retorna o frame do catálogo de filmes"""
    
    # Funções para aumentar/diminuir fonte se fonte_global for fornecida
    def aumentar_fonte():
        if fonte_global and fonte_global.cget("size") < 22:  # 14 + (4 * 2)
            fonte_global.configure(size=fonte_global.cget("size") + 2)

    def diminuir_fonte():
        if fonte_global and fonte_global.cget("size") > 6:  # 14 - (4 * 2)
            fonte_global.configure(size=fonte_global.cget("size") - 2)
    
    # Frame principal
    frame = ctk.CTkFrame(parent, fg_color="transparent", width=1800, height=900)
    frame.pack_propagate(False)
    frame.image_cache = {}

    # Variáveis de controle
    dia_selecionado = ctk.StringVar(value="")
    tipo_selecionado = ctk.StringVar(value="")
    horario_selecionado = ctk.StringVar(value="")
    
    titulo_var = ctk.StringVar(value="Selecione um filme")
    sinopse_var = ctk.StringVar(value="Sinopse do filme aparecerá aqui.")
    direcao_var = ctk.StringVar(value="Direção do filme aparecerá aqui.")
    genero_var = ctk.StringVar(value="Gênero do filme aparecerá aqui.")
    duracao_var = ctk.StringVar(value="Duração do filme aparecerá aqui.")

    filme_selecionado = [None]
    botoes_dias = []
    botoes_filmes = []
    
    # Listas para armazenar botões de horário por tipo
    botoes_horarios_dublado = []
    botoes_horarios_legendado = []

    # ================== LAYOUT PRINCIPAL ==================
    
    # FRAME SUPERIOR: Apenas Dias
    frame_superior = ctk.CTkFrame(frame, height=90)
    frame_superior.pack(fill="x", padx=12, pady=(12, 6))
    frame_superior.pack_propagate(False)

    # Botões para controle de fonte se fonte_global for fornecida
    if fonte_global:
        frame_controle_fonte = ctk.CTkFrame(frame_superior, fg_color="transparent")
        frame_controle_fonte.pack(side="right", padx=10, pady=5)
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

    # Dias
    frame_dias = ctk.CTkFrame(frame_superior, fg_color="transparent")
    frame_dias.pack(fill="x", pady=5)
    ctk.CTkLabel(frame_dias, text="Dias:", font=fonte_global if fonte_global else ("Arial", 14, "bold")).pack(pady=(0, 0))
    
    frame_dias_container = ctk.CTkFrame(frame_dias, fg_color="transparent")
    frame_dias_container.pack(anchor="center", pady=0)

    # FRAME MEIO: Lista de filmes (scroll horizontal)
    frame_meio = ctk.CTkFrame(frame, height=310)
    frame_meio.pack(fill="x", padx=12, pady=6)
    frame_meio.pack_propagate(False)

    # Container para botões de navegação e scroll
    nav_container = ctk.CTkFrame(frame_meio, fg_color="transparent")
    nav_container.pack(fill="both", expand=True)

    # Botão esquerda
    btn_left = ctk.CTkButton(nav_container, text="←", width=40, height=40, corner_radius=20,
                            fg_color=BTN_COLOR, hover_color=BTN_HOVER, text_color=BTN_TEXT,
                            font=fonte_global if fonte_global else ("Arial", 18),
                            command=lambda: canvas.xview_scroll(-1, "units"))
    btn_left.pack(side="left", padx=(0, 5), pady=10)

    scroll_container = ctk.CTkFrame(nav_container, fg_color="transparent")
    scroll_container.pack(fill="both", expand=True, side="left", padx=0, pady=0)

    canvas = tk.Canvas(scroll_container, height=350, bg='#2b2b2b', highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(scroll_container, orientation="horizontal", command=canvas.xview)
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="transparent")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    canvas.pack(side="top", fill="both", expand=True)
    scrollbar.pack(side="bottom", fill="x")

    # Botão direita
    btn_right = ctk.CTkButton(nav_container, text="→", width=40, height=40, corner_radius=20,
                             fg_color=BTN_COLOR, hover_color=BTN_HOVER, text_color=BTN_TEXT,
                             font=fonte_global if fonte_global else ("Arial", 18),
                             command=lambda: canvas.xview_scroll(1, "units"))
    btn_right.pack(side="right", padx=(5, 0), pady=10)

    # FRAME INFERIOR: Detalhes do filme e Horários por Tipo
    frame_inferior = ctk.CTkFrame(frame, height=660)
    frame_inferior.pack(fill="both", expand=True, padx=12, pady=(6, 12))

    # Frame esquerdo: detalhes do filme
    frame_esquerdo = ctk.CTkFrame(frame_inferior, width=600)
    frame_esquerdo.pack(side="left", fill="both", expand=True, padx=(0, 6), pady=10)
    frame_esquerdo.pack_propagate(False)

    # Frame direito: Horários por tipo de sessão
    frame_direito = ctk.CTkFrame(frame_inferior, width=600)
    frame_direito.pack(side="right", fill="both", padx=(6, 0), pady=10)
    frame_direito.pack_propagate(False)

    # ===== CONTEÚDO DO FRAME ESQUERDO (DETALHES DO FILME) =====
    frame_top = ctk.CTkFrame(frame_esquerdo)
    frame_top.pack(fill="x", padx=12, pady=10)

    # Imagem do filme
    frame_imagem = ctk.CTkFrame(frame_top, width=200, height=290)
    frame_imagem.pack(side="left", padx=0, pady=0)
    frame_imagem.pack_propagate(False)

    label_imagem = ctk.CTkLabel(frame_imagem, text="")
    label_imagem.pack(expand=True, fill="both", padx=5, pady=5)

    # Textos do filme
    frame_textos = ctk.CTkFrame(frame_top, fg_color="transparent")
    frame_textos.pack(side="left", fill="both", expand=True, padx=20)

    label_titulo = ctk.CTkLabel(frame_textos, textvariable=titulo_var, font=fonte_global if fonte_global else ("Arial", 18, "bold"))
    label_titulo.pack(anchor="nw", pady=(0,6))

    frame_info_basica = ctk.CTkFrame(frame_textos, fg_color="transparent")
    frame_info_basica.pack(anchor="nw", fill="x", pady=(0,6))

    # Direção
    ctk.CTkLabel(frame_info_basica, text="Direção:", font=fonte_global if fonte_global else ("Arial", 14, "bold")).pack(anchor="nw")
    label_direcao = ctk.CTkLabel(frame_info_basica, textvariable=direcao_var, wraplength=400, justify="left", font=fonte_global)
    label_direcao.pack(anchor="nw", pady=(0,6))

    # Duração
    ctk.CTkLabel(frame_info_basica, text="Duração:", font=fonte_global if fonte_global else ("Arial", 14, "bold")).pack(anchor="nw")
    label_duracao = ctk.CTkLabel(frame_info_basica, textvariable=duracao_var, wraplength=400, justify="left", font=fonte_global)
    label_duracao.pack(anchor="nw", pady=(0,0))

    # Gênero
    ctk.CTkLabel(frame_info_basica, text="Gênero:", font=fonte_global if fonte_global else ("Arial", 14, "bold")).pack(anchor="nw")
    label_genero = ctk.CTkLabel(frame_info_basica, textvariable=genero_var, wraplength=400, justify="left", font=fonte_global)
    label_genero.pack(anchor="nw", pady=(0,6))

    # Sinopse
    ctk.CTkLabel(frame_textos, text="Sinopse:", font=fonte_global if fonte_global else ("Arial", 14, "bold")).pack(anchor="nw", pady=(0,0))
    label_sinopse = ctk.CTkLabel(frame_textos, textvariable=sinopse_var, wraplength=850, justify="left", font=fonte_global)
    label_sinopse.pack(anchor="nw", pady=(0,0))

    # Classificação
    frame_classificacao = ctk.CTkFrame(frame_textos, fg_color="transparent")
    frame_classificacao.pack(anchor="nw", pady=(0,0))
    
    ctk.CTkLabel(frame_classificacao, text="Classificação:", font=fonte_global if fonte_global else ("Arial", 14, "bold")).pack(side="left")
    label_classificacao = ctk.CTkLabel(frame_classificacao, text="", width=50, height=50)
    label_classificacao.pack(side="left", padx=10)

    # ===== CONTEÚDO DO FRAME DIREITO (HORÁRIOS POR TIPO) =====
    ctk.CTkLabel(frame_direito, text="Horários por Tipo de Sessão", font=fonte_global if fonte_global else ("Arial", 16, "bold")).pack(pady=(10, 5))

    # Container principal para os tipos
    frame_tipos_container = ctk.CTkFrame(frame_direito, fg_color="transparent")
    frame_tipos_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Frame para Dublado
    frame_dublado = ctk.CTkFrame(frame_tipos_container, fg_color="transparent")
    frame_dublado.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(frame_dublado, text="Dublado", font=fonte_global if fonte_global else ("Arial", 14, "bold")).pack(anchor="w", pady=(0, 5))
    
    frame_horarios_dublado = ctk.CTkFrame(frame_dublado, fg_color="transparent")
    frame_horarios_dublado.pack(fill="x")

    # Frame para Legendado
    frame_legendado = ctk.CTkFrame(frame_tipos_container, fg_color="transparent")
    frame_legendado.pack(fill="x", pady=(0, 10))

    ctk.CTkLabel(frame_legendado, text="Legendado", font=fonte_global if fonte_global else ("Arial", 14, "bold")).pack(anchor="w", pady=(0, 5))
    
    frame_horarios_legendado = ctk.CTkFrame(frame_legendado, fg_color="transparent")
    frame_horarios_legendado.pack(fill="x")

    # Label para mostrar seleção atual
    label_selecao = ctk.CTkLabel(frame_direito, text="", font=fonte_global if fonte_global else ("Arial", 12, "bold"))
    label_selecao.pack(anchor="w", pady=10)

    # ===== BOTÕES DE NAVEGAÇÃO =====
    botoes_frame = ctk.CTkFrame(frame, height=50)
    botoes_frame.pack(side="bottom", fill="x", padx=20, pady=10)
    botoes_frame.pack_propagate(False)

    # ================== FUNÇÕES PRINCIPAIS ==================
    
    def gerar_proximos_dias():
        hoje = datetime.now()
        dias = []
        for i in range(3):
            dia = hoje + timedelta(days=i)
            dias.append({
                "data": dia,
                "label": dia.strftime("%d/%m"),
                "nome": dia.strftime("%A").replace("Monday", "Segunda").replace("Tuesday", "Terça")
                         .replace("Wednesday", "Quarta").replace("Thursday", "Quinta")
                         .replace("Friday", "Sexta").replace("Saturday", "Sábado")
                         .replace("Sunday", "Domingo")
            })
        return dias

    def criar_botao_dia(parent, dia_info):
        btn = ctk.CTkButton(parent, text=f"{dia_info['nome']}:{dia_info['label']}", 
                           width=200, height=40, corner_radius=10,
                           fg_color=BTN_COLOR, hover_color=BTN_HOVER, text_color=BTN_TEXT,
                           font=fonte_global if fonte_global else ("Arial", 18), command=lambda: selecionar_dia(dia_info))
        btn.pack(side="left", padx=5, pady=5)
        return btn

    def criar_botao_horario(parent, horario, tipo, sessoes_info=None):
        # Obter informações de disponibilidade se disponíveis
        texto_botao = horario
        tooltip = ""
        cor_botao = BTN_COLOR
        
        if sessoes_info:
            for sessao in sessoes_info:
                hora_formatada = str(sessao.get('Hora_Sessao', ''))[:5] if sessao.get('Hora_Sessao') else ''
                if hora_formatada == horario and sessao.get('Tipo_Sessao') == tipo:
                    disponiveis = sessao.get('assentos_livres', 0)
                    total = sessao.get('total_assentos', 0)
                    
                    if disponiveis <= 5 and disponiveis > 0:
                        cor_botao = "#FF9800"  # Laranja - poucos assentos
                        tooltip = f"⚠ {disponiveis} de {total} assentos"
                    elif disponiveis == 0:
                        cor_botao = "#999999"  # Cinza - cheio
                        tooltip = "Sessão cheia"
                    else:
                        tooltip = f"{disponiveis} de {total} assentos"
                    
                    texto_botao = horario
                    break
        
        btn = ctk.CTkButton(parent, text=texto_botao, width=120, height=50, corner_radius=8,
                           fg_color=cor_botao, hover_color=BTN_HOVER, text_color=BTN_TEXT,
                           font=fonte_global if fonte_global else ("Arial", 12), 
                           command=lambda: selecionar_horario(horario, tipo))
        btn.pack(side="left", padx=3, pady=2)
        btn.tooltip = tooltip  # Armazenar tooltip
        return btn

    def selecionar_dia(dia_info):
        dia_selecionado.set(dia_info)
        
        # Atualizar visual dos botões de dia
        for btn in botoes_dias:
            if btn.cget("text").split(':')[1] == dia_info['label']:
                btn.configure(fg_color=SELECTED_COLOR)
            else:
                btn.configure(fg_color=BTN_COLOR)
        
        # Resetar seleções
        horario_selecionado.set("")
        tipo_selecionado.set("")
        
        # Atualizar horários
        atualizar_horarios_por_tipo()

    def selecionar_horario(horario, tipo):
        if not dia_selecionado.get():
            messagebox.showwarning("Seleção Incompleta", "Selecione um dia primeiro")
            return
        
        # Verificar disponibilidade antes de permitir seleção
        if filme_selecionado[0]:
            sessoes_disponiveis = obter_sessoes_com_disponibilidade(
                filme_selecionado[0].get("ID_Filme"), 
                tipo
            )
            
            # Procurar a sessão com este horário
            sessao_selecionada = None
            for sessao in sessoes_disponiveis:
                hora_fmt = str(sessao.get('Hora_Sessao', ''))[:5]
                if hora_fmt == horario:
                    sessao_selecionada = sessao
                    break
            
            if not sessao_selecionada or not sessao_selecionada.get('disponivel', False):
                messagebox.showwarning(
                    "Sessão Indisponível", 
                    "Esta sessão não tem assentos disponíveis no momento.\nEscolha outro horário."
                )
                return
        
        horario_selecionado.set(horario)
        tipo_selecionado.set(tipo)
        
        # Atualizar visual dos botões de horário
        # Resetar todos os botões primeiro
        for btn in botoes_horarios_dublado + botoes_horarios_legendado:
            btn.configure(fg_color=BTN_COLOR)
        
        # Destacar o botão selecionado
        if tipo == "dublado":
            for btn in botoes_horarios_dublado:
                if btn.cget("text").split('\n')[0] == horario:
                    btn.configure(fg_color=SELECTED_COLOR)
        else:  # legendado
            for btn in botoes_horarios_legendado:
                if btn.cget("text").split('\n')[0] == horario:
                    btn.configure(fg_color=SELECTED_COLOR)
        
        atualizar_selecao()

    def atualizar_horarios_por_tipo():
        """Atualiza os horários para cada tipo de sessão com info de disponibilidade"""
        # Limpar botões existentes
        for widget in frame_horarios_dublado.winfo_children():
            widget.destroy()
        for widget in frame_horarios_legendado.winfo_children():
            widget.destroy()
        
        botoes_horarios_dublado.clear()
        botoes_horarios_legendado.clear()
        
        if not dia_selecionado.get() or not filme_selecionado[0]:
            return
        
        filme = filme_selecionado[0]
        id_filme = filme.get("ID_Filme")
        
        if id_filme:
            # Obter sessões com disponibilidade para DUBLADO
            sessoes_dublado = obter_sessoes_com_disponibilidade(id_filme, "dublado")
            if sessoes_dublado:
                for sessao in sessoes_dublado:
                    hora_fmt = str(sessao.get('Hora_Sessao', ''))[:5]
                    btn = criar_botao_horario(frame_horarios_dublado, hora_fmt, "dublado", [sessao])
                    botoes_horarios_dublado.append(btn)
            else:
                ctk.CTkLabel(frame_horarios_dublado, text="Nenhum horário disponível", 
                           font=("Arial", 12), text_color="gray").pack(side="left")
            
            # Obter sessões com disponibilidade para LEGENDADO
            sessoes_legendado = obter_sessoes_com_disponibilidade(id_filme, "legendado")
            if sessoes_legendado:
                for sessao in sessoes_legendado:
                    hora_fmt = str(sessao.get('Hora_Sessao', ''))[:5]
                    btn = criar_botao_horario(frame_horarios_legendado, hora_fmt, "legendado", [sessao])
                    botoes_horarios_legendado.append(btn)
            else:
                ctk.CTkLabel(frame_horarios_legendado, text="Nenhum horário disponível", 
                           font=("Arial", 12), text_color="gray").pack(side="left")

    def destacar_filme_selecionado(filme_atual):
        """Destaca visualmente o filme selecionado"""
        for item_frame, filme_info in botoes_filmes:
            if filme_info["ID_Filme"] == filme_atual["ID_Filme"]:
                item_frame.configure(fg_color=FILME_SELECIONADO_COLOR)
            else:
                item_frame.configure(fg_color=FILME_NORMAL_COLOR)

    def mostrar_filme(filme):
        """Exibe os detalhes do filme selecionado"""
        filme_selecionado[0] = filme
        destacar_filme_selecionado(filme)
        
        # Atualizar informações
        titulo_var.set(filme.get("titulo", ""))
        sinopse_var.set(filme.get("sinopse", ""))
        direcao_var.set(filme.get("direcao", ""))
        duracao_var.set(filme.get("duracao", ""))
        genero_var.set(filme.get("genero", ""))

        # Carregar imagem
        caminho = filme.get("cartaz_path", "")
        img = None
        if caminho and os.path.isfile(caminho):
            try:
                img = Image.open(caminho)
            except Exception as e:
                print(f"Erro ao carregar imagem {caminho}: {e}")
        
        if img is None:
            img = Image.new("RGB", (200, 300), (40, 40, 40))
        
        img = img.resize((200, 300), Image.LANCZOS)
        foto = ctk.CTkImage(img, size=(200, 300))
        label_imagem.configure(image=foto, text="")
        label_imagem.image = foto

        # Carregar classificação
        classificacao_path = filme.get("classificacao", "")
        if classificacao_path and os.path.isfile(classificacao_path):
            try:
                img_c = Image.open(classificacao_path)
                img_c = img_c.resize((50, 50), Image.LANCZOS)
                foto_c = ctk.CTkImage(img_c, size=(50, 50))
                label_classificacao.configure(image=foto_c, text="")
                label_classificacao.image = foto_c
            except Exception as e:
                label_classificacao.configure(image=None, text="N/A")
        else:
            label_classificacao.configure(image=None, text="N/A")

        # Carregar sessões
        id_filme = filme.get("ID_Filme")
        if id_filme:
            sessoes = carregar_sessoes_do_banco(id_filme)
            filme["sessoes"] = sessoes

        # Atualizar interface
        if dia_selecionado.get():
            atualizar_horarios_por_tipo()
            horario_selecionado.set("")
            tipo_selecionado.set("")
        else:
            for widget in frame_horarios_dublado.winfo_children():
                widget.destroy()
            for widget in frame_horarios_legendado.winfo_children():
                widget.destroy()
            botoes_horarios_dublado.clear()
            botoes_horarios_legendado.clear()
            horario_selecionado.set("")
            tipo_selecionado.set("")

        atualizar_selecao()

    def atualizar_selecao():
        dia = dia_selecionado.get()
        tipo = tipo_selecionado.get()
        horario = horario_selecionado.get()
        
        if dia and tipo and horario and filme_selecionado[0]:
            if isinstance(dia, dict):
                selecao_texto = f"Sessão: {dia['nome']} ({dia['label']}) - {horario} - {tipo.capitalize()}"
            else:
                selecao_texto = f"Sessão: {horario} - {tipo.capitalize()}"
            label_selecao.configure(text=selecao_texto)
            # Habilitar botão quando tudo estiver selecionado
            btn_confirmar.configure(state="normal", fg_color=BTN_COLOR, hover_color="#E2952D")
        else:
            label_selecao.configure(text="Selecione filme, dia, horário e tipo")
            # Desabilitar botão quando seleção estiver incompleta
            btn_confirmar.configure(state="disabled", fg_color="gray")

    def criar_botoes_filmes():
        """Cria os botões para cada filme na lista horizontal"""
        for filme in filmes:
            # Frame para cada filme
            item_frame = ctk.CTkFrame(scrollable_frame, fg_color=FILME_NORMAL_COLOR, 
                                    height=380, width=200, corner_radius=8)
            item_frame.pack(side="left", pady=10, padx=8)
            item_frame.pack_propagate(False)
            
            botoes_filmes.append((item_frame, filme))
            
            # Carregar imagem
            caminho_imagem = filme.get("cartaz_path", "")
            if caminho_imagem and os.path.isfile(caminho_imagem):
                try:
                    img = Image.open(caminho_imagem)
                    img = img.resize((160, 200), Image.LANCZOS)
                    foto = ctk.CTkImage(img, size=(160, 200))
                except Exception as e:
                    img = Image.new("RGB", (160, 200), (40, 40, 40))
                    foto = ctk.CTkImage(img, size=(160, 200))
            else:
                img = Image.new("RGB", (160, 200), (40, 40, 40))
                foto = ctk.CTkImage(img, size=(160, 200))

            # Conteúdo do frame
            content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=5, pady=5)

            # Botão com imagem
            btn_imagem = ctk.CTkButton(
                content_frame,
                image=foto, text="",
                fg_color="transparent", hover_color=BTN_HOVER,
                command=lambda f=filme: mostrar_filme(f),
                height=200, width=160
            )
            btn_imagem.pack(pady=(5, 5))

            # Título
            label_titulo = ctk.CTkLabel(
                content_frame,
                text=filme["titulo"].title(),
                anchor="center", text_color=BTN_TEXT,
                font=fonte_global if fonte_global else ("Arial", 12, "bold"), height=60, wraplength=180
            )
            label_titulo.pack(fill="x", expand=False)

    def atualizar_catalogo():
        """Recarrega os filmes do banco"""
        nonlocal filmes
        filmes = carregar_filmes_do_banco()
        
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        botoes_filmes.clear()
        criar_botoes_filmes()
        
        if filme_selecionado[0]:
            filme_atual = next((f for f in filmes if f["ID_Filme"] == filme_selecionado[0].get("ID_Filme")), None)
            if filme_atual:
                mostrar_filme(filme_atual)
            elif filmes:
                mostrar_filme(filmes[0])
        elif filmes:
            mostrar_filme(filmes[0])

    def on_confirmar():
        dia = dia_selecionado.get()
        tipo = tipo_selecionado.get()
        horario = horario_selecionado.get()
        
        if filme_selecionado[0] and dia and tipo and horario:
            filme_completo = filme_selecionado[0].copy()
            filme_completo["dia_selecionado"] = dia
            filme_completo["tipo_selecionado"] = tipo
            filme_completo["horario_selecionado"] = horario
            
            # Adicionar ID da sessão específica para melhor rastreamento
            id_filme = filme_completo.get("ID_Filme")
            sessoes = obter_sessoes_com_disponibilidade(id_filme, tipo)
            
            for sessao in sessoes:
                hora_fmt = str(sessao.get('Hora_Sessao', ''))[:5]
                if hora_fmt == horario:
                    filme_completo["ID_Sessao"] = sessao.get("ID_Sessao")
                    filme_completo["assentos_disponiveis"] = sessao.get("assentos_livres", 0)
                    filme_completo["total_assentos"] = sessao.get("total_assentos", 0)
                    filme_completo["taxa_ocupacao"] = sessao.get("taxa_ocupacao", 0)
                    break
            
            confirmar_callback(filme_completo)
        else:
            messagebox.showwarning("Seleção Incompleta", "Selecione um filme, dia, horário e tipo")

    # ================== INICIALIZAÇÃO ==================
    
    # Vincular variáveis
    dia_selecionado.trace("w", lambda *args: atualizar_selecao())
    tipo_selecionado.trace("w", lambda *args: atualizar_selecao())
    horario_selecionado.trace("w", lambda *args: atualizar_selecao())

    # Criar botões de dias
    dias = gerar_proximos_dias()
    for dia_info in dias:
        btn = criar_botao_dia(frame_dias_container, dia_info)
        botoes_dias.append(btn)

    # Carregar e exibir filmes
    filmes = carregar_filmes_do_banco()
    criar_botoes_filmes()

    # Botões de navegação
    btn_voltar = ctk.CTkButton(botoes_frame, text="Voltar", 
                              fg_color=BTN_COLOR, font=fonte_global if fonte_global else ("Arial", 14, "bold"),
                              hover_color=BTN_HOVER, text_color=BTN_TEXT,
                              height=40, width=150, command=voltar_callback)
    btn_voltar.pack(side="left", padx=10)

    btn_confirmar = ctk.CTkButton(botoes_frame, text="Selecionar Assentos", 
                                 fg_color="gray", font=fonte_global if fonte_global else ("Arial", 14, "bold"),
                                 hover_color="gray", text_color=BTN_TEXT,
                                 height=40, width=150, command=on_confirmar, state="disabled")
    btn_confirmar.pack(side="left", padx=20)

    # Selecionar primeiro filme
    if filmes:
        mostrar_filme(filmes[0])

    # Expor função de atualização
    frame.atualizar_catalogo = atualizar_catalogo

    return frame