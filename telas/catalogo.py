import customtkinter as ctk
from PIL import Image, ImageTk
import os

# ================== DADOS ==================
filmes = [
    {
        "titulo": "O Senhor dos Anéis",
        "descricao": "O Senhor dos Anéis conta a saga do hobbit Frodo Bolseiro em sua missão para destruir o Um Anel, uma joia maligna criada pelo Senhor das Trevas Sauron, antes que ele seja usado para dominar a Terra-média. Acompanhado pela Companhia do Anel, composta por elfos, anões, homens e hobbits, Frodo enfrenta perigos e as forças de Sauron, que se aliam a outros vilões como Saruman. A jornada termina com a destruição do Anel na Montanha da Perdição, vencendo o mal e assegurando a paz na Terra-média. ",
        "teste": "11 de setembro de 2025 | 1h 25min ",
        "genero": "ficcção de aventura, literatura fantástica, alta fantasia.",
        "direçao": "Peter Jackson",
        "classificação": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\doze.png",
        "imagem": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\o senhor dos anéis.jpg",
        "sessoes_dublado": ["14:15", "18:00",  "20:45", "21:15"],
        "sessoes_legendado": ["17:00", "20:45", "21:15"]
    },
    {
        "titulo": "Matrix",
        "descricao": "O jovem programador Thomas Anderson é atormentado por estranhos pesadelos  em que está sempre conectado por cabos a um imenso sistema de computadores do futuro. À medida que o sonho se repete, ele começa a desconfiar da realidade. Thomas conhece os misteriosos Morpheus e Trinity e descobre que é vítima de um sistema inteligente e artificial chamado Matrix, que manipula a mente das pessoas e cria a ilusão de um mundo real enquanto usa os cérebros e corpos dos indivíduos para produzir energia.",
        "teste": "11 de setembro de 2025  | 1h 49min",
        "genero": "ação, Aventura, Ficção científica, Cyberpunk.",
        "direçao": "Lana Wachowski e Lilly Wachowski",
        "classificação": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\catorze.jpg",
        "imagem": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\Matrix.jpg",
        "sessoes_dublado": ["14:45", "17:30",  "19:00", "21:30"],
        "sessoes_legendado": ["16:50", "19:00", "21:30"]
    },
    {
        "titulo": "Interstellar",
        "descricao": "As reservas naturais da Terra estão chegando ao fim e um grupo de astronautas recebe a missão de verificar possíveis planetas para receberem a população mundial, possibilitando a continuação da espécie. Cooper é chamado para liderar o grupo e aceita a missão sabendo que pode nunca mais ver os filhos. Ao lado de Brand, Jenkins e Doyle, ele seguirá em busca de um novo lar.",
        "teste": "4 de setembro de 2025 | 1h 27min",
        "genero": "Ficção científica, Ação, Suspense, Aventura.",
        "direçao": "Christopher Nolan",
        "classificação": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\dez.png",
        "imagem": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\Interstellar.jpg",
        "sessoes_dublado": ["13:00", "16:45", "20:00"],
        "sessoes_legendado": ["17:00", "20:00", "22:30",]
    },
    {
        "titulo": "Jumanji",
        "descricao": "Quatro adolescentes encontram um videogame cuja ação se passa em uma floresta tropical. Empolgados com o jogo, eles escolhem seus avatares para o desafio, mas um evento inesperado faz com que eles sejam transportados para dentro do universo fictício, transformando-os nos personagens da aventura.",
        "teste": "11 de setembro de 2025 | 1h 30min",
        "genero": "Comédia, Infantil, Aventura, Ação.",
        "direçao": "Jake Kasdan e Joe Johnston",
        "classificação": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\livre.png",
        "imagem": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\jumanji.jpg",
        "sessoes_dublado": ["11:30", "15:00", "18:30", "21:30"],
        "sessoes_legendado": ["18:30", "21:30", ]
    },
    {
        "titulo": "Demon Slayer - Castelo Infinito",
        "descricao": "Os Pilares agora enfrentam Muzan e decidem atacá-lo juntos. No entanto, eles são transportados para a Fortaleza Infinita antes que possam desferir um único golpe e, portanto, são separados.",
        "teste": "11 de setembro de 2025 | 2h 36min",
        "genero": "Ação, Aventura, Fantasia Sombria e Artes Marciais.",
        "direçao": "Haruo Sotozaki",
        "classificação": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\dezoito.png",
        "imagem": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\Demon Slayer - castelo infinito.jpg",
        "sessoes_dublado": ["12:00", "16:00", "19:45", "20:45"],
        "sessoes_legendado": ["19:45", "20:45"]
    },
    {
        "titulo": "Homem-Aranha Sem Volta Para Casa",
        "descricao": "Peter Parker tem a sua identidade secreta revelada e pede ajuda ao Doutor Estranho. Quando o feitiço para reverter o evento não sai como esperado, o Homem-Aranha e o seu companheiro dos Vingadores precisam enfrentar inimigos de todo o multiverso.",
        "teste": "18 de setembro de 2025 | 1h 38min",
        "genero": "Filme super-heroi, Ação, Aventura, Comédia, Suspense",
        "direçao": "Jon Watts ",
        "classificação": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\doze.png",
        "imagem": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\Homem-aranha sem volta para casa.jpg",
        "sessoes_dublado": ["13:30", "17:15", "21:00"],
        "sessoes_legendado": ["16:20", "19:00", "22:30",]
    },
    {
        "titulo": "Invocação do Mal",
        "descricao": "Invocação do Mal acompanha os investigadores paranormais Ed e Lorraine Warren, chamados para ajudar uma família aterrorizada por uma presença demoníaca em sua nova casa, nos anos 70. O casal luta para confrontar a entidade maligna que se alimenta do medo e busca controlar os membros da família, especialmente a mãe, em um caso que se torna o mais difícil de suas carreiras, tudo baseado em um caso real. ",
        "teste": "4 de setembro de 2025 | 2h 15min ",
        "genero": "Terror, Sobrenatural, Mistério, Suspense.",
        "direçao": " Michael Chaves",
        "classificação": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\catorze.jpg",
        "imagem": r"C:\Users\\58513786\\Documents\\Visual Studio 2022\\aula10.py\\listadproduto.py\\ctk.py\\tela.py\\Invocação do mal.jpg",
        "sessoes_dublado": ["13:00", "16:00", "22:00", "23:30"],
        "sessoes_legendado": ["17:00", "19:45", "23:30",]
    },
]


def criar_tela_catalogo(parent, voltar_callback=None, confirmar_callback=None):
    """Cria e retorna o frame do catálogo de filmes com seleção de horário"""
    
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    
    # cache de imagens para evitar garbage collection
    frame.image_cache = {}

    # ----- frame esquerdo: lista (scrollable) -----
    frame_esq = ctk.CTkFrame(frame, width=220)
    frame_esq.pack(side="left", fill="y", padx=(12,6), pady=12)

    ctk.CTkLabel(frame_esq, text="Filmes em Cartaz", font=("Arial", 16, "bold")).pack(pady=(8,6))

    scroll = ctk.CTkScrollableFrame(frame_esq, width=200, height=520)
    scroll.pack(fill="both", expand=True, padx=8, pady=8)
    
    # Variáveis para os dados do filme
    titulo_var = ctk.StringVar(value="Selecione um filme")
    descricao_var = ctk.StringVar(value="Descrição do filme aparecerá aqui.")
    lancamento_var = ctk.StringVar(value="lançamento do filme aparecera aqui.")
    genero_var = ctk.StringVar(value="genêro do filme aparecera aqui.")
    direcao_var = ctk.StringVar(value="direção do filme aparecera aqui.")
    classificacao_var = ctk.StringVar(value="")

    # ----- frame direito: detalhes -----
    frame_dir = ctk.CTkFrame(frame)
    frame_dir.pack(side="right", expand=True, fill="both", padx=(6,12), pady=12)

    # Frame superior com imagem e textos
    frame_top = ctk.CTkFrame(frame_dir)
    frame_top.pack(fill="x", padx=12, pady=12)

    # Imagem do filme
    label_imagem = ctk.CTkLabel(frame_top, text="")
    label_imagem.pack(side="left", padx=12, pady=6)

    # Frame de textos
    frame_textos = ctk.CTkFrame(frame_top)
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

    label_classificacao = ctk.CTkLabel(frame_textos, textvariable=classificacao_var, wraplength=200, justify="left")
    label_classificacao.pack(anchor="nw", pady=(0,12))

    # Frame para sessões com seleção de horário
    frame_sessoes = ctk.CTkFrame(frame_dir, height=200)
    frame_sessoes.pack(fill="x", padx=12, pady=(6,12))

    # Variável para armazenar o horário selecionado
    horario_selecionado = ctk.StringVar(value="")

    def criar_linha_sessoes(frame, titulo, sessoes, linha_base):
        if not sessoes:
            return linha_base
        
        ctk.CTkLabel(frame, text=titulo, font=("Arial", 13, "bold")).grid(
            row=linha_base, column=0, sticky="w", pady=(4,4), padx=6
        )
        
        for i, hora in enumerate(sessoes):
            def criar_callback(hora_selecionada):
                def callback():
                    horario_selecionado.set(hora_selecionada)
                    # Destacar o botão selecionado
                    for widget in frame.winfo_children():
                        if isinstance(widget, ctk.CTkButton):
                            if widget.cget("text") == hora_selecionada:
                                widget.configure(fg_color="#1f6aa5")  # Azul mais escuro
                            else:
                                widget.configure(fg_color="#2b2b2b")  # Cinza padrão
                return callback
            
            btn = ctk.CTkButton(frame, text=hora, width=90, height=36, corner_radius=10,
                               command=criar_callback(hora))
            btn.grid(row=linha_base, column=i+1, padx=6, pady=4)
        
        return linha_base + 1

    def mostrar_sessoes(filme):
        for widget in frame_sessoes.winfo_children():
            widget.destroy()
        
        # Título das sessões
        ctk.CTkLabel(frame_sessoes, text="Selecione o Horário:", 
                     font=("Arial", 16, "bold")).pack(anchor="w", pady=(10, 5))
        
        # Sub-frame para os horários
        horarios_frame = ctk.CTkFrame(frame_sessoes, fg_color="transparent")
        horarios_frame.pack(fill="x", padx=10, pady=5)
        
        linha = 0
        if filme.get("sessoes_dublado"):
            linha = criar_linha_sessoes(horarios_frame, "Dublado:", filme.get("sessoes_dublado", []), linha)
        if filme.get("sessoes_legendado"):
            linha = criar_linha_sessoes(horarios_frame, "Legendado:", filme.get("sessoes_legendado", []), linha)
        
        # Label para mostrar horário selecionado
        label_horario_selecionado = ctk.CTkLabel(frame_sessoes, textvariable=horario_selecionado, 
                                                font=("Arial", 14, "bold"))
        label_horario_selecionado.pack(anchor="w", pady=10)

    # Variável para armazenar o filme selecionado
    filme_selecionado = [None]  # Usando lista para referência mutável

    def mostrar_filme(index: int):
        filme = filmes[index]
        filme_selecionado[0] = filme  # Armazena o filme selecionado
        horario_selecionado.set("")  # Reseta o horário selecionado
        
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
            except Exception:
                img = None
        if img is None:
            img = Image.new("RGB", (600, 280), (20, 20, 20))

        img.thumbnail((1000, 480))
        foto = ImageTk.PhotoImage(img)
        label_imagem.configure(image=foto, text="")
        label_imagem.image = foto
        frame.image_cache[f"poster_{index}"] = foto

        # Carregar classificação
        classificacao = filme.get("classificacao") or filme.get("classificação") or ""
        if isinstance(classificacao, str) and os.path.isfile(classificacao):
            try:
                img_c = Image.open(classificacao)
                img_c.thumbnail((70, 70))
                foto_c = ImageTk.PhotoImage(img_c)
                label_classificacao.configure(text="")
                label_classificacao.configure(image=foto_c)
                label_classificacao.image = foto_c
                label_classificacao.configure(textvariable=None)
                frame.image_cache[f"class_{index}"] = foto_c
            except Exception:
                classificacao_var.set(str(classificacao))
                label_classificacao.configure(textvariable=classificacao_var, image=None)
        else:
            classificacao_var.set(str(classificacao))
            label_classificacao.configure(textvariable=classificacao_var, image=None)

        mostrar_sessoes(filme)

    # Cria botões para cada filme
    for idx, filme in enumerate(filmes):
        btn = ctk.CTkButton(scroll, text=filme["titulo"], width=180, height=36, 
                           command=lambda i=idx: mostrar_filme(i))
        btn.pack(pady=4, padx=6, fill="x")

    # Botões de navegação
    botoes_frame = ctk.CTkFrame(frame)
    botoes_frame.pack(side="bottom", fill="x", padx=20, pady=10)

    btn_voltar = ctk.CTkButton(botoes_frame, text="Voltar", command=voltar_callback)
    btn_voltar.pack(side="left", padx=10)

    def on_confirmar():
        if filme_selecionado[0] and horario_selecionado.get():
            confirmar_callback(filme_selecionado[0], horario_selecionado.get())
        else:
            print("Selecione um filme e um horário")

    btn_confirmar = ctk.CTkButton(botoes_frame, text="Selecionar Assentos", 
                                 command=on_confirmar)
    btn_confirmar.pack(side="right", padx=10)

    # Seleciona o primeiro filme por padrão
    if filmes:
        mostrar_filme(0)

    return frame, btn_voltar, btn_confirmar

# Função de compatibilidade
def mostrar_catalogo_filmes(parent, voltar_callback=None, confirmar_callback=None):
    return criar_tela_catalogo(parent, voltar_callback, confirmar_callback)

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Catálogo de Filmes")
    app.geometry("1000x800")
    
    def voltar():
        print("Voltando...")
    
    def confirmar(filme, horario):
        print(f"Filme selecionado: {filme['titulo']} - Horário: {horario}")
    
    frame, btn_voltar, btn_confirmar = criar_tela_catalogo(app, voltar, confirmar)
    frame.pack(fill="both", expand=True)
    
    app.mainloop()