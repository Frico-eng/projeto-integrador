import customtkinter as ctk
from PIL import Image, ImageTk
import os

def mostrar_catalogo_filmes(parent):
    # ================== DADOS ==================
    filmes = [
    {
    "titulo": "O Senhor dos Anéis",
    "descricao": "O Senhor dos Anéis conta a saga do hobbit Frodo Bolseiro em sua missão para destruir o Um Anel, uma joia maligna criada pelo Senhor das Trevas Sauron, antes que ele seja usado para dominar a Terra-média. Acompanhado pela Companhia do Anel, composta por elfos, anões, homens e hobbits, Frodo enfrenta perigos e asforças de Sauron, que se aliam a outros vilões como Saruman. A jornada termina com a destruição do Anel na Montanha da Perdição, vencendo o mal e assegurando a paz na Terra-média. ",
    "imagem": r"C:\\Users\\59699816\\OneDrive - SENAC PA - EDU\\projeto\\senhor.jpg"
    },
    {
    "titulo": "Matrix",
    "descricao": "O jovem programador Thomas Anderson é atormentado por estranhos pesadelos em que está sempre conectado por cabos a um imenso sistema de computadores do futuro. À medida que o sonho se repete, ele começa a desconfiar da realidade. Thomas conhece os misteriosos Morpheus e Trinity e descobre que é vítima de um sistema inteligente e artificial chamado Matrix, que manipula a mente das pessoas e cria a ilusão de um mundo real enquanto usa os cérebros e corpos dos indivíduos para produzir energia.",
    "imagem": r"C:\\Users\\59699816\\OneDrive - SENAC PA - EDU\projeto\matrix.jpg"
    },
    {
    "titulo": "Interstellar",
    "descricao": "As reservas naturais da Terra estão chegando ao fim e um grupo de astronautas recebe a missão de verificar possíveis planetas para receberem a população mundial, possibilitando a continuação da espécie. Cooper é chamado para liderar o grupo e aceita a missão sabendo que pode nunca mais ver os filhos. Ao lado de Brand, Jenkins e Doyle, ele seguirá em busca de um novo lar.",
    "imagem": r"C:\\Users\\59699816\\OneDrive - SENAC PA - EDU\\projeto\\interstellar.jpg"
    },
    {
    "titulo": "Jumanji",
    "descricao": "Quatro adolescentes encontram um videogame cuja ação se passa em uma floresta tropical. Empolgados com o jogo, eles escolhem seus avatares para o desafio, mas um evento inesperado faz com que eles sejam transportados para dentro do universo fictício, transformando-os nos personagens da aventura. ",
    "imagem": r"C:\\Users\\59699816\\OneDrive - SENAC PA - EDU\\projeto\\jumanji.jpg"
    },
    {
    "titulo": "Demon Slayer - Castelo Infinito",
    "descricao": "Os Pilares agora enfrentam Muzan e decidem atacá-lo juntos. Namun, eles são transportados para a Fortaleza Infinita antes que possam desferir um único golpe e, portanto, são separados.",
    "imagem": r"C:\\Users\\59699816\\OneDrive - SENAC PA - EDU\\projeto\\demon.jpg"
    },
    {
    "titulo": "Homem-Aranha Sem Volta Para Casa",
    "descricao": "Peter Parker tem a sua identidade secreta revelada e pede ajuda ao Doutor Estranho...",
    "imagem": r"C:\\Users\\59699816\\OneDrive - SENAC PA - EDU\\projeto\\aranha.jpg"
    },
    {
    "titulo": "Invocação do Mal",
    "descricao": "Baseado na história de uma fazenda assombrada em Rhode Island...",
    "imagem": r"C:\\Users\\59699816\\OneDrive - SENAC PA - EDU\\projeto\\mal.jpg"
    },
    ]

    # Frame principal do catálogo
    frame = ctk.CTkFrame(parent, fg_color="#1E1E1E")
    
    # Cache de imagens para evitar garbage collection
    frame.image_cache = {}
    
    # Variável para armazenar o filme selecionado
    filme_selecionado = ctk.IntVar(value=0)

    # ----- Frame Esquerdo: Lista de Filmes -----
    frame_esq = ctk.CTkFrame(frame, width=260)
    frame_esq.pack(side="left", fill="y", padx=(12, 6), pady=12)

    ctk.CTkLabel(frame_esq, text="Filmes em Cartaz", font=("Arial", 16, "bold")).pack(pady=(8, 6))

    scroll = ctk.CTkScrollableFrame(frame_esq, width=240, height=520)
    scroll.pack(fill="both", expand=True, padx=8, pady=8)

    # ----- Frame Direito: Detalhes -----
    frame_dir = ctk.CTkFrame(frame)
    frame_dir.pack(side="right", expand=True, fill="both", padx=(6, 12), pady=12)

    titulo_var = ctk.StringVar(value="Selecione um filme")
    descricao_var = ctk.StringVar(value="Descrição do filme aparecerá aqui.")

    label_titulo = ctk.CTkLabel(frame_dir, textvariable=titulo_var, font=("Arial", 18, "bold"))
    label_titulo.pack(anchor="nw", pady=(8, 6), padx=12)

    label_imagem = ctk.CTkLabel(frame_dir, text="")  # Será atualizado com PhotoImage
    label_imagem.pack(padx=12, pady=6)

    label_descricao = ctk.CTkLabel(frame_dir, textvariable=descricao_var, wraplength=520, justify="left")
    label_descricao.pack(anchor="nw", padx=12, pady=(6, 12))

    # ----- Função para Mostrar Detalhes do Filme -----
    def mostrar_filme(index: int):
        filme_selecionado.set(index)
        filme = filmes[index]
        titulo_var.set(filme["titulo"])
        descricao_var.set(filme["descricao"])

        caminho = filme.get("imagem", "")
        
        # tenta abrir a imagem, senão usa placeholder
        try:
            if os.path.exists(caminho):
                img = Image.open(caminho)
                img = img.resize((300, 450), Image.LANCZOS)
            else:
                raise FileNotFoundError
        except Exception as e:
            # Cria uma imagem placeholder
            img = Image.new("RGB", (300, 450), (40, 40, 40))
            # Adiciona texto à imagem placeholder
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            draw.text((150, 225), "Imagem não encontrada", fill=(255, 255, 255), anchor="mm", font=font)

        foto = ImageTk.PhotoImage(img)
        label_imagem.configure(image=foto)
        label_imagem.image = foto
        frame.image_cache[index] = foto  # guarda no cache

    # ----- Função para Confirmar Seleção -----
    def confirmar_selecao():
        index = filme_selecionado.get()
        filme = filmes[index]
        print(f"Filme selecionado: {filme['titulo']}")
        # Aqui você pode adicionar a lógica para processar a seleção do filme
        # Por exemplo, abrir uma nova janela, adicionar à lista de favoritos, etc.

    # ----- Cria Botões dos Filmes -----
    for idx, filme in enumerate(filmes):
        btn = ctk.CTkButton(
            scroll,
            text=filme["titulo"],
            width=220,
            height=40,
            command=lambda i=idx: mostrar_filme(i),
            fg_color="#2E2E2E",
            hover_color="#3D3D3D",
            text_color="white"
        )
        btn.pack(pady=4, padx=6, fill="x")

    # Frame para os botões de ação (Confirmar e Voltar)
    frame_botoes = ctk.CTkFrame(frame_dir, fg_color="transparent")
    frame_botoes.pack(side="bottom", fill="x", padx=12, pady=12)
    
    # Botão Confirmar
    btn_confirmar = ctk.CTkButton(
        frame_botoes, 
        text="Confirmar", 
        command=confirmar_selecao,
        width=100,
        height=40,
        fg_color="#4CAF50",  # Verde
        hover_color="#45a049",
        text_color="#FFFFFF",
        corner_radius=15,
        font=("Arial", 14, "bold")
    )
    btn_confirmar.pack(side="right", padx=(0, 10))

    # Botão Voltar
    btn_voltar = ctk.CTkButton(
        frame_botoes, 
        text="Voltar", 
        command=lambda: None,  # Será configurado pelo main
        width=100,
        height=40,
        text_color="#000000",
        fg_color="#F6C148",
        hover_color="#E2952D",
        border_color="#E2952D",
        corner_radius=15,
        font=("Arial", 14, "bold")
    )
    btn_voltar.pack(side="right")

    # Seleciona o primeiro filme automaticamente
    if filmes:
        mostrar_filme(0)

    def confirmar_selecao():
        index = filme_selecionado.get()
        filme = filmes[index]
        print(f"Filme selecionado: {filme['titulo']}")
        
        # Chamar a função para abrir a tela de sessões
        # Ajuste o caminho conforme a hierarquia real dos seus frames
        try:
            parent.master.master.on_filme_selecionado(filme)
        except:
            print("Erro ao abrir tela de sessões. Verifique a hierarquia dos frames.")
    
    return frame, btn_voltar, btn_confirmar