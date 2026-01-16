FILME_IMAGES = {
    "predador_terras_selvagens": os.path.join(IMAGE_DIR, "predador.jpg"),
    "zootopia": os.path.join(IMAGE_DIR, "zootopia.jpg"),
    "matrix": os.path.join(IMAGE_DIR, "matrix.jpg"),
    "interstellar": os.path.join(IMAGE_DIR, "Interstellar.jpg"),
    "jumanji": os.path.join(IMAGE_DIR, "jumanji.jpg"),
    "demon_slayer": os.path.join(IMAGE_DIR, "Demon Slayer - castelo infinito.jpg"),
    "homem_aranha": os.path.join(IMAGE_DIR, "Homem-aranha Sem volta para casa.jpg"),
    "invocacao_mal": os.path.join(IMAGE_DIR, "invocação do mal.jpg"),
}
print(FILME_IMAGES["matrix"])
# Caminhos para as classificações indicativas
CLASSIFICACOES = {
    "LIVRE": os.path.join(IMAGE_DIR, "livre.png"),
    "12": os.path.join(IMAGE_DIR, "doze.png"),
    "12": os.path.join(IMAGE_DIR, "doze.png"),
    "14": os.path.join(IMAGE_DIR, "catorze.jpg"),
    "10": os.path.join(IMAGE_DIR, "dez.png"),
    "LIVRE": os.path.join(IMAGE_DIR, "livre.png"),
    "18": os.path.join(IMAGE_DIR, "dezoito.png"),
}

# ================== DADOS DOS FILMES ==================
filmes = [
    {"titulo": "predador terras selvagens",
        "descricao": "O filme se passa no futuro, em um planeta remoto, onde um jovem Predador da raça Yautja, excluído de seu clã, encontra uma aliada improvável em Thia (Fanning) e embarca em uma jornada traiçoeira em busca de um monstro que supostamente não pode ser morto.",
        "teste": "6 de novembro de 2025 | 1h 38min",
        "genero": "terror, suspense, Aventura, Ficção científica.",
        "direçao": "Dan Trachtenberg",
        "classificacao": CLASSIFICACOES["12"],
        "imagem": FILME_IMAGES["predador_terras_selvagens"],
        "sessoes_dublado": ["14:50", "17:00", "20:00", "22:15"],
        "sessoes_legendado": ["17:30", "20:45", "21:15"]
        },
    {
        "titulo": "zootopia",
        "descricao": "Em uma cidade de animais, uma raposa falante se torna uma fugitiva ao ser acusada de um crime que não cometeu. O principal policial do local, o incontestável coelho, sai em sua busca..",
        "teste": "17 de março de 2025 | 1h 48min",
        "genero": "Ficção policial, infantil, animação, Aventura, Animação.",
        "direçao": "Rich Moore, Byron Howard",
        "classificacao": CLASSIFICACOES["LIVRE"],
        "imagem": FILME_IMAGES["zootopia"],
        "sessoes_dublado": ["14:15", "18:00", "20:30", "21:00"],
        "sessoes_legendado": ["17:00", "20:45", "21:15"]
    },
    {
        "titulo": "Matrix",
        "descricao": "O jovem programador Thomas Anderson é atormentado por estranhos pesadelos em que está sempre conectado por cabos a um imenso sistema de computadores do futuro. À medida que o sonho se repete, ele começa a desconfiar da realidade. Thomas conhece os misteriosos Morpheus e Trinity e descobre que é vítima de um sistema inteligente e artificial chamado Matrix, que manipula a mente das pessoas e cria a ilusão de um mundo real enquanto usa os cérebros e corpos dos indivíduos para produzir energia.",
        "teste": "11 de setembro de 2025 | 1h 49min",
        "genero": "Ação, Aventura, Ficção científica, Cyberpunk.",
        "direçao": "Lana Wachowski e Lilly Wachowski",
        "classificacao": CLASSIFICACOES["14"],
        "imagem": FILME_IMAGES["matrix"],
        "sessoes_dublado": ["14:45", "17:30", "19:30", "22:30"],
        "sessoes_legendado": ["16:50", "19:00", "21:30"]
    },
    {
        "titulo": "Interstellar",
        "descricao": "As reservas naturais da Terra estão chegando ao fim e um grupo de astronautas recebe a missão de verificar possíveis planetas para receberem a população mundial, possibilitando a continuação da espécie. Cooper é chamado para liderar o grupo e aceita a missão sabendo que pode nunca mais ver os filhos. Ao lado de Brand, Jenkins e Doyle, ele seguirá em busca de um novo lar.",
        "teste": "4 de setembro de 2025 | 1h 27min",
        "genero": "Ficção científica, Ação, Suspense, Aventura.",
        "direçao": "Christopher Nolan",
        "classificacao": CLASSIFICACOES["10"],
        "imagem": FILME_IMAGES["interstellar"],
        "sessoes_dublado": ["13:00", "16:45", "20:30"],
        "sessoes_legendado": ["17:00", "20:00", "22:30"]
    },
    {
        "titulo": "Jumanji",
        "descricao": "Quatro adolescentes encontram um videogame cuja ação se passa em uma floresta tropical. Empolgados com o jogo, eles escolhem seus avatares para o desafio, mas um evento inesperado faz com que eles sejam transportados para dentro do universo fictício, transformando-os nos personagens da aventura.",
        "teste": "11 de setembro de 2025 | 1h 30min",
        "genero": "Comédia, Infantil, Aventura, Ação.",
        "direçao": "Jake Kasdan e Joe Johnston",
        "classificacao": CLASSIFICACOES["LIVRE"],
        "imagem": FILME_IMAGES["jumanji"],
        "sessoes_dublado": ["11:30", "15:00", "18:00", "21:00"],
        "sessoes_legendado": ["18:30", "21:30"]
    },
    {
        "titulo": "Demon Slayer - Castelo Infinito",
        "descricao": "Os Pilares agora enfrentam Muzan e decidem atacá-lo juntos. No entanto, eles são transportados para a Fortaleza Infinita antes que possam desferir um único golpe e, portanto, são separados.",
        "teste": "11 de setembro de 2025 | 2h 36min",
        "genero": "Ação, Aventura, Fantasia Sombria e Artes Marciais.",
        "direçao": "Haruo Sotozaki",
        "classificacao": CLASSIFICACOES["18"],
        "imagem": FILME_IMAGES["demon_slayer"],
        "sessoes_dublado": ["12:00", "16:00", "19:45", "22:45"],
        "sessoes_legendado": ["19:00", "20:45"]
    },
    {
        "titulo": "Homem-Aranha Sem Volta Para Casa",
        "descricao": "Peter Parker tem a sua identidade secreta revelada e pede ajuda ao Doutor Estranho. Quando o feitiço para reverter o evento não sai como esperado, o Homem-Aranha e o seu companheiro dos Vingadores precisam enfrentar inimigos de todo o multiverso.",
        "teste": "18 de setembro de 2025 | 1h 38min",
        "genero": "Filme super-herói, Ação, Aventura, Comédia, Suspense",
        "direçao": "Jon Watts",
        "classificacao": CLASSIFICACOES["12"],
        "imagem": FILME_IMAGES["homem_aranha"],
        "sessoes_dublado": ["13:30", "17:15", "21:00"],
        "sessoes_legendado": ["16:20", "19:00", "22:30"]
    },
    {
        "titulo": "Invocação do Mal",
        "descricao": "Invocação do Mal acompanha os investigadores paranormais Ed e Lorraine Warren, chamados para ajudar uma família aterrorizada por uma presença demoníaca em sua nova casa, nos anos 70. O casal luta para confrontar a entidade maligna que se alimenta do medo e busca controlar os membros da família, especialmente a mãe, em um caso que se torna o mais difícil de suas carreiras, tudo baseado em um caso real.",
        "teste": "4 de setembro de 2025 | 2h 15min",
        "genero": "Terror, Sobrenatural, Mistério, Suspense.",
        "direçao": "Michael Chaves",
        "classificacao": CLASSIFICACOES["14"],
        "imagem": FILME_IMAGES["invocacao_mal"],
        "sessoes_dublado": ["13:00", "16:00", "22:00", "23:30"],
        "sessoes_legendado": ["17:00", "19:45", "23:00"]
    },
]