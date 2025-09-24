import customtkinter as ctk
# --- Botão customizado ---
def criar_tela_assentos(root, voltar_callback=None, avancar_callback=None):
    """
    Cria e retorna o frame de seleção de assentos
    voltar_callback: função chamada ao clicar Voltar
    avancar_callback: função chamada ao clicar Avançar (após confirmação)
    """
    
    # ================== CORES ==================
    COR_LIVRE       = "#BDC3C7"
    COR_SELECIONADO = "#27AE60"
    COR_OCUPADO     = "#C0392B"
    COR_TEXTO       = "#ECF0F1"
    COR_FUNDO       = "#1E1E1E"
    COR_PANEL       = "#2C3E50"
    

    
    # Frame principal
    frame = ctk.CTkFrame(root, width=900, height=650, fg_color=COR_FUNDO)
    
    # Título
    ctk.CTkLabel(frame, text="Selecione seu assento", font=("Arial", 22, "bold"), text_color="white").pack(pady=20)

    # Container principal
    container = ctk.CTkFrame(frame, fg_color="transparent")
    container.pack(pady=10, fill="both", expand=True)

    # Grid de assentos
    frame_assentos = ctk.CTkFrame(container, fg_color=COR_FUNDO)
    frame_assentos.pack(side="left", padx=20, pady=20, fill="both", expand=True)

    # Painel de resumo
    painel_resumo = ctk.CTkFrame(container, width=200, fg_color=COR_PANEL)
    painel_resumo.pack(side="right", padx=20, pady=20, fill="y")
    
    ctk.CTkLabel(painel_resumo, text="Assentos Selecionados", font=("Arial", 16, "bold"), text_color="white").pack(pady=10)
    
    lista_selecionados = ctk.CTkLabel(painel_resumo, text="Nenhum assento selecionado", font=("Arial", 14), text_color="white", justify="left")
    lista_selecionados.pack(pady=10)

    label_total = ctk.CTkLabel(painel_resumo, text="Total: R$ 0,00", font=("Arial", 16, "bold"), text_color="white")
    label_total.pack(pady=10)

    # Config assentos
    linhas = ["A", "B", "C", "D", "E"]
    colunas = 5
    preco = 25.00
    assentos = {}
    selecionados = []

    def toggle_assento(codigo):
        botao, status = assentos[codigo]
        if status == "ocupado":
            return
        if status == "livre":
            botao.configure(fg_color=COR_SELECIONADO)
            assentos[codigo] = (botao, "selecionado")
            selecionados.append(codigo)
        elif status == "selecionado":
            botao.configure(fg_color=COR_LIVRE)
            assentos[codigo] = (botao, "livre")
            selecionados.remove(codigo)
        atualizar_resumo()

    def atualizar_resumo():
        if not selecionados:
            lista_selecionados.configure(text="Nenhum assento selecionado")
        else:
            lista_selecionados.configure(text="\n".join(selecionados))
        label_total.configure(text=f"Total: R$ {len(selecionados)*preco:.2f}")

    # Criar botões de assento
    for i, linha in enumerate(linhas):
        for j in range(colunas):
            codigo = f"{linha}{j}"
            botao = ctk.CTkButton(frame_assentos, text=codigo, width=50, height=40, fg_color=COR_LIVRE,
                                  text_color=COR_TEXTO, font=("Arial", 14, "bold"), corner_radius=10,
                                  command=lambda c=codigo: toggle_assento(c))
            botao.grid(row=i, column=j, padx=5, pady=5)
            assentos[codigo] = (botao, "livre")

    # ================== BOTÕES ==================
    frame_botoes = ctk.CTkFrame(frame, fg_color="transparent")
    frame_botoes.pack(pady=20)

    def confirmar():
        # Marca os selecionados como ocupados
        for codigo in selecionados:
            botao, _ = assentos[codigo]
            botao.configure(fg_color=COR_OCUPADO)
            assentos[codigo] = (botao, "ocupado")
        selecionados.clear()
        atualizar_resumo()

    ctk.CTkButton(frame_botoes, text="Confirmar",text_color="#000000", width=150, height=40, font=("Arial", 14, "bold"), command=confirmar, fg_color="#F6C148",hover_color="#E2952D",border_color="#E2952D", corner_radius=15).pack(side="left", padx=10)
    if avancar_callback:
        ctk.CTkButton(frame_botoes, text="Avançar",text_color="#000000", font=("Arial", 14, "bold"), width=150, height=40, command=avancar_callback, fg_color="#F6C148",hover_color="#E2952D",border_color="#E2952D", corner_radius=15).pack(side="left", padx=10)
    if voltar_callback:
        ctk.CTkButton(frame_botoes, text="Voltar",text_color="#000000", font=("Arial", 14, "bold"), width=150, height=40, command=voltar_callback, fg_color="#F6C148",hover_color="#E2952D",border_color="#E2952D", corner_radius=15).pack(side="left", padx=10)

    return frame
