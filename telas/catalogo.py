import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime, timedelta
from crud.crud_filme import listar_filmes
from crud.crud_sessao import listar_sessoes_por_filme

# ================== CONSTANTES DE CORES ==================
BTN_COLOR = "#F6C148"
BTN_HOVER = "#E2952D"
BTN_TEXT = "#1C2732"
FILME_SELECIONADO_COLOR = "#B6D8F1"  # Nova cor para o filme selecionado
FILME_NORMAL_COLOR = "#F6C148"       # Cor normal dos filmes

# ================== CONSTANTES DE CAMINHOS ==================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # sobe uma pasta (pai de 'telas')
IMAGE_DIR = os.path.join(BASE_DIR, "utilidades", "images")

# Caminhos para as classificações indicativas
CLASSIFICACOES = {
    "LIVRE": os.path.join(IMAGE_DIR, "livre.png"),
    "10": os.path.join(IMAGE_DIR, "dez.png"),
    "12": os.path.join(IMAGE_DIR, "doze.png"),
    "14": os.path.join(IMAGE_DIR, "catorze.jpg"),
    "16": os.path.join(IMAGE_DIR, "dezesseis.png"),
    "18": os.path.join(IMAGE_DIR, "dezoito.png"),
}

# Carregar filmes do banco de dados
def carregar_filmes_do_banco():
    try:
        filmes_db = listar_filmes()
        filmes_formatados = []
        
        for filme in filmes_db:
            # Formatar dados do filme
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

# Carregar sessões do banco de dados
def carregar_sessoes_do_banco(id_filme):
    try:
        sessoes_db = listar_sessoes_por_filme(id_filme)
        sessoes_formatadas = {
            "dublado": [],
            "legendado": []
        }
        
        for sessao in sessoes_db:
            # Usar o campo formatado
            hora = sessao.get("Hora_Formatada", "")
            tipo = sessao["Tipo_Sessao"]
            
            if tipo == "dublado" and hora:
                sessoes_formatadas["dublado"].append(hora)
            elif tipo == "legendado" and hora:
                sessoes_formatadas["legendado"].append(hora)
        
        # Ordenar horários
        sessoes_formatadas["dublado"].sort()
        sessoes_formatadas["legendado"].sort()
        
        return sessoes_formatadas
    except Exception as e:
        print(f"Erro ao carregar sessões do banco: {e}")
        return {"dublado": [], "legendado": []}

def criar_tela_catalogo(parent, voltar_callback=None, confirmar_callback=None):
    """Cria e retorna o frame do catálogo de filmes com nova estrutura de layout"""
    
    # Frame principal com tamanho fixo
    frame = ctk.CTkFrame(parent, fg_color="transparent", width=1800, height=900)
    frame.pack_propagate(False)
    
    # cache de imagens para evitar garbage collection
    frame.image_cache = {}

    # Variáveis para armazenar seleções
    dia_selecionado = ctk.StringVar(value="")
    tipo_selecionado = ctk.StringVar(value="")
    horario_selecionado = ctk.StringVar(value="")

    # Variáveis para os dados do filme
    titulo_var = ctk.StringVar(value="Selecione um filme")
    sinopse_var = ctk.StringVar(value="Sinopse do filme aparecerá aqui.")
    direcao_var = ctk.StringVar(value="Direção do filme aparecerá aqui.")
    genero_var = ctk.StringVar(value="Gênero do filme aparecerá aqui.")
    duracao_var = ctk.StringVar(value="Duração do filme aparecerá aqui.")
    classificacao_var = ctk.StringVar(value="")

    # Variável para armazenar o filme selecionado
    filme_selecionado = [None]

    # Listas para armazenar referências dos botões
    botoes_dias = []
    botoes_tipos = []
    botoes_horarios = []
    botoes_filmes = []  # Nova lista para armazenar referências dos frames dos filmes

    # ----- FRAME SUPERIOR: DIAS E TIPOS -----
    frame_superior = ctk.CTkFrame(frame, height=220)
    frame_superior.pack(fill="x", padx=12, pady=(12, 6))
    frame_superior.pack_propagate(False)

    # Frame para dias (centralizado)
    frame_dias = ctk.CTkFrame(frame_superior, fg_color="transparent")
    frame_dias.pack(fill="x", pady=5)
    ctk.CTkLabel(frame_dias, text="Selecione o Dia:", font=("Arial", 14, "bold")).pack(pady=(0, 0))
    
    # Container para botões de dias (centralizado)
    frame_dias_container = ctk.CTkFrame(frame_dias, fg_color="transparent")
    frame_dias_container.pack(anchor="center", pady=0)

    # Frame para tipos (centralizado)
    frame_tipos = ctk.CTkFrame(frame_superior, fg_color="transparent")
    frame_tipos.pack(fill="x", pady=0)
    ctk.CTkLabel(frame_tipos, text="Selecione o Tipo:", font=("Arial", 14, "bold")).pack(pady=(0, 0))
    
    # Container para botões de tipo (centralizado)
    frame_tipos_container = ctk.CTkFrame(frame_tipos, fg_color="transparent")
    frame_tipos_container.pack(anchor="center", pady=5)

    # ----- FRAME MEIO: LISTA DE FILMES (SCROLL HORIZONTAL) -----
    frame_meio = ctk.CTkFrame(frame, height=300)
    frame_meio.pack(fill="x", padx=12, pady=6)
    frame_meio.pack_propagate(False)

    ctk.CTkLabel(frame_meio, text="Filmes em Cartaz", font=("Arial", 16, "bold")).pack(pady=(8, 6))

    # Container para scroll horizontal dos filmes
    scroll_container = ctk.CTkFrame(frame_meio, fg_color="transparent")
    scroll_container.pack(fill="both", expand=True, padx=10, pady=5)

    # Canvas e scrollbar para rolagem horizontal
    canvas = tk.Canvas(scroll_container, height=250, bg='#2b2b2b', highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(scroll_container, orientation="horizontal", command=canvas.xview)
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="transparent")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    canvas.pack(side="top", fill="both", expand=True)
    scrollbar.pack(side="bottom", fill="x")

    # ----- FRAME INFERIOR: DETALHES DO FILME E HORÁRIOS -----
    frame_inferior = ctk.CTkFrame(frame)
    frame_inferior.pack(fill="both", expand=True, padx=12, pady=(6, 12))

    # Frame esquerdo: detalhes do filme
    frame_esquerdo = ctk.CTkFrame(frame_inferior, width=400)
    frame_esquerdo.pack(side="left", fill="both", expand=True, padx=(0, 6), pady=10)
    frame_esquerdo.pack_propagate(False)

    # Frame direito: horários
    frame_direito = ctk.CTkFrame(frame_inferior, width=600)
    frame_direito.pack(side="right", fill="both", padx=(6, 0), pady=10)
    frame_direito.pack_propagate(False)

    # ===== CONTEÚDO DO FRAME ESQUERDO (DETALHES DO FILME) =====
    # Frame superior com imagem e textos
    frame_top = ctk.CTkFrame(frame_esquerdo)
    frame_top.pack(fill="x", padx=12, pady=10)

    # Frame para a imagem do filme
    frame_imagem = ctk.CTkFrame(frame_top, width=200, height=320)
    frame_imagem.pack(side="left", padx=0, pady=0)
    frame_imagem.pack_propagate(False)

    # Imagem do filme
    label_imagem = ctk.CTkLabel(frame_imagem, text="")
    label_imagem.pack(expand=True, fill="both", padx=5, pady=5)

    # Frame de textos
    frame_textos = ctk.CTkFrame(frame_top, fg_color="transparent")
    frame_textos.pack(side="left", fill="both", expand=True, padx=0)

    label_titulo = ctk.CTkLabel(frame_textos, textvariable=titulo_var, font=("Arial", 18, "bold"))
    label_titulo.pack(anchor="nw", pady=(0,6))

    # Frame para informações básicas
    frame_info_basica = ctk.CTkFrame(frame_textos, fg_color="transparent")
    frame_info_basica.pack(anchor="nw", fill="x", pady=(0,6))

    # Direção
    label_direcao_titulo = ctk.CTkLabel(frame_info_basica, text="Direção:", font=("Arial", 14, "bold"))
    label_direcao_titulo.pack(anchor="nw")
    label_direcao = ctk.CTkLabel(frame_info_basica, textvariable=direcao_var, wraplength=400, justify="left")
    label_direcao.pack(anchor="nw", pady=(0,6))

    # Duração
    label_duracao_titulo = ctk.CTkLabel(frame_info_basica, text="Duração:", font=("Arial", 14, "bold"))
    label_duracao_titulo.pack(anchor="nw")
    label_duracao = ctk.CTkLabel(frame_info_basica, textvariable=duracao_var, wraplength=400, justify="left")
    label_duracao.pack(anchor="nw", pady=(0,6))

    # Gênero
    label_genero_titulo = ctk.CTkLabel(frame_info_basica, text="Gênero:", font=("Arial", 14, "bold"))
    label_genero_titulo.pack(anchor="nw")
    label_genero = ctk.CTkLabel(frame_info_basica, textvariable=genero_var, wraplength=400, justify="left")
    label_genero.pack(anchor="nw", pady=(0,6))

    # Sinopse
    label_sinopse_titulo = ctk.CTkLabel(frame_textos, text="Sinopse:", font=("Arial", 14, "bold"))
    label_sinopse_titulo.pack(anchor="nw", pady=(6,0))
    label_sinopse = ctk.CTkLabel(frame_textos, textvariable=sinopse_var, wraplength=850, justify="left")
    label_sinopse.pack(anchor="nw", pady=(0,6))

    # Frame para classificação
    frame_classificacao = ctk.CTkFrame(frame_textos, fg_color="transparent")
    frame_classificacao.pack(anchor="nw", pady=(0,6))
    
    ctk.CTkLabel(frame_classificacao, text="Classificação:", font=("Arial", 14, "bold")).pack(side="left")
    label_classificacao = ctk.CTkLabel(frame_classificacao, text="", width=50, height=50)
    label_classificacao.pack(side="left", padx=10)

    # ===== CONTEÚDO DO FRAME DIREITO (HORÁRIOS) =====
    ctk.CTkLabel(frame_direito, text="Horários Disponíveis", 
                 font=("Arial", 16, "bold")).pack(pady=(10, 5))

    # Container para botões de horário
    frame_horarios_container = ctk.CTkFrame(frame_direito, fg_color="transparent")
    frame_horarios_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Label para mostrar seleção atual
    label_selecao = ctk.CTkLabel(frame_direito, text="", font=("Arial", 12, "bold"))
    label_selecao.pack(anchor="w", pady=10)

    # ----- BOTÕES DE NAVEGAÇÃO -----
    botoes_frame = ctk.CTkFrame(frame, height=50)
    botoes_frame.pack(side="bottom", fill="x", padx=20, pady=10)
    botoes_frame.pack_propagate(False)

    # ================== FUNÇÕES AUXILIARES ==================
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
                           fg_color=BTN_COLOR,
                           hover_color=BTN_HOVER,
                           text_color=BTN_TEXT,
                           font=("Arial", 18),
                           command=lambda: selecionar_dia(dia_info))
        btn.pack(side="left", padx=5, pady=5)
        return btn

    def criar_botao_tipo(parent, tipo, label):
        btn = ctk.CTkButton(parent, text=label, width=200, height=40, corner_radius=10,
                           fg_color=BTN_COLOR,
                           hover_color=BTN_HOVER,
                           text_color=BTN_TEXT,
                           font=("Arial", 18),
                           command=lambda: selecionar_tipo(tipo))
        btn.pack(side="left", padx=5, pady=5)
        return btn

    def criar_botao_horario(parent, horario):
        btn = ctk.CTkButton(parent, text=horario, width=200, height=50, corner_radius=8,
                           fg_color=BTN_COLOR,
                           hover_color=BTN_HOVER,
                           text_color=BTN_TEXT,
                           font=("Arial", 18),
                           command=lambda: selecionar_horario(horario))
        btn.pack(pady=3)
        return btn

    def selecionar_dia(dia_info):
        dia_selecionado.set(dia_info)
        # Atualizar visual dos botões de dia
        for btn in botoes_dias:
            if btn.cget("text").split(':')[1] == dia_info['label']:
                btn.configure(fg_color="#B6D8F1")
            else:
                btn.configure(fg_color=BTN_COLOR)
        
        # Resetar seleções de tipo e horário
        tipo_selecionado.set("")
        horario_selecionado.set("")
        atualizar_botoes_tipo()
        atualizar_botoes_horario()

    def selecionar_tipo(tipo):
        if not dia_selecionado.get():
            messagebox.showwarning("Seleção Incompleta", "Selecione um dia primeiro")
            return
        
        tipo_selecionado.set(tipo)
        # Atualizar visual dos botões de tipo
        for btn_tipo in botoes_tipos:
            if btn_tipo.cget("text").lower() == tipo:
                btn_tipo.configure(fg_color="#B6D8F1")
            else:
                btn_tipo.configure(fg_color=BTN_COLOR)
        
        # Resetar seleção de horário
        horario_selecionado.set("")
        atualizar_botoes_horario()

    def selecionar_horario(horario):
        if not dia_selecionado.get() or not tipo_selecionado.get():
            messagebox.showwarning("Seleção Incompleta", "Selecione um dia e tipo primeiro")
            return
        
        horario_selecionado.set(horario)
        # Atualizar visual dos botões de horário
        for btn_horario in botoes_horarios:
            if btn_horario.cget("text") == horario:
                btn_horario.configure(fg_color="#B6D8F1")
            else:
                btn_horario.configure(fg_color=BTN_COLOR)

    def atualizar_botoes_tipo():
        """Atualiza os botões de tipo baseado no filme selecionado e dia"""
        # Limpar botões de tipo existentes
        for widget in frame_tipos_container.winfo_children():
            widget.destroy()
        
        botoes_tipos.clear()
        
        if not dia_selecionado.get() or not filme_selecionado[0]:
            return
        
        # Criar botões para cada tipo disponível para este filme
        filme = filme_selecionado[0]
        if filme and "sessoes" in filme:
            tipos_disponiveis = []
            if filme["sessoes"].get("dublado"):
                tipos_disponiveis.append(("dublado", "Dublado"))
            if filme["sessoes"].get("legendado"):
                tipos_disponiveis.append(("legendado", "Legendado"))
            
            for tipo, label in tipos_disponiveis:
                btn = criar_botao_tipo(frame_tipos_container, tipo, label)
                botoes_tipos.append(btn)

    def atualizar_botoes_horario():
        """Atualiza os botões de horário baseado no filme, dia e tipo selecionados"""
        # Limpar botões de horário existentes
        for widget in frame_horarios_container.winfo_children():
            widget.destroy()
        
        botoes_horarios.clear()
        
        if not dia_selecionado.get() or not tipo_selecionado.get() or not filme_selecionado[0]:
            return
        
        # Criar botões para cada horário disponível
        filme = filme_selecionado[0]
        if filme and "sessoes" in filme:
            horarios = filme["sessoes"].get(tipo_selecionado.get(), [])
            
            for horario in horarios:
                btn = criar_botao_horario(frame_horarios_container, horario)
                botoes_horarios.append(btn)

    def destacar_filme_selecionado(filme_atual):
        """Destaca visualmente o filme selecionado na lista horizontal"""
        for i, (item_frame, filme_info) in enumerate(botoes_filmes):
            if filme_info["ID_Filme"] == filme_atual["ID_Filme"]:
                # Destacar o filme selecionado
                item_frame.configure(fg_color=FILME_SELECIONADO_COLOR)
            else:
                # Voltar à cor normal para os outros filmes
                item_frame.configure(fg_color=FILME_NORMAL_COLOR)

    def mostrar_filme(filme):
        """Exibe os detalhes do filme selecionado e atualiza as sessões disponíveis"""
        filme_selecionado[0] = filme
        
        # Destacar visualmente o filme selecionado
        destacar_filme_selecionado(filme)
        
        # Atualizar informações do filme
        titulo_var.set(filme.get("titulo", ""))
        sinopse_var.set(filme.get("sinopse", ""))
        direcao_var.set(filme.get("direcao", ""))
        duracao_var.set(filme.get("duracao", ""))
        genero_var.set(filme.get("genero", ""))

        # Carregar imagem do filme
        caminho = filme.get("cartaz_path", "")
        img = None
        if caminho and os.path.isfile(caminho):
            try:
                img = Image.open(caminho)
            except Exception as e:
                print(f"Erro ao carregar imagem {caminho}: {e}")
                img = None
        
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
                print(f"Erro ao carregar classificação {classificacao_path}: {e}")
                label_classificacao.configure(image=None, text="N/A")
        else:
            label_classificacao.configure(image=None, text="N/A")

        # Carregar sessões do banco de dados
        id_filme = filme.get("ID_Filme")
        if id_filme:
            sessoes = carregar_sessoes_do_banco(id_filme)
            filme["sessoes"] = sessoes

        # ATUALIZAÇÃO CRÍTICA: Atualizar tipos e horários quando o filme muda
        if dia_selecionado.get():
            # Se já temos um dia selecionado, atualizar tipos e horários
            atualizar_botoes_tipo()
            if tipo_selecionado.get():
                atualizar_botoes_horario()
        else:
            # Se não há dia selecionado, limpar tipos e horários
            for widget in frame_tipos_container.winfo_children():
                widget.destroy()
            botoes_tipos.clear()
            
            for widget in frame_horarios_container.winfo_children():
                widget.destroy()
            botoes_horarios.clear()
            tipo_selecionado.set("")
            horario_selecionado.set("")

        # Atualizar seleção atual
        atualizar_selecao()

    def atualizar_selecao():
        dia = dia_selecionado.get()
        tipo = tipo_selecionado.get()
        horario = horario_selecionado.get()
        
        if dia and tipo and horario:
            if isinstance(dia, dict):
                selecao_texto = f"Sessão: {dia['nome']} ({dia['label']}) - {tipo.capitalize()} - {horario}"
            else:
                selecao_texto = f"Sessão: {tipo.capitalize()} - {horario}"
            label_selecao.configure(text=selecao_texto)
        else:
            label_selecao.configure(text="Selecione dia, tipo e horário")

    # Vincular as variáveis à atualização do texto
    dia_selecionado.trace("w", lambda *args: atualizar_selecao())
    tipo_selecionado.trace("w", lambda *args: atualizar_selecao())
    horario_selecionado.trace("w", lambda *args: atualizar_selecao())

    # ================== FUNÇÃO DE ATUALIZAÇÃO AUTOMÁTICA ==================
    def atualizar_catalogo():
        """Recarrega os filmes do banco e atualiza a interface automaticamente"""
        nonlocal filmes
        
        # Recarregar filmes do banco
        filmes = carregar_filmes_do_banco()
        
        # Limpar a lista atual
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        # Limpar a lista de referências
        botoes_filmes.clear()
        
        # Recriar os botões dos filmes
        criar_botoes_filmes()
        
        # Se havia um filme selecionado, tentar mantê-lo
        if filme_selecionado[0]:
            filme_atual = next((f for f in filmes if f["ID_Filme"] == filme_selecionado[0].get("ID_Filme")), None)
            if filme_atual:
                mostrar_filme(filme_atual)
            elif filmes:
                mostrar_filme(filmes[0])
        elif filmes:
            mostrar_filme(filmes[0])
    
    def criar_botoes_filmes():
        """Cria os botões para cada filme na lista horizontal"""
        for filme in filmes:
            # Frame para cada item do filme
            item_frame = ctk.CTkFrame(scrollable_frame, fg_color=FILME_NORMAL_COLOR, height=300, width=160, corner_radius=8)
            item_frame.pack(side="left", pady=10, padx=8)
            item_frame.pack_propagate(False)
            
            # Armazenar referência do frame e do filme
            botoes_filmes.append((item_frame, filme))
            
            # Carrega a imagem do cartaz
            caminho_imagem = filme.get("cartaz_path", "")
            foto = None
            
            if caminho_imagem and os.path.isfile(caminho_imagem):
                try:
                    img = Image.open(caminho_imagem)
                    img = img.resize((140, 180), Image.LANCZOS)
                    foto = ctk.CTkImage(img, size=(140, 180))
                except Exception as e:
                    print(f"Erro ao carregar imagem {caminho_imagem}: {e}")
                    # Criar imagem padrão
                    img = Image.new("RGB", (140, 180), (40, 40, 40))
                    foto = ctk.CTkImage(img, size=(140, 180))
            else:
                # Imagem padrão se não houver caminho
                img = Image.new("RGB", (140, 180), (40, 40, 40))
                foto = ctk.CTkImage(img, size=(140, 180))

            # Frame principal que contém imagem e botão
            content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=5, pady=5)

            # BOTÃO com a imagem
            btn_imagem = ctk.CTkButton(
                content_frame,
                image=foto,
                text="",
                fg_color="transparent",
                hover_color=BTN_HOVER,
                command=lambda f=filme: mostrar_filme(f),
                height=180,
                width=140
            )
            btn_imagem.pack(pady=(5, 5))

            # LABEL com o título
            label_titulo = ctk.CTkLabel(
                content_frame,
                text=filme["titulo"].title(),
                anchor="center",
                text_color=BTN_TEXT,
                font=("Arial", 12, "bold"),
                height=30,
                wraplength=140
            )
            label_titulo.pack(fill="x", expand=False)

    # ================== INICIALIZAÇÃO ==================
    # Criar botões de dias
    dias = gerar_proximos_dias()
    for dia_info in dias:
        btn = criar_botao_dia(frame_dias_container, dia_info)
        botoes_dias.append(btn)

    # Carregar filmes do banco e criar botões
    filmes = carregar_filmes_do_banco()
    criar_botoes_filmes()

    # Botões de navegação
    btn_voltar = ctk.CTkButton(botoes_frame, text="Voltar", 
                              fg_color=BTN_COLOR, font=("Arial", 14, "bold"),
                              hover_color=BTN_HOVER,
                              text_color=BTN_TEXT, height=40, width=150,
                              command=voltar_callback)
    btn_voltar.pack(side="left", padx=10)

    def on_confirmar():
        dia = dia_selecionado.get()
        tipo = tipo_selecionado.get()
        horario = horario_selecionado.get()
        
        if filme_selecionado[0] and dia and tipo and horario:
            # Adiciona todas as informações selecionadas ao dicionário do filme
            filme_completo = filme_selecionado[0].copy()
            filme_completo["dia_selecionado"] = dia
            filme_completo["tipo_selecionado"] = tipo
            filme_completo["horario_selecionado"] = horario
            confirmar_callback(filme_completo)
        else:
            messagebox.showwarning("Seleção Incompleta", "Selecione um filme, dia, tipo e horário")

    btn_confirmar = ctk.CTkButton(botoes_frame, text="Selecionar Assentos", 
                                 fg_color=BTN_COLOR, font=("Arial", 14, "bold"),
                                 hover_color=BTN_HOVER,
                                 text_color=BTN_TEXT, height=40, width=150,
                                 command=on_confirmar)
    btn_confirmar.pack(side="left", padx=20)

    # Seleciona o primeiro filme por padrão
    if filmes:
        mostrar_filme(filmes[0])

    # Expor a função de atualização para uso externo
    frame.atualizar_catalogo = atualizar_catalogo

    return frame