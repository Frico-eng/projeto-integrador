import customtkinter as ctk

def criar_tela_assentos(root, voltar_callback=None, avancar_callback=None):
    """
    Cria e retorna o frame de seleção de assentos
    voltar_callback: função chamada ao clicar Voltar
    avancar_callback: função chamada ao clicar em Confirmar
    """
    
    # ================== CORES ==================
    COR_LIVRE       = "#BDC3C7"
    COR_SELECIONADO = "#27AE60"
    COR_OCUPADO     = "#C0392B"
    COR_TEXTO       = "#ECF0F1"
    COR_FUNDO       = "#1E1E1E"
    COR_PANEL       = "#2C3E50"
    
    # Frame principal - ocupa toda a área disponível
    frame = ctk.CTkFrame(root, fg_color=COR_FUNDO)
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Container principal
    container_principal = ctk.CTkFrame(frame, fg_color="transparent")
    container_principal.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Título
    ctk.CTkLabel(container_principal, text="Selecione seu assento", 
                font=("Arial", 24, "bold"), text_color="white").pack(pady=(0, 20))
    
    # Container para assentos e painel lado a lado
    container_conteudo = ctk.CTkFrame(container_principal, fg_color="transparent")
    container_conteudo.pack(fill="both", expand=True, pady=10)
    
    # Frame de assentos (maior, à esquerda)
    frame_assentos = ctk.CTkFrame(container_conteudo, fg_color=COR_FUNDO)
    frame_assentos.pack(side="left", fill="both", expand=True, padx=(0, 15))
    
    # Painel de resumo (menor, à direita)
    painel_resumo = ctk.CTkFrame(container_conteudo, width=280, fg_color=COR_PANEL)
    painel_resumo.pack(side="right", fill="y", padx=(15, 0))
    painel_resumo.pack_propagate(False)
    
    # Título do painel
    ctk.CTkLabel(painel_resumo, text="Assentos Selecionados", 
                font=("Arial", 18, "bold"), text_color="white").pack(pady=20)
    
    # Área para lista de assentos selecionados
    frame_lista = ctk.CTkScrollableFrame(painel_resumo, fg_color="transparent", height=150)
    frame_lista.pack(fill="both", expand=True, padx=15, pady=10)
    
    lista_selecionados = ctk.CTkLabel(frame_lista, text="Nenhum assento selecionado", 
                                     font=("Arial", 14), text_color="white", 
                                     justify="left", wraplength=250)
    lista_selecionados.pack(anchor="w")
    
    # Informações de preço
    ctk.CTkLabel(painel_resumo, text="Preço por assento: R$ 25,00", 
                font=("Arial", 12), text_color=COR_TEXTO).pack(pady=(20, 5))
    
    label_total = ctk.CTkLabel(painel_resumo, text="Total: R$ 0,00", 
                              font=("Arial", 20, "bold"), text_color="#F6C148")
    label_total.pack(pady=15)
    
    # ================== CONFIGURAÇÃO DOS ASSENTOS ==================
    linhas = ["A", "B", "C", "D", "E", "F", "G"]
    colunas = 8
    preco = 25.00
    assentos = {}
    selecionados = []
    
    # Container para centralizar a grade de assentos
    container_assentos = ctk.CTkFrame(frame_assentos, fg_color="transparent")
    container_assentos.pack(expand=True, pady=20)
    
    # Título da tela de assentos
    ctk.CTkLabel(container_assentos, text="TELA", font=("Arial", 16, "bold"), 
                text_color="#F6C148", fg_color="#34495E", corner_radius=5,
                width=300, height=30).pack(pady=(0, 30))
    
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
            assentos_formatados = ", ".join(selecionados)
            lista_selecionados.configure(text=assentos_formatados)
        
        total = len(selecionados) * preco
        label_total.configure(text=f"Total: R$ {total:.2f}")
    
    # Criar grade de assentos
    for i, linha in enumerate(linhas):
        linha_frame = ctk.CTkFrame(container_assentos, fg_color="transparent")
        linha_frame.pack(pady=3)
        
        for j in range(colunas):
            codigo = f"{linha}{j+1}"
            botao = ctk.CTkButton(linha_frame, text=codigo, width=60, height=50, 
                                 fg_color=COR_LIVRE, text_color=COR_TEXTO, 
                                 font=("Arial", 12, "bold"), corner_radius=8,
                                 command=lambda c=codigo: toggle_assento(c))
            botao.pack(side="left", padx=3)
            assentos[codigo] = (botao, "livre")
    
    # Marcar alguns assentos como ocupados para exemplo
    exemplos_ocupados = ["A1", "B3", "C5", "D2", "E7", "F4", "G6"]
    for codigo in exemplos_ocupados:
        if codigo in assentos:
            botao, _ = assentos[codigo]
            botao.configure(fg_color=COR_OCUPADO, state="disabled")
            assentos[codigo] = (botao, "ocupado")
    
    # ================== LEGENDA ==================
    frame_legenda = ctk.CTkFrame(container_assentos, fg_color="transparent")
    frame_legenda.pack(pady=20)
    
    ctk.CTkLabel(frame_legenda, text="Legenda:", font=("Arial", 12, "bold"), 
                text_color="white").pack(side="left", padx=(0, 15))
    
    ctk.CTkLabel(frame_legenda, text="● Disponível", font=("Arial", 11), 
                text_color=COR_LIVRE).pack(side="left", padx=10)
    
    ctk.CTkLabel(frame_legenda, text="● Selecionado", font=("Arial", 11), 
                text_color=COR_SELECIONADO).pack(side="left", padx=10)
    
    ctk.CTkLabel(frame_legenda, text="● Ocupado", font=("Arial", 11), 
                text_color=COR_OCUPADO).pack(side="left", padx=10)
    
    # ================== BOTÕES ==================
    frame_botoes = ctk.CTkFrame(container_principal, fg_color="transparent")
    frame_botoes.pack(pady=20)
    
    def confirmar():
        if not selecionados:
            lista_selecionados.configure(text="Selecione pelo menos um assento!")
            return
            
        # Marca os selecionados como ocupados
        for codigo in selecionados:
            botao, _ = assentos[codigo]
            botao.configure(fg_color=COR_OCUPADO, state="disabled")
            assentos[codigo] = (botao, "ocupado")
        
        # Mensagem de confirmação
        lista_selecionados.configure(text=f"Assentos confirmados!\n{', '.join(selecionados)}")
        
        # Chama a função de avançar para próxima tela
        if avancar_callback:
            avancar_callback()
        
        selecionados.clear()
        atualizar_resumo()
    
    # APENAS 2 BOTÕES: Voltar e Confirmar
    if voltar_callback:
        btn_voltar = ctk.CTkButton(frame_botoes, text="Voltar", text_color="white", 
                                  font=("Arial", 14, "bold"), width=150, height=40, 
                                  command=voltar_callback, fg_color="#34495E",
                                  hover_color="#2C3E50", corner_radius=10)
        btn_voltar.pack(side="left", padx=20)
    
    # Botão Confirmar substitui o Avançar - agora ele confirma E avança
    btn_confirmar = ctk.CTkButton(frame_botoes, text="Confirmar", text_color="#000000", 
                                 width=150, height=40, font=("Arial", 14, "bold"), 
                                 command=confirmar, fg_color="#F6C148", 
                                 hover_color="#E2952D", corner_radius=10)
    btn_confirmar.pack(side="right", padx=20)
    
    return frame