import customtkinter as ctk
from PIL import Image, ImageTk
import os
from datetime import datetime, timedelta

# ================== CONSTANTES DE CAMINHOS ==================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # sobe uma pasta (pai de 'telas')
IMAGE_DIR = os.path.join(BASE_DIR, "utilidades", "images")

# Caminhos para as imagens dos filmes
FILME_IMAGES = {
    "senhor_aneis": os.path.join(IMAGE_DIR, "o senhor dos anéis.jpg"),
    "matrix": os.path.join(IMAGE_DIR, "matrix.jpg"),
    "interstellar": os.path.join(IMAGE_DIR, "Interstellar.jpg"),
    "jumanji": os.path.join(IMAGE_DIR, "jumanji.jpg"),
    "demon_slayer": os.path.join(IMAGE_DIR, "Demon Slayer - castelo infinito.jpg"),
    "homem_aranha": os.path.join(IMAGE_DIR, "Homem-aranha Sem volta para casa.jpg"),
    "invocacao_mal": os.path.join(IMAGE_DIR, "invocação do mal.jpg")
}

# Caminhos para as classificações indicativas
CLASSIFICACOES = {
    "12": os.path.join(IMAGE_DIR, "doze.png"),
    "14": os.path.join(IMAGE_DIR, "catorze.png"),
    "10": os.path.join(IMAGE_DIR, "dez.png"),
    "LIVRE": os.path.join(IMAGE_DIR, "livre.png"),
    "18": os.path.join(IMAGE_DIR, "dezoito.png")
}

# ================== DADOS DOS FILMES ==================
filmes = [
    {
        "titulo": "O Senhor dos Anéis",
        "descricao": "O Senhor dos Anéis conta a saga do hobbit Frodo Bolseiro em sua missão para destruir o Um Anel, uma joia maligna criada pelo Senhor das Trevas Sauron, antes que ele seja usado para dominar a Terra-média. Acompanhado pela Companhia do Anel, composta por elfos, anões, homens e hobbits, Frodo enfrenta perigos e as forças de Sauron, que se aliam a outros vilões como Saruman. A jornada termina com a destruição do Anel na Montanha da Perdição, vencendo o mal e assegurando a paz na Terra-média.",
        "teste": "11 de setembro de 2025 | 1h 25min",
        "genero": "Ficção de aventura, literatura fantástica, alta fantasia.",
        "direçao": "Peter Jackson",
        "classificacao": CLASSIFICACOES["12"],
        "imagem": FILME_IMAGES["senhor_aneis"],
        "sessoes": {
            "dublado": ["14:15", "18:00", "20:45", "21:15"],
            "legendado": ["17:00", "20:45", "21:15"]
        }
    },
    {
        "titulo": "Matrix",
        "descricao": "O jovem programador Thomas Anderson é atormentado por estranhos pesadelos em que está sempre conectado por cabos a um imenso sistema de computadores do futuro. À medida que o sonho se repete, he começa a desconfiar da realidade. Thomas conhece os misteriosos Morpheus e Trinity e descobre que é vítima de um sistema inteligente e artificial chamado Matrix, que manipula a mente das pessoas e cria a ilusão de um mundo real enquanto usa os cérebros e corpos dos indivíduos para produzir energia.",
        "teste": "11 de setembro de 2025 | 1h 49min",
        "genero": "Ação, Aventura, Ficção científica, Cyberpunk.",
        "direçao": "Lana Wachowski e Lilly Wachowski",
        "classificacao": CLASSIFICACOES["14"],
        "imagem": FILME_IMAGES["matrix"],
        "sessoes": {
            "dublado": ["14:45", "17:30", "19:00", "21:30"],
            "legendado": ["16:50", "19:00", "21:30"]
        }
    },
    {
        "titulo": "Interstellar",
        "descricao": "As reservas naturais da Terra estão chegando ao fim e um grupo de astronautas recebe a missão de verificar possíveis planetas para receberem a população mundial, possibilitando a continuação da espécie. Cooper é chamado para liderar o grupo e aceita a missão sabendo que pode nunca mais ver os filhos. Ao lado de Brand, Jenkins e Doyle, ele seguirá em busca de um novo lar.",
        "teste": "4 de setembro de 2025 | 1h 27min",
        "genero": "Ficção científica, Ação, Suspense, Aventura.",
        "direçao": "Christopher Nolan",
        "classificacao": CLASSIFICACOES["10"],
        "imagem": FILME_IMAGES["interstellar"],
        "sessoes": {
            "dublado": ["13:00", "16:45", "20:00"],
            "legendado": ["17:00", "20:00", "22:30"]
        }
    },
    {
        "titulo": "Jumanji",
        "descricao": "Quatro adolescentes encontram um videogame cuja ação se passa em uma floresta tropical. Empolgados com o jogo, eles escolhem seus avatares para o desafio, mas um evento inesperado faz com que eles sejam transportados para dentro do universo fictício, transformando-os nos personagens da aventura.",
        "teste": "11 de setembro de 2025 | 1h 30min",
        "genero": "Comédia, Infantil, Aventura, Ação.",
        "direçao": "Jake Kasdan e Joe Johnston",
        "classificacao": CLASSIFICACOES["LIVRE"],
        "imagem": FILME_IMAGES["jumanji"],
        "sessoes": {
            "dublado": ["11:30", "15:00", "18:30", "21:30"],
            "legendado": ["18:30", "21:30"]
        }
    },
    {
        "titulo": "Demon Slayer - Castelo Infinito",
        "descricao": "Os Pilares agora enfrentam Muzan e decidem atacá-lo juntos. No entanto, eles são transportados para a Fortaleza Infinita antes que possam desferir um único golpe e, portanto, são separados.",
        "teste": "11 de setembro de 2025 | 2h 36min",
        "genero": "Ação, Aventura, Fantasia Sombria e Artes Marciais.",
        "direçao": "Haruo Sotozaki",
        "classificacao": CLASSIFICACOES["18"],
        "imagem": FILME_IMAGES["demon_slayer"],
        "sessoes": {
            "dublado": ["12:00", "16:00", "19:45", "20:45"],
            "legendado": ["19:45", "20:45"]
        }
    },
    {
        "titulo": "Homem-Aranha Sem Volta Para Casa",
        "descricao": "Peter Parker tem a sua identidade secreta revelada e pede ajuda ao Doutor Estranho. Quando o feitiço para reverter o evento não sai como esperado, o Homem-Aranha e o seu companheiro dos Vingadores precisam enfrentar inimigos de todo o multiverso.",
        "teste": "18 de setembro de 2025 | 1h 38min",
        "genero": "Filme super-herói, Ação, Aventura, Comédia, Suspense",
        "direçao": "Jon Watts",
        "classificacao": CLASSIFICACOES["12"],
        "imagem": FILME_IMAGES["homem_aranha"],
        "sessoes": {
            "dublado": ["13:30", "17:15", "21:00"],
            "legendado": ["16:20", "19:00", "22:30"]
        }
    },
    {
        "titulo": "Invocação do Mal",
        "descricao": "Invocação do Mal acompanha os investigadores paranormais Ed e Lorraine Warren, chamados para ajudar uma família aterrorizada por uma presença demoníaca em sua nova casa, nos anos 70. O casal luta para confrontar a entidade maligna que se alimenta do medo e busca controlar os membros da família, especialmente a mãe, em um caso que se torna o mais difícil de suas carreiras, tudo baseado em um caso real.",
        "teste": "4 de setembro de 2025 | 2h 15min",
        "genero": "Terror, Sobrenatural, Mistério, Suspense.",
        "direçao": "Michael Chaves",
        "classificacao": CLASSIFICACOES["14"],
        "imagem": FILME_IMAGES["invocacao_mal"],
        "sessoes": {
            "dublado": ["13:00", "16:00", "22:00", "23:30"],
            "legendado": ["17:00", "19:45", "23:30"]
        }
    },
]

def criar_tela_catalogo(parent, voltar_callback=None, confirmar_callback=None):
    """Cria e retorna o frame do catálogo de filmes com seleção de horário"""
    
    # Frame principal com tamanho fixo
    frame = ctk.CTkFrame(parent, fg_color="transparent", width=1000, height=900)
    frame.pack_propagate(False)  # Impede redimensionamento automático
    
    # cache de imagens para evitar garbage collection
    frame.image_cache = {}

    # ----- frame esquerdo: lista (scrollable) -----
    frame_esq = ctk.CTkFrame(frame, width=220, height=650)
    frame_esq.pack(side="left", fill="y", padx=(12,6), pady=12)
    frame_esq.pack_propagate(False)

    ctk.CTkLabel(frame_esq, text="Filmes em Cartaz", font=("Arial", 16, "bold")).pack(pady=(8,6))

    scroll = ctk.CTkScrollableFrame(frame_esq, width=200, height=580)
    scroll.pack(fill="both", expand=True, padx=8, pady=8)
    
    # Variáveis para os dados do filme
    titulo_var = ctk.StringVar(value="Selecione um filme")
    descricao_var = ctk.StringVar(value="Descrição do filme aparecerá aqui.")
    lancamento_var = ctk.StringVar(value="Lançamento do filme aparecerá aqui.")
    genero_var = ctk.StringVar(value="Gênero do filme aparecerá aqui.")
    direcao_var = ctk.StringVar(value="Direção do filme aparecerá aqui.")
    classificacao_var = ctk.StringVar(value="")

    # ----- frame direito: detalhes -----
    frame_dir = ctk.CTkFrame(frame, width=750, height=700)
    frame_dir.pack(side="right", fill="both", padx=(6,12), pady=12)
    frame_dir.pack_propagate(False)

    # Frame superior com imagem e textos
    frame_top = ctk.CTkFrame(frame_dir, height=320)
    frame_top.pack(fill="x", padx=12, pady=12)
    frame_top.pack_propagate(False)

    # Imagem do filme
    label_imagem = ctk.CTkLabel(frame_top, text="", width=200, height=300)
    label_imagem.pack(side="left", padx=12, pady=6)

    # Frame de textos
    frame_textos = ctk.CTkFrame(frame_top, fg_color="transparent")
    frame_textos.pack(side="left", fill="both", expand=True, padx=12)

    label_titulo = ctk.CTkLabel(frame_textos, textvariable=titulo_var, font=("Arial", 18, "bold"))
    label_titulo.pack(anchor="nw", pady=(0,6))

    label_descricao = ctk.CTkLabel(frame_textos, textvariable=descricao_var, wraplength=400, justify="left")
    label_descricao.pack(anchor="nw", pady=(0,12))

    label_lancamento2 = ctk.CTkLabel(frame_textos, text="Data de lançamento", font=("Arial", 14, "bold"))
    label_lancamento2.pack(anchor="nw")
    label_lancamento = ctk.CTkLabel(frame_textos, textvariable=lancamento_var, wraplength=400, justify="left")
    label_lancamento.pack(anchor="nw", pady=(0,12))

    label_genero2 = ctk.CTkLabel(frame_textos, text="Gênero", font=("Arial", 14, "bold"))
    label_genero2.pack(anchor="nw")
    label_genero = ctk.CTkLabel(frame_textos, textvariable=genero_var, wraplength=400, justify="left")
    label_genero.pack(anchor="nw", pady=(0,12))

    label_direcao2 = ctk.CTkLabel(frame_textos, text="Direção", font=("Arial", 14, "bold"))
    label_direcao2.pack(anchor="nw")
    label_direcao = ctk.CTkLabel(frame_textos, textvariable=direcao_var, wraplength=400, justify="left")
    label_direcao.pack(anchor="nw", pady=(0,12))

    # Frame para classificação
    frame_classificacao = ctk.CTkFrame(frame_textos, fg_color="transparent")
    frame_classificacao.pack(anchor="nw", pady=(0,12))
    
    ctk.CTkLabel(frame_classificacao, text="Classificação:", font=("Arial", 14, "bold")).pack(side="left")
    label_classificacao = ctk.CTkLabel(frame_classificacao, text="", width=50, height=50)
    label_classificacao.pack(side="left", padx=10)

    # Frame para sessões com seleção de horário
    frame_sessoes = ctk.CTkFrame(frame_dir, height=450, width=700)
    frame_sessoes.pack(fill="x", padx=12, pady=(6,12))
    frame_sessoes.pack_propagate(False)

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
                           width=100, height=60, corner_radius=10,
                           command=lambda: selecionar_dia(dia_info))
        btn.pack(side="left", padx=5, pady=5)
        return btn

    def criar_botao_tipo(parent, tipo, label):
        btn = ctk.CTkButton(parent, text=label, width=100, height=40, corner_radius=10,
                           command=lambda: selecionar_tipo(tipo))
        btn.pack(side="left", padx=5, pady=5)
        return btn

    def criar_botao_horario(parent, horario):
        btn = ctk.CTkButton(parent, text=horario, width=80, height=35, corner_radius=8,
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
                btn.configure(fg_color="#2b2b2b")
        
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
                btn_tipo.configure(fg_color="#2b2b2b")
        
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
                btn_horario.configure(fg_color="#2b2b2b")

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
                     font=("Arial", 16, "bold")).pack(anchor="w", pady=(10, 5))
        
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
        
        def atualizar_selecao(*args):
            dia = dia_selecionado.get()
            tipo = tipo_selecionado.get()
            horario = horario_selecionado.get()
            
            if dia and tipo and horario:
                selecao_texto = f"Sessão selecionada: {dia['nome']} ({dia['label']}) - {tipo.capitalize()} - {horario}"
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

    def mostrar_filme(index: int):
        filme = filmes[index]
        filme_selecionado[0] = filme
        
        titulo_var.set(filme.get("titulo", ""))
        descricao_var.set(filme.get("descricao", ""))
        lancamento_var.set(filme.get("teste", ""))
        genero_var.set(filme.get("genero", ""))
        direcao_var.set(filme.get("direçao", ""))

        # Carregar imagem do filme
        caminho = filme.get("imagem", "")
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

        mostrar_sessoes(filme)

    # Cria botões para cada filme
    for idx, filme in enumerate(filmes):
        btn = ctk.CTkButton(scroll, text=filme["titulo"], width=180, height=36, 
                           command=lambda i=idx: mostrar_filme(i))
        btn.pack(pady=4, padx=6, fill="x")

    # Botões de navegação
    botoes_frame = ctk.CTkFrame(frame_dir)
    botoes_frame.pack(side="bottom", fill="x", padx=20, pady=10)

    btn_voltar = ctk.CTkButton(botoes_frame, text="Voltar", command=voltar_callback)
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
            print("Selecione um filme, dia, tipo e horário")

    btn_confirmar = ctk.CTkButton(botoes_frame, text="Selecionar Assentos", 
                                 command=on_confirmar)
    btn_confirmar.pack(side="left", padx=20)

    # Seleciona o primeiro filme por padrão
    if filmes:
        mostrar_filme(0)

    return frame

# Função de compatibilidade
def mostrar_catalogo_filmes(parent, voltar_callback=None, confirmar_callback=None):
    return criar_tela_catalogo(parent, voltar_callback, confirmar_callback)

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Catálogo de Filmes")
    app.geometry("1000x700")  # Tamanho fixo da janela
    
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