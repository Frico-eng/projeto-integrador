import customtkinter as ctk
from PIL import Image, ImageTk

def criar_tela_assentos(root, voltar_callback=None, avancar_callback=None, filme_selecionado=None):
    """
    Cria e retorna o frame de seleção de assentos
    voltar_callback: função chamada ao clicar Voltar
    avancar_callback: função chamada ao clicar em Confirmar
    filme_selecionado: dicionário com informações do filme (titulo, cartaz, etc.)
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
    titulo_filme = filme_selecionado.get("titulo", "Selecione seu assento") if filme_selecionado else "Selecione seu assento"
    ctk.CTkLabel(container_principal, text=titulo_filme, 
                font=("Arial", 24, "bold"), text_color="white").pack(pady=(0, 20))
    
    # Container principal com 3 colunas: Cartaz + Assentos + Resumo
    container_conteudo = ctk.CTkFrame(container_principal, fg_color="transparent")
    container_conteudo.pack(fill="both", expand=True, pady=10)
    
    # ================== COLUNA 1: CARTAZ DO FILME ==================
    frame_cartaz = ctk.CTkFrame(container_conteudo, width=250, fg_color="transparent")
    frame_cartaz.pack(side="left", fill="y", padx=(0, 15))
    frame_cartaz.pack_propagate(False)
    
    if filme_selecionado and "cartaz" in filme_selecionado:
        try:
            # Carregar e redimensionar a imagem do cartaz
            imagem_original = Image.open(filme_selecionado["cartaz"])
            imagem_redimensionada = imagem_original.resize((220, 300), Image.LANCZOS)
            cartaz_img = ctk.CTkImage(imagem_redimensionada, size=(220, 300))
            
            ctk.CTkLabel(frame_cartaz, image=cartaz_img, text="").pack(pady=10)
            
            # Informações do filme
            info_frame = ctk.CTkFrame(frame_cartaz, fg_color=COR_PANEL, corner_radius=10)
            info_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(info_frame, text=filme_selecionado.get("titulo", ""), 
                        font=("Arial", 16, "bold"), text_color="white").pack(pady=5)
            
            ctk.CTkLabel(info_frame, text=f"Gênero: {filme_selecionado.get('genero', '')}", 
                        font=("Arial", 12), text_color=COR_TEXTO).pack(pady=2)
            
            ctk.CTkLabel(info_frame, text=f"Duração: {filme_selecionado.get('duracao', '')}", 
                        font=("Arial", 12), text_color=COR_TEXTO).pack(pady=2)
            
            ctk.CTkLabel(info_frame, text=f"Classificação: {filme_selecionado.get('classificacao', '')}", 
                        font=("Arial", 12), text_color=COR_TEXTO).pack(pady=2)
            
        except Exception as e:
            print(f"Erro ao carregar cartaz: {e}")
            ctk.CTkLabel(frame_cartaz, text="Cartaz não disponível", 
                        font=("Arial", 14), text_color="white").pack(pady=50)
    else:
        ctk.CTkLabel(frame_cartaz, text="Nenhum filme selecionado", 
                    font=("Arial", 14), text_color="white").pack(pady=50)
    
    # ================== COLUNA 2: ASSENTOS ==================
    frame_assentos_container = ctk.CTkFrame(container_conteudo, fg_color="transparent")
    frame_assentos_container.pack(side="left", fill="both", expand=True, padx=15)
    
    # Frame de assentos
    frame_assentos = ctk.CTkFrame(frame_assentos_container, fg_color=COR_FUNDO)
    frame_assentos.pack(fill="both", expand=True)
    
    # ================== COLUNA 3: PAINEL DE RESUMO ==================
    painel_resumo = ctk.CTkFrame(container_conteudo, width=280, fg_color=COR_PANEL)
    painel_resumo.pack(side="right", fill="y", padx=(15, 0))
    painel_resumo.pack_propagate(False)
    
    # Título do painel
    ctk.CTkLabel(painel_resumo, text="Resumo da Compra", 
                font=("Arial", 18, "bold"), text_color="white").pack(pady=20)
    
    # Informações do filme no resumo
    info_compra_frame = ctk.CTkFrame(painel_resumo, fg_color="transparent")
    info_compra_frame.pack(fill="x", padx=15, pady=10)
    
    if filme_selecionado:
        ctk.CTkLabel(info_compra_frame, text=filme_selecionado.get("titulo", ""), 
                    font=("Arial", 14, "bold"), text_color="#F6C148").pack(anchor="w")
        
        ctk.CTkLabel(info_compra_frame, text=f"Horário: {filme_selecionado.get('horario_selecionado', '')}", 
                    font=("Arial", 12), text_color=COR_TEXTO).pack(anchor="w", pady=2)
    
    # Área para lista de assentos selecionados
    frame_lista = ctk.CTkScrollableFrame(painel_resumo, fg_color="transparent", height=120)
    frame_lista.pack(fill="both", expand=True, padx=15, pady=10)
    
    lista_selecionados = ctk.CTkLabel(frame_lista, text="Nenhum assento selecionado", 
                                     font=("Arial", 14), text_color="white", 
                                     justify="left", wraplength=250)
    lista_selecionados.pack(anchor="w")
    
    # Informações de preço
    preco_info_frame = ctk.CTkFrame(painel_resumo, fg_color="transparent")
    preco_info_frame.pack(fill="x", padx=15, pady=10)
    
    ctk.CTkLabel(preco_info_frame, text="Preço por assento: R$ 25,00", 
                font=("Arial", 12), text_color=COR_TEXTO).pack(anchor="w", pady=2)
    
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
                width=400, height=30).pack(pady=(0, 30))
    
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
            lista_selecionados.configure(text=f"Assentos:\n{assentos_formatados}")
        
        total = len(selecionados) * preco
        label_total.configure(text=f"Total: R$ {total:.2f}")
    
    # Criar grade de assentos
    for i, linha in enumerate(linhas):
        linha_frame = ctk.CTkFrame(container_assentos, fg_color="transparent")
        linha_frame.pack(pady=3)
        
        for j in range(colunas):
            codigo = f"{linha}{j+1}"
            botao = ctk.CTkButton(linha_frame, text=codigo, width=50, height=45, 
                                 fg_color=COR_LIVRE, text_color=COR_TEXTO, 
                                 font=("Arial", 11, "bold"), corner_radius=8,
                                 command=lambda c=codigo: toggle_assento(c))
            botao.pack(side="left", padx=2)
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
        
        # Chama a função de avançar para próxima tela (pagamento)
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
    
    # Botão Confirmar que também avança para pagamento
    btn_confirmar = ctk.CTkButton(frame_botoes, text="Confirmar", text_color="#000000", 
                                 width=150, height=40, font=("Arial", 14, "bold"), 
                                 command=confirmar, fg_color="#F6C148", 
                                 hover_color="#E2952D", corner_radius=10)
    btn_confirmar.pack(side="right", padx=20)
    
    return frame