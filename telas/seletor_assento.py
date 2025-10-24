import os
import customtkinter as ctk
from PIL import Image, ImageTk

BTN_COLOR = "#F6C148"
BTN_HOVER = "#E2952D"
BTN_TEXT = "#1C2732"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # sobe uma pasta (pai de 'telas')
IMAGE_DIR = os.path.join(BASE_DIR, "utilidades", "images")

def criar_tela_assentos(root, voltar_callback=None, avancar_callback=None, filme_selecionado=None):    
    """
    Cria e retorna o frame de seleção de assentos
    voltar_callback: função chamada ao clicar Voltar
    avancar_callback: função chamada ao clicar em Confirmar
    filme_selecionado: dicionário com informações do filme (titulo, cartaz, etc.)
    """
    
    # ================== CORES DOS ASSENTOS ==================
    COR_LIVRE       = "#BDC3C7"
    COR_SELECIONADO = "#27AE60"
    COR_OCUPADO     = "#C0392B"
    COR_TEXTO       = "#ECF0F1"
    
    # Frame principal grande - igual ao do catálogo
    frame = ctk.CTkFrame(root, fg_color="transparent", width=1800, height=900)
    frame.pack_propagate(False)
    
    # ----- frame esquerdo: cartaz do filme -----
    frame_esq = ctk.CTkFrame(frame, width=320, height=650,fg_color="#F6C148")
    frame_esq.pack(side="left", fill="y", padx=(12,6), pady=12)
    frame_esq.pack_propagate(False)

    ctk.CTkLabel(frame_esq, text="Detalhes do Filme", font=("Arial", 16, "bold"),text_color="black").pack(pady=(8,6))

    if filme_selecionado and "imagem" in filme_selecionado:
        try:
            # Carregar e redimensionar a imagem do cartaz
            imagem_original = Image.open(filme_selecionado["imagem"])
            imagem_redimensionada = imagem_original.resize((280, 350), Image.LANCZOS)
            cartaz_img = ctk.CTkImage(imagem_redimensionada, size=(280, 350))
            
            ctk.CTkLabel(frame_esq, image=cartaz_img, text="").pack(pady=10)
            
           # Informações do filme
            info_frame = ctk.CTkFrame(frame_esq, fg_color="transparent")
            info_frame.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(
                info_frame,
                text=filme_selecionado.get("titulo", ""),
                font=("Arial", 16, "bold"),
                wraplength=280,
                text_color="black"
            ).pack(pady=5)

            ctk.CTkLabel(
                info_frame,
                text=f"Gênero: {filme_selecionado.get('genero', '')}",
                font=("Arial", 12),
                wraplength=280,
                text_color="black"
            ).pack(pady=2)

            ctk.CTkLabel(
                info_frame,
                text=f"Duração: {filme_selecionado.get('teste', '')}",
                font=("Arial", 12),
                text_color="black"
            ).pack(pady=2)

            
            # Informações da sessão selecionada
            sessao_frame = ctk.CTkFrame(frame_esq, fg_color="transparent")
            sessao_frame.pack(fill="x", padx=10, pady=10)
            
            if filme_selecionado.get('dia_selecionado'):
                dia_info = filme_selecionado['dia_selecionado']
                ctk.CTkLabel(sessao_frame, text=f"Data: {dia_info['nome']} ({dia_info['label']})", 
                            font=("Arial", 12, "bold")).pack(pady=2)
            
            if filme_selecionado.get('tipo_selecionado'):
                ctk.CTkLabel(sessao_frame, text=f"Tipo: {filme_selecionado['tipo_selecionado'].capitalize()}", 
                            font=("Arial", 12)).pack(pady=2)
            
            if filme_selecionado.get('horario_selecionado'):
                ctk.CTkLabel(sessao_frame, text=f"Horário: {filme_selecionado['horario_selecionado']}", 
                            font=("Arial", 12)).pack(pady=2)
            
            # Carregar classificação
            if "classificacao" in filme_selecionado and os.path.isfile(filme_selecionado["classificacao"]):
                try:
                    img_class = Image.open(filme_selecionado["classificacao"])
                    img_class = img_class.resize((30, 30), Image.LANCZOS)
                    class_img = ctk.CTkImage(img_class, size=(30, 30))
                    
                    class_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                    class_frame.pack(pady=2)
                    ctk.CTkLabel(class_frame, text="Classificação: ", 
                                font=("Arial", 12)).pack(side="left")
                    ctk.CTkLabel(class_frame, image=class_img, text="").pack(side="left")
                except Exception as e:
                    print(f"Erro ao carregar classificação: {e}")
            
        except Exception as e:
            print(f"Erro ao carregar cartaz: {e}")
            ctk.CTkLabel(frame_esq, text="", 
                        font=("Arial", 14)).pack(pady=50)
    else:
        ctk.CTkLabel(frame_esq, text="Nenhum filme selecionado", 
                    font=("Arial", 14)).pack(pady=50)
    
    # ----- frame direito: assentos e resumo -----
    frame_dir = ctk.CTkFrame(frame, width=1800, height=700)
    frame_dir.pack(side="right", fill="both", padx=(6,12), pady=12)
    frame_dir.pack_propagate(False)

    # Título
    titulo_filme = filme_selecionado.get("titulo", "Selecione seu assento") if filme_selecionado else "Selecione seu assento"
    ctk.CTkLabel(frame_dir, text="Seleção de Assentos", 
                font=("Arial", 24, "bold")).pack(pady=(10, 10))

    # Container para assentos e resumo
    container_conteudo = ctk.CTkFrame(frame_dir, fg_color="transparent")
    container_conteudo.pack(fill="both", expand=True, pady=10)
    
    # ================== COLUNA ASSENTOS ==================
    frame_assentos_container = ctk.CTkFrame(container_conteudo, fg_color="transparent")
    frame_assentos_container.pack(side="left", fill="both", expand=True, padx=(0, 15))
    
    # Frame de assentos
    frame_assentos = ctk.CTkFrame(frame_assentos_container, fg_color="transparent")
    frame_assentos.pack(fill="both", expand=True)
    
    # ================== COLUNA RESUMO ==================
    painel_resumo = ctk.CTkFrame(container_conteudo, width=300, fg_color="transparent")
    painel_resumo.pack(side="right", fill="y", padx=(15, 0))
    painel_resumo.pack_propagate(False)
    
    # Título do painel
    ctk.CTkLabel(painel_resumo, text="Resumo da Compra", 
                font=("Arial", 18, "bold")).pack(pady=20)
    
    # Informações do filme no resumo
    info_compra_frame = ctk.CTkFrame(painel_resumo, fg_color="transparent")
    info_compra_frame.pack(fill="x", padx=15, pady=10)
    
    if filme_selecionado:
        ctk.CTkLabel(info_compra_frame, text=filme_selecionado.get("titulo", ""), 
                    font=("Arial", 14, "bold"), wraplength=250).pack(anchor="w")
        
        if filme_selecionado.get('horario_selecionado'):
            ctk.CTkLabel(info_compra_frame, text=f"Horário: {filme_selecionado['horario_selecionado']}", 
                        font=("Arial", 12)).pack(anchor="w", pady=2)
    
    # Área para lista de assentos selecionados
    frame_lista = ctk.CTkScrollableFrame(painel_resumo, fg_color="transparent", height=120)
    frame_lista.pack(fill="both", expand=True, padx=15, pady=10)
    
    lista_selecionados = ctk.CTkLabel(frame_lista, text="Nenhum assento selecionado", 
                                     font=("Arial", 14), 
                                     justify="left", wraplength=250)
    lista_selecionados.pack(anchor="w")
    
    # Informações de preço
    preco_info_frame = ctk.CTkFrame(painel_resumo, fg_color="transparent")
    preco_info_frame.pack(fill="x", padx=15, pady=10)
    
    ctk.CTkLabel(preco_info_frame, text="Preço por assento: R$ 25,00", 
                font=("Arial", 12)).pack(anchor="w", pady=2)
    
    label_total = ctk.CTkLabel(painel_resumo, text="Total: R$ 0,00", 
                              font=("Arial", 20, "bold"))
    label_total.pack(pady=15)
    
    # ================== CONFIGURAÇÃO DOS ASSENTOS ==================
    linhas = ["A", "B", "C", "D", "E", "F", "G"]
    colunas = 8
    preco = 25.00
    assentos = {}
    selecionados = []
    
    # Carregar imagem do assento - USANDO BASE_DIR E IMAGE_DIR
    caminho_assento = os.path.join(IMAGE_DIR, "assento.png")
    try:
        img_assento = Image.open(caminho_assento)
        # Redimensionar para caber no botão
        img_assento = img_assento.resize((30, 30), Image.LANCZOS)
        foto_assento = ctk.CTkImage(img_assento, size=(40, 40))
        print(f"Imagem do assento carregada: {caminho_assento}")
    except Exception as e:
        print(f"Erro ao carregar imagem do assento {caminho_assento}: {e}")
        foto_assento = None
    
    # Container para centralizar a grade de assentos
    container_assentos = ctk.CTkFrame(frame_assentos, fg_color="transparent")
    container_assentos.pack(expand=True, pady=20)
    
    # Título da tela de assentos
    ctk.CTkLabel(container_assentos, text="TELA", font=("Arial", 16, "bold"), 
                fg_color="#2b2b2b", corner_radius=5,
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
        
        # Chama a função de avançar para próxima tela (pagamento) passando os dados COMPLETOS
        if avancar_callback:
            dados_compra = {
                "filme": filme_selecionado,
                "assentos": selecionados.copy(),
                "quantidade": len(selecionados),  # ADICIONE ESTA LINHA
                "preco_unitario": preco,          # ADICIONE ESTA LINHA
                "total": len(selecionados) * preco
            }
            print(f"DEBUG: Chamando avancar_callback com {len(selecionados)} assentos")
            print(f"DEBUG: Dados completos: {dados_compra}")
            avancar_callback(dados_compra)
        else:
            print("ERRO: avancar_callback não definido!")
        
        selecionados.clear()
        atualizar_resumo()

    
    # Criar grade de assentos
    for i, linha in enumerate(linhas):
        linha_frame = ctk.CTkFrame(container_assentos, fg_color="transparent")
        linha_frame.pack(pady=3)
        
        for j in range(colunas):
            codigo = f"{linha}{j+1}"
            botao = ctk.CTkButton(
                linha_frame, 
                text=codigo, 
                width=70, 
                height=70, 
                fg_color=COR_LIVRE, 
                text_color=COR_TEXTO, 
                font=("Arial", 11, "bold"), 
                corner_radius=8,
                image=foto_assento,  # Adiciona a imagem do assento
                compound="top",      # Imagem acima do texto
                command=lambda c=codigo: toggle_assento(c)
            )
            botao.pack(side="left", padx=2)
            assentos[codigo] = (botao, "livre")
    
    # Marcar alguns assentos como ocupados para exemplo
    exemplos_ocupados = ["A1", "B3", "C5", "D2", "E7", "F4", "G6"]
    for codigo in exemplos_ocupados:
        if codigo in assentos:
            botao, _ = assentos[codigo]
            botao.configure(fg_color=COR_OCUPADO, state="disabled")
            assentos[codigo] = (botao, "ocupado")
    
    # ================== LEGENDA COM FRAME DESTACADO ==================
    frame_legenda = ctk.CTkFrame(container_assentos, 
                                fg_color="#2b2b2b", 
                                border_width=2,
                                border_color="#444444",
                                corner_radius=12,height=45)
    frame_legenda.pack(pady=20, padx=20, fill="x")
    
    # Título da legenda
    ctk.CTkLabel(frame_legenda, text="Legenda dos Assentos", 
                font=("Arial", 14, "bold"),
                text_color=COR_TEXTO).pack(pady=(10, 8))
    
    # Container para os itens da legenda
    legenda_itens_frame = ctk.CTkFrame(frame_legenda, fg_color="transparent",height=40)
    legenda_itens_frame.pack(fill="x", padx=15, pady=(0, 10))
    
    # Item 1 - Disponível
    item1_frame = ctk.CTkFrame(legenda_itens_frame, fg_color="transparent")
    item1_frame.pack(side="left", expand=True, padx=10)
    
    ctk.CTkLabel(item1_frame, text="●", font=("Arial", 20), 
                text_color=COR_LIVRE).pack(side="left", padx=(0, 5))
    ctk.CTkLabel(item1_frame, text="Disponível", font=("Arial", 16), 
                text_color=COR_TEXTO).pack(side="left")
    
    # Item 2 - Selecionado
    item2_frame = ctk.CTkFrame(legenda_itens_frame, fg_color="transparent")
    item2_frame.pack(side="left", expand=True, padx=10)
    
    ctk.CTkLabel(item2_frame, text="●", font=("Arial", 20), 
                text_color=COR_SELECIONADO).pack(side="left", padx=(0, 5))
    ctk.CTkLabel(item2_frame, text="Selecionado", font=("Arial", 16), 
                text_color=COR_TEXTO).pack(side="left")
    
    # Item 3 - Ocupado
    item3_frame = ctk.CTkFrame(legenda_itens_frame, fg_color="transparent")
    item3_frame.pack(side="left", expand=True, padx=10)
    
    ctk.CTkLabel(item3_frame, text="●", font=("Arial", 20), 
                text_color=COR_OCUPADO).pack(side="left", padx=(0, 5))
    ctk.CTkLabel(item3_frame, text="Ocupado", font=("Arial", 16), 
                text_color=COR_TEXTO).pack(side="left")
    
    # ================== BOTÕES ==================
    frame_botoes = ctk.CTkFrame(frame_dir,height=100)
    frame_botoes.pack(side="bottom", fill="x", padx=20, pady=0)

    # APENAS 2 BOTÕES: Voltar e Confirmar
    if voltar_callback:
        btn_voltar = ctk.CTkButton(frame_botoes, text="Voltar",
                                  font=("Arial", 14, "bold"), width=150, height=40, 
                                  command=voltar_callback, 
                                  fg_color=BTN_COLOR,
                                  hover_color=BTN_HOVER,
                                  text_color=BTN_TEXT)
        btn_voltar.pack(side="left", padx=10)

    # Botão Confirmar que também avança para pagamento
    btn_confirmar = ctk.CTkButton(frame_botoes, text="Confirmar", 
                                 width=150, height=40, font=("Arial", 14, "bold"), 
                                 command=confirmar, 
                                 fg_color=BTN_COLOR,
                                 hover_color=BTN_HOVER,
                                 text_color=BTN_TEXT)
    btn_confirmar.pack(side="left", padx=20)
    
    return frame