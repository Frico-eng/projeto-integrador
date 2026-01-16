import customtkinter as ctk
from PIL import Image, ImageTk
import os

# ================== CONFIGURAÇÃO ==================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================== DADOS ==================
filmes = [
    {
        "titulo": "O Senhor dos Anéis",
        "descricao": "O Senhor dos Anéis conta a saga do hobbit Frodo Bolseiro em sua missão para destruir o Um Anel, uma joia maligna criada pelo Senhor das Trevas Sauron, antes que ele seja usado para dominar a Terra-média. Acompanhado pela Companhia do Anel, composta por elfos, anões, homens e hobbits, Frodo enfrenta perigos e as forças de Sauron, que se aliam a outros vilões como Saruman. A jornada termina com a destruição do Anel na Montanha da Perdição, vencendo o mal e assegurando a paz na Terra-média.  ",
        "genero": "ficcção de aventura, literatura fantástica, alta fantasia.",
        "classificação": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\doze.png",
        "imagem": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\o senhor dos anéis.jpg",
        "sessoes": ["14:15", "18:00", "20:45", "21:15"]
    },
    {
        "titulo": "Matrix",
        "descricao": "O jovem programador Thomas Anderson é atormentado por estranhos pesadelos  em que está sempre conectado por cabos a um imenso sistema de computadores do futuro. À medida que o sonho se repete, ele começa a desconfiar da realidade. Thomas conhece os misteriosos Morpheus e Trinity e descobre que é vítima de um sistema inteligente e artificial chamado Matrix, que manipula a mente das pessoas e cria a ilusão de um mundo real enquanto usa os cérebros e corpos dos indivíduos para produzir energia.",
        "genero": "ação, Aventura, Ficção científica, Cyberpunk.",
        "classificação": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\catorze.jpg",
        "imagem": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\Matrix.jpg",
        "sessoes": ["14:45", "17:30", "19:00", "21:30"]
    },
    {
        "titulo": "Interstellar",
        "descricao": "As reservas naturais da Terra estão chegando ao fim e um grupo de astronautas recebe a missão  de verificar possíveis planetas para receberem a população mundial, possibilitando a continuação da espécie. Cooper é chamado para liderar o grupo e aceita a missão sabendo que pode nunca mais ver os filhos. Ao lado de Brand, Jenkins e Doyle, ele seguirá em busca de um novo lar.",
        "genero": "Ficção científica, Ação, Suspense, Aventura.",
        "classificação": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\dez.png",
        "imagem": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\Interstellar.jpg",
        "sessoes": ["13:00", "16:45", "20:00"]
    },
    {
        "titulo": "Jumanji",
        "descricao": "Quatro adolescentes encontram um videogame cuja ação se passa em uma floresta tropical. Empolgados com o jogo, eles escolhem seus avatares para o desafio, mas um evento inesperado faz com que eles sejam transportados para dentro do universo fictício, transformando-os nos personagens da aventura. ",
        "genero": "Comédia, Infantil, Aventura, Ação.",
        "classificação": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\livre.png",
        "imagem": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\jumanji.jpg",
        "sessoes": ["11:30", "15:00", "18:30"]
    },
    {
        "titulo": "Demon Slayer - Castelo Infinito",
        "descricao": "Os Pilares agora enfrentam Muzan e decidem atacá-lo juntos. No entanto, eles são transportados para a Fortaleza Infinita antes que possam desferir um único golpe e, portanto, são separados.",
        "genero": "Ação, Aventura, Fantasia Sombria e Artes Marciais.",
        "classificação": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\dezoito.png",
        "imagem": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\Demon Slayer - castelo infinito.jpg",
        "sessoes": ["12:00", "16:00", "19:45"]
    },
    {
        "titulo": "Homem-Aranha Sem Volta Para Casa",
        "descricao": "Peter Parker tem a sua identidade secreta revelada e pede ajuda ao Doutor Estranho. Quando o feitiço para reverter o evento não sai como esperado, o Homem-Aranha e o seu companheiro dos Vingadores precisam enfrentar inimigos de todo o multiverso.",
        "genero": "Filme super-heroi, Ação, Aventura, Comédia, Suspense",
        "classificação": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\doze.png",
        "imagem": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\Homem-aranha sem volta para casa.jpg",
        "sessoes": ["13:30", "17:15", "21:00"]
    },
    {
        "titulo": "Invocação do Mal",
        "descricao": "Invocação do Mal é um filme de terror que acompanha os investigadores paranormais Ed e Lorraine Warren, chamados para ajudar uma família aterrorizada por uma presença demoníaca em sua nova casa, nos anos 70. O casal luta para confrontar a entidade maligna que se alimenta do medo e busca controlar os membros da família, especialmente a mãe, em um caso que se torna o mais difícil de suas carreiras, tudo baseado em um caso real. ",
        "genero": "Terror, Sobrenatural, Mistério, Suspense.",
        "classificação": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\catorze.jpg",
        "imagem": r"C:\Users\58513786\Documents\Visual Studio 2022\aula10.py\listadproduto.py\ctk.py\tela.py\Invocação do mal.jpg",
        "sessoes": ["22:00"]
    },
]

# ================== APLICATIVO ==================
app = ctk.CTk()
app.title("Catálogo de Filmes (customtkinter)")
app.geometry("900x600")

# cache de imagens para evitar garbage collection
app.image_cache = {}

# ----- frame esquerdo: lista (scrollable) -----
frame_esq = ctk.CTkFrame(app, width=260)
frame_esq.pack(side="left", fill="y", padx=(12,6), pady=12)

ctk.CTkLabel(frame_esq, text="Filmes em Cartaz", font=("Arial", 16, "bold")).pack(pady=(8,6))

scroll = ctk.CTkScrollableFrame(frame_esq, width=240, height=520)
scroll.pack(fill="both", expand=True, padx=8, pady=8)

# ----- frame direito: detalhes -----
frame_dir = ctk.CTkFrame(app)
frame_dir.pack(side="right", expand=True, fill="both", padx=(6,12), pady=12)

titulo_var = ctk.StringVar(value="Selecione um filme")
descricao_var = ctk.StringVar(value="Descrição do filme aparecerá aqui.")
genero_var = ctk.StringVar(value="genêro do filme aparecera aqui.")
classificacao_var = ctk.StringVar(value="")

label_titulo = ctk.CTkLabel(frame_dir, textvariable=titulo_var, font=("Arial", 18, "bold"))
label_titulo.pack(anchor="nw", pady=(8,6), padx=12)

label_imagem = ctk.CTkLabel(frame_dir, text="")  # será atualizado com PhotoImage
label_imagem.pack(padx=12, pady=6)

label_descricao = ctk.CTkLabel(frame_dir, textvariable=descricao_var, wraplength=520, justify="left")
label_descricao.pack(anchor="nw", padx=12, pady=(6,12))

label_genero = ctk.CTkLabel(frame_dir, textvariable=genero_var, wraplength=520, justify="left")
label_genero.pack(anchor="nw", padx=12, pady=(6,12))

label_classificacao = ctk.CTkLabel(frame_dir, textvariable=classificacao_var, wraplength=520, justify="left")
label_classificacao.pack(anchor="nw", padx=12, pady=(6,12))

# ----- frame para sessões -----
frame_sessoes = ctk.CTkFrame(frame_dir)
frame_sessoes.pack(anchor="nw", padx=12, pady=(6,12), fill="x")

# Função que mostra as sessões (limpa e cria botões)
def mostrar_sessoes(sessoes):
    for widget in frame_sessoes.winfo_children():
        widget.destroy()

    if not sessoes:
        return

    ctk.CTkLabel(frame_sessoes, text="Sessões:", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0,6))

    for hora in sessoes:
        btn = ctk.CTkButton(frame_sessoes, text=hora, width=72, height=34, corner_radius=8)
        btn.pack(side="left", padx=6, pady=4)

# Função que mostra os detalhes do filme selecionado
def mostrar_filme(index: int):
    filme = filmes[index]
    titulo_var.set(filme.get("titulo", ""))
    descricao_var.set(filme.get("descricao", ""))
    genero_var.set(filme.get("genero", ""))

    # -------- imagem do filme --------
    caminho = filme.get("imagem", "")
    img = None
    if caminho and os.path.isfile(caminho):
        try:
            img = Image.open(caminho)
        except Exception:
            img = None

    if img is None:
        img = Image.new("RGB", (200, 400), (60, 60, 60))

    img.thumbnail((700, 700))
    foto = ImageTk.PhotoImage(img)
    label_imagem.configure(image=foto, text="")
    label_imagem.image = foto
    app.image_cache[f"poster_{index}"] = foto

    # -------- classificação (pode ser texto ou caminho de imagem) --------
    classificacao = filme.get("classificacao") or filme.get("classificação") or ""
    if isinstance(classificacao, str) and os.path.isfile(classificacao):
        try:
            img_c = Image.open(classificacao)
            img_c.thumbnail((90, 90))
            foto_c = ImageTk.PhotoImage(img_c)
            # remove textvariable antes de mostrar imagem para evitar conflito
            label_classificacao.configure(text="")
            label_classificacao.configure(image=foto_c)
            label_classificacao.image = foto_c
            label_classificacao.configure(textvariable=None)
            app.image_cache[f"class_{index}"] = foto_c
        except Exception:
            classificacao_var.set(str(classificacao))
            label_classificacao.configure(textvariable=classificacao_var, image=None)
    else:
        classificacao_var.set(str(classificacao))
        label_classificacao.configure(textvariable=classificacao_var, image=None)

    # -------- sessões --------
    sessoes = filme.get("sessoes", [])
    mostrar_sessoes(sessoes)


# cria botões (um por filme) dentro do scroll
for idx, filme in enumerate(filmes):
    btn = ctk.CTkButton(
        scroll,
        text=filme["titulo"],
        width=220,
        height=40,
        command=lambda i=idx: mostrar_filme(i)
    )
    btn.pack(pady=4, padx=6, fill="x")

# seleciona o primeiro filme por padrão (se houver)
if filmes:
    mostrar_filme(0)

# Nota: para rodar a interface, salve este arquivo e execute com Python onde customtkinter e Pillow estejam instalados.
# Ex.: pip install customtkinter pillow
if __name__ == "__main__":
    app.mainloop()
