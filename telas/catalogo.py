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
                # Campos que podem não existir no banco (mantidos para compatibilidade)
                "descricao": f"Assista {filme['Titulo_Filme']} nos melhores cinemas.",
                "teste": f"Duração: {filme['Duracao']} minutos",
                "direçao": "Vários diretores"
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
    """Cria e retorna o frame do catálogo de filmes com seleção de horário"""
    
    # Frame principal com tamanho fixo
    frame = ctk.CTkFrame(parent, fg_color="transparent", width=1800, height=900)
    frame.pack_propagate(False)  # Impede redimensionamento automático
    
    # cache de imagens para evitar garbage collection
    frame.image_cache = {}

    # ----- frame esquerdo: lista (scrollable) -----
    frame_esq = ctk.CTkFrame(frame, width=240, height=600)
    frame_esq.pack(side="left", fill="y", padx=(12,6), pady=12)
    frame_esq.pack_propagate(False)

    ctk.CTkLabel(frame_esq, text="Filmes em Cartaz", font=("Arial", 16, "bold")).pack(pady=(8,6))

    scroll = ctk.CTkScrollableFrame(frame_esq, width=100, height=580)
    scroll.pack(fill="both", expand=True, padx=8, pady=8)
    
    # Variáveis para os dados do filme
    titulo_var = ctk.StringVar(value="Selecione um filme")
    descricao_var = ctk.StringVar(value="Descrição do filme aparecerá aqui.")
    lancamento_var = ctk.StringVar(value="Lançamento do filme aparecerá aqui.")
    genero_var = ctk.StringVar(value="Gênero do filme aparecerá aqui.")
    duracao_var = ctk.StringVar(value="Duração do filme aparecerá aqui.")
    classificacao_var = ctk.StringVar(value="")

    # ----- frame direito: detalhes -----
    frame_dir = ctk.CTkFrame(frame, width=1800, height=700)
    frame_dir.pack(side="right", fill="both", padx=(6,12), pady=12)
    frame_dir.pack_propagate(False)

    # Frame superior com imagem e textos - ALTURA REDUZIDA
    frame_top = ctk.CTkFrame(frame_dir, height=450)
    frame_top.pack(fill="x", padx=12, pady=(10,0))
    frame_top.pack_propagate(False)

    # Frame para a imagem do filme (container com tamanho adequado)
    frame_imagem = ctk.CTkFrame(frame_top, width=300, height=450)
    frame_imagem.pack(side="left", padx=12, pady=12)
    frame_imagem.pack_propagate(False)

    # Imagem do filme - agora dentro do frame_imagem
    label_imagem = ctk.CTkLabel(frame_imagem, text="")
    label_imagem.pack(expand=True, fill="both", padx=5, pady=5)

    # Frame de textos
    frame_textos = ctk.CTkFrame(frame_top, fg_color="transparent")
    frame_textos.pack(side="left", fill="both", expand=True, padx=12)

    label_titulo = ctk.CTkLabel(frame_textos, textvariable=titulo_var, font=("Arial", 18, "bold"))
    label_titulo.pack(anchor="nw", pady=(0,6))

    label_descricao = ctk.CTkLabel(frame_textos, textvariable=descricao_var, wraplength=1200, justify="left")
    label_descricao.pack(anchor="nw", pady=(0,6))

    label_lancamento2 = ctk.CTkLabel(frame_textos, text="Duração", font=("Arial", 14, "bold"))
    label_lancamento2.pack(anchor="nw")
    label_lancamento = ctk.CTkLabel(frame_textos, textvariable=duracao_var, wraplength=400, justify="left")
    label_lancamento.pack(anchor="nw", pady=(0,6))

    label_genero2 = ctk.CTkLabel(frame_textos, text="Gênero", font=("Arial", 14, "bold"))
    label_genero2.pack(anchor="nw")
    label_genero = ctk.CTkLabel(frame_textos, textvariable=genero_var, wraplength=400, justify="left")
    label_genero.pack(anchor="nw", pady=(0,6))

    # Frame para classificação
    frame_classificacao = ctk.CTkFrame(frame_textos, fg_color="transparent")
    frame_classificacao.pack(anchor="nw", pady=(0,6))
    
    ctk.CTkLabel(frame_classificacao, text="Classificação:", font=("Arial", 14, "bold")).pack(side="left")
    label_classificacao = ctk.CTkLabel(frame_classificacao, text="", width=50, height=50)
    label_classificacao.pack(side="left", padx=10)

    # Frame para sessões com seleção de horário
    frame_sessoes = ctk.CTkFrame(frame_dir, height=350)
    frame_sessoes.pack(fill="x", padx=12, pady=(10,0))
    frame_sessoes.pack_propagate(False)

    # Botões de navegação
    botoes_frame = ctk.CTkFrame(frame_dir, height=50)
    botoes_frame.pack(side="bottom", fill="x", padx=20, pady=10)
    botoes_frame.pack_propagate(False)

    # Variáveis para armazenar seleções
    dia_selecionado = ctk.StringVar(value="")
    tipo_selecionado = ctk.StringVar(value="")
    horario_selecionado = ctk.StringVar(value="")

    # Função para gerar os próximos 3 dias
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
        btn = ctk.CTkButton(parent, text=f"{dia_info['nome']}\n{dia_info['label']}", 
                           width=80, height=30, corner_radius=10,
                           fg_color=BTN_COLOR,
                           hover_color=BTN_HOVER,
                           text_color=BTN_TEXT,
                           command=lambda: selecionar_dia(dia_info))
        btn.pack(side="left", padx=5, pady=5)
        return btn

    def criar_botao_tipo(parent, tipo, label):
        btn = ctk.CTkButton(parent, text=label, width=80, height=30, corner_radius=10,
                           fg_color=BTN_COLOR,
                           hover_color=BTN_HOVER,
                           text_color=BTN_TEXT,
                           command=lambda: selecionar_tipo(tipo))
        btn.pack(side="left", padx=5, pady=5)
        return btn

    def criar_botao_horario(parent, horario):
        btn = ctk.CTkButton(parent, text=horario, width=80, height=30, corner_radius=8,
                           fg_color=BTN_COLOR,
                           hover_color=BTN_HOVER,
                           text_color=BTN_TEXT,
                           command=lambda: selecionar_horario(horario))
        btn.pack(side="left", padx=3, pady=3)
        return btn

    def selecionar_dia(dia_info):
        dia_selecionado.set(dia_info)
        # Atualizar visual dos botões de dia
        for btn in botoes_dias:
            if btn.cget("text").split('\n')[1] == dia_info['label']:
                btn.configure(fg_color="#1f6aa5")
            else:
                btn.configure(fg_color=BTN_COLOR)
        
        # Resetar seleções de tipo e horário
        tipo_selecionado.set("")
        horario_selecionado.set("")
        atualizar_botoes_tipo()
        atualizar_botoes_horario()

    def selecionar_tipo(tipo):
        if not dia_selecionado.get():
            return
        
        tipo_selecionado.set(tipo)
        # Atualizar visual dos botões de tipo
        for btn_tipo in botoes_tipos:
            if btn_tipo.cget("text").lower() == tipo:
                btn_tipo.configure(fg_color="#1f6aa5")
            else:
                btn_tipo.configure(fg_color=BTN_COLOR)
        
        # Resetar seleção de horário
        horario_selecionado.set("")
        atualizar_botoes_horario()

    def selecionar_horario(horario):
        if not dia_selecionado.get() or not tipo_selecionado.get():
            return
        
        horario_selecionado.set(horario)
        # Atualizar visual dos botões de horário
        for btn_horario in botoes_horarios:
            if btn_horario.cget("text") == horario:
                btn_horario.configure(fg_color="#1f6aa5")
            else:
                btn_horario.configure(fg_color=BTN_COLOR)

    def atualizar_botoes_tipo():
        # Limpar botões de tipo existentes
        for widget in frame_tipos_container.winfo_children():
            widget.destroy()
        
        botoes_tipos.clear()
        
        if not dia_selecionado.get():
            return
        
        # Criar botões para cada tipo disponível
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
        # Limpar botões de horário existentes
        for widget in frame_horarios_container.winfo_children():
            widget.destroy()
        
        botoes_horarios.clear()
        
        if not dia_selecionado.get() or not tipo_selecionado.get():
            return
        
        # Criar botões para cada horário disponível
        filme = filme_selecionado[0]
        if filme and "sessoes" in filme:
            horarios = filme["sessoes"].get(tipo_selecionado.get(), [])
            
            for horario in horarios:
                btn = criar_botao_horario(frame_horarios_container, horario)
                botoes_horarios.append(btn)

    def mostrar_sessoes(filme):
        # Limpar frame de sessões
        for widget in frame_sessoes.winfo_children():
            widget.destroy()
        
        # Resetar seleções
        dia_selecionado.set("")
        tipo_selecionado.set("")
        horario_selecionado.set("")
        
        # Título das sessões
        ctk.CTkLabel(frame_sessoes, text="Selecione a Sessão:", 
                     font=("Arial", 16, "bold")).pack(anchor="w", pady=(10,5))
        
        # Frame para dias
        frame_dias = ctk.CTkFrame(frame_sessoes, fg_color="transparent")
        frame_dias.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(frame_dias, text="Dia:", font=("Arial", 14, "bold")).pack(anchor="w")
        
        # Container para botões de dias
        frame_dias_container = ctk.CTkFrame(frame_dias, fg_color="transparent")
        frame_dias_container.pack(fill="x", pady=5)
        
        # Criar botões para os próximos 3 dias
        dias = gerar_proximos_dias()
        botoes_dias.clear()
        for dia_info in dias:
            btn = criar_botao_dia(frame_dias_container, dia_info)
            botoes_dias.append(btn)
        
        # Frame para tipos (dublado/legendado)
        frame_tipos = ctk.CTkFrame(frame_sessoes, fg_color="transparent")
        frame_tipos.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(frame_tipos, text="Tipo:", font=("Arial", 14, "bold")).pack(anchor="w")
        
        # Container para botões de tipo
        global frame_tipos_container
        frame_tipos_container = ctk.CTkFrame(frame_tipos, fg_color="transparent")
        frame_tipos_container.pack(fill="x", pady=5)
        
        # Frame para horários
        frame_horarios = ctk.CTkFrame(frame_sessoes, fg_color="transparent")
        frame_horarios.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(frame_horarios, text="Horário:", font=("Arial", 14, "bold")).pack(anchor="w")
        
        # Container para botões de horário
        global frame_horarios_container
        frame_horarios_container = ctk.CTkFrame(frame_horarios, fg_color="transparent")
        frame_horarios_container.pack(fill="x", pady=5)
        
        # Label para mostrar seleção atual
        label_selecao = ctk.CTkLabel(frame_sessoes, text="", font=("Arial", 14, "bold"))
        label_selecao.pack(anchor="w", pady=10)
        
        # NO ARQUIVO catalogo.py - FUNÇÃO atualizar_selecao
        def atualizar_selecao(*args):
            dia = dia_selecionado.get()
            tipo = tipo_selecionado.get()
            horario = horario_selecionado.get()
            
            # CORREÇÃO: Verificar se dia é um dicionário antes de acessar
            if dia and tipo and horario:
                if isinstance(dia, dict):
                    selecao_texto = f"Sessão selecionada: {dia['nome']} ({dia['label']}) - {tipo.capitalize()} - {horario}"
                else:
                    # Se for string, tentar extrair informações básicas
                    selecao_texto = f"Sessão selecionada: {tipo.capitalize()} - {horario}"
                label_selecao.configure(text=selecao_texto)
            else:
                label_selecao.configure(text="")
        
        # Vincular as variáveis à atualização do texto
        dia_selecionado.trace("w", atualizar_selecao)
        tipo_selecionado.trace("w", atualizar_selecao)
        horario_selecionado.trace("w", atualizar_selecao)

    # Listas para armazenar referências dos botões
    botoes_dias = []
    botoes_tipos = []
    botoes_horarios = []

    # Variável para armazenar o filme selecionado
    filme_selecionado = [None]

    def mostrar_filme(filme):
        filme_selecionado[0] = filme
        
        titulo_var.set(filme.get("titulo", ""))
        descricao_var.set(filme.get("descricao", ""))
        duracao_var.set(filme.get("duracao", ""))
        genero_var.set(filme.get("genero", ""))
        lancamento_var.set(filme.get("teste", ""))

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
        foto = ctk.CTkImage(img, size=(300, 450))
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
            mostrar_sessoes(filme)

    # Carregar filmes do banco
    filmes = carregar_filmes_do_banco()

    # Cria botões para cada filme
    for filme in filmes:
        # Frame para cada item do filme
        item_frame = ctk.CTkFrame(scroll, fg_color=BTN_COLOR, height=300, width=60, corner_radius=8)
        item_frame.pack(pady=4, padx=6, fill="x")
        item_frame.pack_propagate(False)
        
        # Carrega a imagem do cartaz
        caminho_imagem = filme.get("cartaz_path", "")
        img = None
        
        if caminho_imagem and os.path.isfile(caminho_imagem):
            try:
                img = Image.open(caminho_imagem)
                # Redimensiona para thumbnail pequena
                img = img.resize((180, 210), Image.LANCZOS)
                foto = ctk.CTkImage(img, size=(180, 210))
            except Exception as e:
                print(f"Erro ao carregar imagem {caminho_imagem}: {e}")
                img = None

        # Frame principal que contém imagem e botão
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent", height=500)
        content_frame.pack(fill="both", expand=True, padx=8, pady=2)
        content_frame.pack_propagate(False)

        # BOTÃO com a imagem (no lugar da label)
        btn_imagem = ctk.CTkButton(
            content_frame,
            image=foto,
            text="",  # Texto vazio
            fg_color="transparent",
            hover_color=BTN_HOVER,
            command=lambda f=filme: mostrar_filme(f),
            height=210,
            width=180
        )
        btn_imagem.pack(pady=(10, 10))

        # LABEL com o título (no lugar do botão)
        label_titulo = ctk.CTkLabel(
            content_frame,
            text=filme["titulo"].title(),
            anchor="center",
            text_color=BTN_TEXT,
            font=("Arial", 14, "bold"),
            height=50,
            wraplength=180
        )
        label_titulo.pack(fill="x", expand=False, padx=20)

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

    return frame

# Função de compatibilidade
def mostrar_catalogo_filmes(parent, voltar_callback=None, confirmar_callback=None):
    return criar_tela_catalogo(parent, voltar_callback, confirmar_callback)

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Catálogo de Filmes")
    app.geometry("1000x700")
    
    def voltar():
        print("Voltando...")
    
    def confirmar(filme):
        print(f"Filme selecionado: {filme['titulo']}")
        print(f"Dia: {filme['dia_selecionado']['nome']} ({filme['dia_selecionado']['label']})")
        print(f"Tipo: {filme['tipo_selecionado']}")
        print(f"Horário: {filme['horario_selecionado']}")
    
    frame = criar_tela_catalogo(app, voltar, confirmar)
    frame.pack(fill="both", expand=True)
    
    app.mainloop()