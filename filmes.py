import tkinter as tk

# =============================
# DADOS DOS FILMES
# =============================
filmes = [
    {
        "titulo": "Predador: Terras Selvagens",
        "direcao": "Dan Trachtenberg",
        "duracao": "98 min",
        "genero": "Terror, Suspense, Aventura, Ficção científica",
        "sinopse": "Um jovem guerreiro Comanche embarca em uma missão perigosa "
                   "para proteger sua tribo de uma ameaça alienígena mortal.",
        "classificacao": "12"
    },
    {"titulo": "Zootopia"},
    {"titulo": "Matrix"},
    {"titulo": "Interestelar"},
    {"titulo": "Jumanji"},
    {"titulo": "Demon Slayer - Castelo Infinito"},
    {"titulo": "Homem-Aranha: Sem Volta Para Casa"},
    {"titulo": "Invocação do Mal"},

    # 🔥 FILMES ADICIONADOS
    {"titulo": "Avatar"},
    {"titulo": "Vingadores: Ultimato"},
    {"titulo": "Jurassic Park"},
    {"titulo": "O Senhor dos Anéis"},
    {"titulo": "Batman: O Cavaleiro das Trevas"},
    {"titulo": "Star Wars"},
    {"titulo": "Mad Max: Estrada da Fúria"},
]

VISIBLE = 8
CARD_WIDTH = 130
CARD_HEIGHT = 190

# =============================
# APLICAÇÃO
# =============================
class CinemaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cinema")
        self.geometry("1200x700")
        self.configure(bg="#2b2b2b")

        self.index = 0
        self.filme_selecionado = filmes[0]

        self.criar_topo()
        self.criar_carrossel()
        self.criar_conteudo()
        self.criar_rodape()

    # =============================
    # TOPO - DIAS
    # =============================
    def criar_topo(self):
        topo = tk.Frame(self, bg="#2b2b2b")
        topo.pack(fill="x", pady=10)

        tk.Label(
            topo, text="Dias:",
            bg="#2b2b2b", fg="white",
            font=("Arial", 11, "bold")
        ).pack()

        dias = tk.Frame(topo, bg="#2b2b2b")
        dias.pack(pady=5)

        for dia in ["Sexta:09/01", "Sábado:10/01", "Domingo:11/01"]:
            tk.Button(
                dias,
                text=dia,
                bg="#f5c542",
                fg="black",
                font=("Arial", 10, "bold"),
                width=16,
                relief="flat"
            ).pack(side="left", padx=5)

    # =============================
    # CARROSSEL DE FILMES
    # =============================
    def criar_carrossel(self):
        area = tk.Frame(self, bg="#1f1f1f")
        area.pack(fill="x", pady=10)

        tk.Button(area, text="←", font=("Arial", 18),
                  command=self.prev).pack(side="left", padx=10)

        self.container = tk.Frame(area, bg="#1f1f1f")
        self.container.pack(side="left", expand=True)

        tk.Button(area, text="→", font=("Arial", 18),
                  command=self.next).pack(side="left", padx=10)

        self.draw_cards()

    def draw_cards(self):
        for w in self.container.winfo_children():
            w.destroy()

        for filme in filmes[self.index:self.index + VISIBLE]:
            card = tk.Frame(
                self.container,
                width=CARD_WIDTH,
                height=CARD_HEIGHT,
                bg="#f5c542",
                bd=2,
                relief="raised",
                cursor="hand2"
            )
            card.pack(side="left", padx=6)
            card.pack_propagate(False)

            card.bind("<Button-1>", lambda e, f=filme: self.selecionar_filme(f))

            tk.Label(
                card,
                text=filme["titulo"],
                bg="#f5c542",
                wraplength=110,
                font=("Arial", 9, "bold"),
                justify="center"
            ).pack(expand=True)

    def next(self):
        if self.index + VISIBLE < len(filmes):
            self.index += 1
            self.draw_cards()

    def prev(self):
        if self.index > 0:
            self.index -= 1
            self.draw_cards()

    # =============================
    # CONTEÚDO CENTRAL
    # =============================
    def criar_conteudo(self):
        corpo = tk.Frame(self, bg="#2b2b2b")
        corpo.pack(fill="both", expand=True, padx=10)

        # ---- DETALHES DO FILME
        self.detalhes = tk.Frame(corpo, bg="#1f1f1f")
        self.detalhes.pack(side="left", fill="both", expand=True, padx=5)

        self.lbl_titulo = tk.Label(
            self.detalhes,
            bg="#1f1f1f", fg="white",
            font=("Arial", 14, "bold")
        )
        self.lbl_titulo.pack(anchor="w", pady=10, padx=10)

        self.lbl_info = tk.Label(
            self.detalhes,
            bg="#1f1f1f", fg="white",
            justify="left",
            wraplength=700,
            font=("Arial", 10)
        )
        self.lbl_info.pack(anchor="w", padx=10)

        self.atualizar_detalhes()

        # ---- HORÁRIOS
        horarios = tk.Frame(corpo, bg="#1f1f1f", width=250)
        horarios.pack(side="right", fill="y")
        horarios.pack_propagate(False)

        tk.Label(
            horarios,
            text="Horários por Tipo de Sessão",
            bg="#1f1f1f", fg="white",
            font=("Arial", 11, "bold")
        ).pack(pady=10)

        tk.Label(horarios, text="Dublado",
                 bg="#1f1f1f", fg="white").pack(anchor="w", padx=10)

        tk.Label(horarios, text="Legendado",
                 bg="#1f1f1f", fg="white").pack(anchor="w", padx=10, pady=10)

    def selecionar_filme(self, filme):
        self.filme_selecionado = filme
        self.atualizar_detalhes()

    def atualizar_detalhes(self):
        f = self.filme_selecionado
        self.lbl_titulo.config(text=f["titulo"])

        texto = (
            f"Direção:\n{f.get('direcao','-')}\n\n"
            f"Duração:\n{f.get('duracao','-')}\n\n"
            f"Gênero:\n{f.get('genero','-')}\n\n"
            f"Sinopse:\n{f.get('sinopse','-')}\n\n"
            f"Classificação: {f.get('classificacao','-')}"
        )
        self.lbl_info.config(text=texto)

    # =============================
    # RODAPÉ
    # =============================
    def criar_rodape(self):
        rodape = tk.Frame(self, bg="#2b2b2b")
        rodape.pack(fill="x", pady=10)

        tk.Button(
            rodape, text="Voltar",
            bg="#f5c542", fg="black",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(side="left", padx=20)

        tk.Button(
            rodape, text="Selecionar Assentos",
            bg="#f5c542", fg="black",
            font=("Arial", 10, "bold"),
            width=20
        ).pack(side="right", padx=20)


# =============================
# EXECUÇÃO
# =============================
if __name__ == "__main__":
    app = CinemaApp()
    app.mainloop()
