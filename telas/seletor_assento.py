import os
import customtkinter as ctk
from PIL import Image, ImageTk
from crud.crud_filme import buscar_filme_por_id
from crud.crud_sessao import buscar_sessao_por_dados, listar_sessoes_por_filme
from crud.crud_sala import buscar_sala_por_id
from crud.crud_assento_sessao import (
    listar_assentos_por_sessao, 
    reservar_assento, 
    verificar_disponibilidade_assento,
    obter_resumo_ocupacao_sessao,
    obter_info_sessao
)
from utilidades.session import get_user_id

BTN_COLOR = "#F6C148"
BTN_HOVER = "#E2952D"
BTN_TEXT = "#1C2732"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "utilidades", "images")

def criar_tela_assentos(root, voltar_callback=None, avancar_callback=None, filme_selecionado=None, fonte_global=None):    
    """
    Cria e retorna o frame de seleção de assentos
    """
    
    # Funções para aumentar/diminuir fonte (usa fonte_global quando disponível, caso contrário aplica localmente)
    def aplicar_fonte_local():
        """Atualiza widgets desta tela com o tamanho local `current_font_size`."""
        fs = current_font_size
        try:
            lista_selecionados.configure(font=("Arial", fs))
        except Exception:
            pass
        try:
            label_total.configure(font=("Arial", max(10, fs+6), "bold"))
        except Exception:
            pass
        try:
            label_titulo_resumo.configure(font=("Arial", max(10, fs+2), "bold"))
            label_horario_resumo.configure(font=("Arial", fs))
            label_sala_resumo.configure(font=("Arial", fs))
            label_ocupacao.configure(font=("Arial", fs))
        except Exception:
            pass
        # Atualiza botões de assento existentes
        for codigo, (botao, status, id_assento, id_assento_sessao) in assentos.items():
            try:
                botao.configure(font=("Arial", fs, "bold"))
            except Exception:
                pass
        # Atualiza labels e botões do frame esquerdo (detalhes do filme)
        try:
            for w in frame_esq.winfo_children():
                try:
                    w.configure(font=("Arial", max(10, fs)))
                except Exception:
                    pass
                # filhos internos (info_frame, sessao_frame, etc.)
                try:
                    for c in w.winfo_children():
                        try:
                            c.configure(font=("Arial", max(10, fs)))
                        except Exception:
                            pass
                        try:
                            for d in c.winfo_children():
                                try:
                                    d.configure(font=("Arial", max(10, fs)))
                                except Exception:
                                    pass
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception:
            pass

    def aumentar_fonte():
        nonlocal current_font_size
        if fonte_global:
            if fonte_global.cget("size") < 22:
                fonte_global.configure(size=fonte_global.cget("size") + 2)
        else:
            if current_font_size < 22:
                current_font_size += 2
                aplicar_fonte_local()

    def diminuir_fonte():
        nonlocal current_font_size
        if fonte_global:
            if fonte_global.cget("size") > 6:
                fonte_global.configure(size=fonte_global.cget("size") - 2)
        else:
            if current_font_size > 6:
                current_font_size -= 2
                aplicar_fonte_local()
    
    # ================== CORES DOS ASSENTOS ==================
    COR_LIVRE = "#BDC3C7"
    COR_SELECIONADO = "#27AE60"
    COR_OCUPADO = "#C0392B"
    COR_TEXTO = "#ECF0F1"
    
    # Frame principal
    frame = ctk.CTkFrame(root, fg_color="transparent", width=1800, height=900)
    frame.pack_propagate(False)
    
    # ================== VARIÁVEIS ==================
    filme_info = None
    sala_info = None
    sessao_info = None
    assentos_info = []
    assentos = {}
    selecionados = []
    preco = 25.00
    seat_icon = None  # Variável para armazenar o ícone do assento
    current_font_size = fonte_global.cget("size") if fonte_global else 14

    # ================== FUNÇÕES PRINCIPAIS (DEFINIDAS PRIMEIRO) ==================
    
    def carregar_icone_assento():
        """Carrega o ícone do assento"""
        nonlocal seat_icon
        try:
            seat_icon_path = os.path.join(IMAGE_DIR, "seat.png")
            if os.path.exists(seat_icon_path):
                # Carregar e redimensionar a imagem
                img = Image.open(seat_icon_path)
                # Redimensionar para caber no botão (ajuste o tamanho conforme necessário)
                img_resized = img.resize((20, 20), Image.LANCZOS)
                seat_icon = ctk.CTkImage(img_resized, size=(20, 20))
                print("DEBUG: Ícone do assento carregado com sucesso")
            else:
                print(f"DEBUG: Arquivo do ícone não encontrado em: {seat_icon_path}")
                seat_icon = None
        except Exception as e:
            print(f"DEBUG: Erro ao carregar ícone do assento: {e}")
            seat_icon = None

    def confirmar():
        """Confirma a seleção"""
        print(f"DEBUG: Confirmando {len(selecionados)} assentos...")
        
        if not selecionados:
            lista_selecionados.configure(text="Selecione pelo menos um assento!")
            print("DEBUG: Nenhum assento selecionado para confirmar")
            return
            
        try:
            if not sessao_info:
                lista_selecionados.configure(text="Erro: Sessão não encontrada!")
                return
                
            id_sessao = sessao_info["ID_Sessao"]
            print(f"DEBUG: Reservando assentos para sessão {id_sessao}...")
            
            # Reservar cada assento individualmente e capturar ID_Assento_Sessao
            assentos_reservados = []
            assentos_reservados_sessao = []
            for assento in selecionados:
                id_cliente = get_user_id()
                if not id_cliente:
                    lista_selecionados.configure(text="Faça login para reservar assentos.")
                    print("DEBUG: Usuário não logado ao tentar reservar")
                    continue

                sucesso = reservar_assento(
                    id_sessao, 
                    assento["id_assento"], 
                    id_cliente=id_cliente
                )
                if sucesso:
                    assentos_reservados.append(assento["codigo"])
                    # usar o ID_Assento_Sessao armazenado na seleção
                    id_assento_sessao = assento.get("id_assento_sessao")
                    if id_assento_sessao:
                        assentos_reservados_sessao.append(id_assento_sessao)
                    print(f"DEBUG: Assento {assento['codigo']} reservado com sucesso")
                else:
                    print(f"DEBUG: Erro ao reservar assento {assento['codigo']}")
            
            if assentos_reservados:
                lista_selecionados.configure(text=f"Assentos confirmados!\n{', '.join(assentos_reservados)}")
                print(f"DEBUG: Assentos confirmados: {assentos_reservados}")
                
                if avancar_callback:
                    # Estruturar dados de forma consistente
                    dados_compra = {
                        "filme": filme_info,
                        "sala": sala_info,
                        "sessao": sessao_info,
                        "assentos": assentos_reservados,
                        "assentos_ids_sessao": assentos_reservados_sessao,
                        "quantidade": len(assentos_reservados),
                        "preco_unitario": preco,
                        "total": len(assentos_reservados) * preco
                    }
                    
                    print(f"DEBUG: Estrutura de dados enviada:")
                    print(f"  - Filme: {filme_info.get('Titulo_Filme') if filme_info else 'N/A'}")
                    print(f"  - Sessao ID: {sessao_info.get('ID_Sessao')}")
                    print(f"  - Assentos: {assentos_reservados}")
                    
                    avancar_callback(dados_compra)
                else:
                    print("ERRO: avancar_callback não definido!")
                
                # Atualizar interface para refletir assentos ocupados
                print("DEBUG: Atualizando interface após confirmação...")
                for assento in selecionados:
                    codigo = assento["codigo"]
                    if codigo in assentos:
                        botao, _, id_assento, id_assento_sessao = assentos[codigo]
                        botao.configure(fg_color=COR_OCUPADO, state="disabled", image="")
                        assentos[codigo] = (botao, "ocupado", id_assento, id_assento_sessao)
                
                selecionados.clear()
                atualizar_resumo()
                print("DEBUG: Confirmação concluída com sucesso")
            else:
                lista_selecionados.configure(text="Erro ao reservar assentos!")
            
        except Exception as e:
            print(f"Erro ao confirmar: {e}")
            lista_selecionados.configure(text="Erro ao confirmar assentos!")
            import traceback
            traceback.print_exc()

    def toggle_assento(codigo, id_assento):
        """Alterna seleção do assento"""
        nonlocal selecionados
        
        if codigo not in assentos:
            return
            
        # Desempacotar: (botao, status, ID_Assento, ID_Assento_Sessao)
        botao, status, id_assento, id_assento_sessao = assentos[codigo]
        if status == "ocupado":
            return
            
        if status == "livre":
            # Verificar disponibilidade no banco
            if sessao_info and verificar_disponibilidade_assento(sessao_info["ID_Sessao"], id_assento):
                botao.configure(fg_color=COR_SELECIONADO)
                assentos[codigo] = (botao, "selecionado", id_assento, id_assento_sessao)
                selecionados.append({"codigo": codigo, "id_assento": id_assento, "id_assento_sessao": id_assento_sessao})
                print(f"DEBUG: Assento {codigo} selecionado")
            else:
                print(f"DEBUG: Assento {codigo} não está mais disponível")
                botao.configure(fg_color=COR_OCUPADO, state="disabled", image="")
                assentos[codigo] = (botao, "ocupado", id_assento, id_assento_sessao)
        else:
            botao.configure(fg_color=COR_LIVRE)
            assentos[codigo] = (botao, "livre", id_assento, id_assento_sessao)
            selecionados = [item for item in selecionados if item["codigo"] != codigo]
            print(f"DEBUG: Assento {codigo} desselecionado")
            
        atualizar_resumo()

    def atualizar_resumo():
        """Atualiza o resumo"""
        print(f"DEBUG: Atualizando resumo - {len(selecionados)} assentos selecionados")
        
        if not selecionados:
            lista_selecionados.configure(text="Nenhum assento selecionado")
        else:
            assentos_str = ", ".join([item["codigo"] for item in selecionados])
            lista_selecionados.configure(text=f"Assentos selecionados:\n{assentos_str}")
        
        total = len(selecionados) * preco
        label_total.configure(text=f"Total: R$ {total:.2f}")
        
        # Atualizar informações de ocupação se houver sessão
        if sessao_info:
            resumo_ocupacao = obter_resumo_ocupacao_sessao(sessao_info["ID_Sessao"])
            if resumo_ocupacao:
                label_ocupacao.configure(
                    text=f"Disponíveis: {resumo_ocupacao['disponiveis']} / {resumo_ocupacao['total_assentos']}"
                )
        
        # Forçar atualização da interface
        frame_dir.update()

    # ================== CARREGAR DADOS DO BANCO ==================
    def carregar_dados_banco():
        nonlocal filme_info, sala_info, sessao_info, assentos_info
        
        try:
            print("=" * 50)
            print("DEBUG: Iniciando carregamento de dados do banco...")
            
            if not filme_selecionado:
                print("DEBUG: Nenhum filme selecionado")
                return
            
            # Buscar filme no banco
            if "ID_Filme" in filme_selecionado:
                filme_info = buscar_filme_por_id(filme_selecionado["ID_Filme"])
                print(f"DEBUG: Filme encontrado - {filme_info.get('Titulo_Filme') if filme_info else 'Nenhum'}")
            
            # Buscar sessão específica
            tipo_sessao = filme_selecionado.get('tipo_selecionado', 'dublado')
            horario_sessao = filme_selecionado.get('horario_selecionado', '16:00')
            
            print(f"DEBUG: Buscando sessão - Tipo: {tipo_sessao}, Horário: {horario_sessao}")
            
            # Buscar sessões disponíveis para este filme
            sessoes = listar_sessoes_por_filme(filme_selecionado["ID_Filme"])
            
            if sessoes:
                # Encontrar sessão que corresponde ao tipo e horário selecionado
                sessao_encontrada = None
                for sessao in sessoes:
                    if (sessao.get('Tipo_Sessao') == tipo_sessao and 
                        str(sessao.get('Hora_Sessao'))[:5] == horario_sessao):
                        sessao_encontrada = sessao
                        break
                
                if not sessao_encontrada:
                    # Usar a primeira sessão disponível se não encontrar exata
                    sessao_encontrada = sessoes[0]
                    print(f"DEBUG: Sessão exata não encontrada, usando primeira disponível")
                
                sessao_info = sessao_encontrada
                print(f"DEBUG: Sessão encontrada - ID: {sessao_info['ID_Sessao']}")
                
                # Buscar informações da sala
                if "ID_Sala" in sessao_info:
                    sala_info = buscar_sala_por_id(sessao_info["ID_Sala"])
                    print(f"DEBUG: Sala encontrada - {sala_info}")
                
                # Buscar assentos da sessão
                if sessao_info:
                    assentos_info = listar_assentos_por_sessao(sessao_info["ID_Sessao"])
                    print(f"DEBUG: {len(assentos_info)} assentos encontrados para a sessão")
            else:
                print("DEBUG: Nenhuma sessão encontrada, usando dados de teste")
                # Dados de teste
                sessao_info = {"ID_Sessao": 1, "ID_Sala": 1, "Tipo_Sessao": tipo_sessao}
                sala_info = {"ID_Sala": 1, "Nome_Sala": "Sala 1", "Capacidade": 56}
                assentos_info = criar_assentos_teste()
            
            # Atualizar interface
            atualizar_interface()
            criar_grade_assentos()
            
        except Exception as e:
            print(f"Erro ao carregar dados do banco: {e}")
            import traceback
            traceback.print_exc()
            
            # Em caso de erro, usar dados de teste
            print("DEBUG: Usando dados de teste devido a erro")
            filme_info = filme_selecionado
            sessao_info = {"ID_Sessao": 1, "ID_Sala": 1}
            sala_info = {"ID_Sala": 1, "Nome_Sala": "Sala 1", "Capacidade": 56}
            assentos_info = criar_assentos_teste()
            atualizar_interface()
            criar_grade_assentos()

    def criar_assentos_teste():
        """Cria assentos de teste para desenvolvimento"""
        assentos = []
        linhas = ["A", "B", "C", "D", "E", "F", "G"]
        colunas = 8
        
        for i, linha in enumerate(linhas):
            for coluna in range(1, colunas + 1):
                assentos.append({
                    "ID_Assento": i * colunas + coluna,
                    "Linha": linha,
                    "Coluna": coluna,
                    "Status": "disponivel"
                })
        
        # Marcar alguns como ocupados
        assentos[0]["Status"] = "ocupado"  # A1
        assentos[5]["Status"] = "ocupado"  # A6
        assentos[10]["Status"] = "ocupado" # B2
        
        return assentos

    # ================== INTERFACE ==================
    
    # Frame esquerdo - Detalhes do filme
    frame_esq = ctk.CTkFrame(frame, width=320, height=650, fg_color="#F6C148")
    frame_esq.pack(side="left", fill="y", padx=(12,6), pady=12)
    frame_esq.pack_propagate(False)

    ctk.CTkLabel(frame_esq, text="Detalhes do Filme", font=("Arial", 16, "bold"), text_color="black").pack(pady=(8,6))

    # Frame direito - Assentos e resumo
    frame_dir = ctk.CTkFrame(frame, width=2000, height=700)
    frame_dir.pack(side="right", fill="both", padx=(6,12), pady=12)
    frame_dir.pack_propagate(False)

    # Top bar: title left, font controls right
    frame_top_dir = ctk.CTkFrame(frame_dir, fg_color="transparent")
    frame_top_dir.pack(fill="x", pady=(10, 10), padx=12)

    ctk.CTkLabel(frame_top_dir, text="Seleção de Assentos", font=fonte_global if fonte_global else ("Arial", 24, "bold")).pack(side="left")

    # Controles de fonte no canto superior direito (igual ao catálogo/main)
    frame_controle_fonte_top = ctk.CTkFrame(frame_top_dir, fg_color="transparent")
    frame_controle_fonte_top.pack(side="right", padx=6)
    # Usar fonte_global quando disponível para manter consistência visual
    ctk.CTkButton(frame_controle_fonte_top, text="A+", command=aumentar_fonte, width=50, font=fonte_global if fonte_global else None).pack(side="left", padx=5)
    ctk.CTkButton(frame_controle_fonte_top, text="A-", command=diminuir_fonte, width=50, font=fonte_global if fonte_global else None).pack(side="left", padx=5)

    # Container principal
    container_conteudo = ctk.CTkFrame(frame_dir, fg_color="transparent")
    container_conteudo.pack(fill="both", expand=True, pady=10)
    
    # Coluna assentos
    frame_assentos_container = ctk.CTkFrame(container_conteudo, fg_color="transparent")
    frame_assentos_container.pack(side="left", fill="both", expand=True, padx=(0, 15))
    
    frame_assentos = ctk.CTkFrame(frame_assentos_container, fg_color="transparent")
    frame_assentos.pack(fill="both", expand=True)
    
    container_assentos = ctk.CTkFrame(frame_assentos, fg_color="transparent")
    container_assentos.pack(expand=True, pady=20)
    
    # TELA (sempre visível)
    ctk.CTkLabel(container_assentos, text="TELA", font=("Arial", 16, "bold"), 
                fg_color="#2b2b2b", corner_radius=5, width=400, height=30).pack(pady=(0, 30))
    
    # Coluna resumo
    painel_resumo = ctk.CTkFrame(container_conteudo, width=300, fg_color="transparent")
    painel_resumo.pack(side="right", fill="y", padx=(15, 0))
    painel_resumo.pack_propagate(False)
    
    ctk.CTkLabel(painel_resumo, text="Resumo da Compra", font=("Arial", 18, "bold")).pack(pady=20)
    
    info_compra_frame = ctk.CTkFrame(painel_resumo, fg_color="transparent")
    info_compra_frame.pack(fill="x", padx=15, pady=10)
    
    # Labels para informações do filme no resumo
    label_titulo_resumo = ctk.CTkLabel(info_compra_frame, text="", 
                                      font=fonte_global if fonte_global else ("Arial", 14, "bold"), wraplength=250, justify="left")
    label_titulo_resumo.pack(anchor="w")
    
    label_horario_resumo = ctk.CTkLabel(info_compra_frame, text="", 
                                       font=fonte_global if fonte_global else ("Arial", 12), justify="left")
    label_horario_resumo.pack(anchor="w", pady=2)
    
    label_sala_resumo = ctk.CTkLabel(info_compra_frame, text="", 
                                    font=fonte_global if fonte_global else ("Arial", 12), justify="left")
    label_sala_resumo.pack(anchor="w", pady=2)
    
    # Label para ocupação
    label_ocupacao = ctk.CTkLabel(info_compra_frame, text="", 
                                 font=fonte_global if fonte_global else ("Arial", 11), justify="left")
    label_ocupacao.pack(anchor="w", pady=2)
    
    frame_lista = ctk.CTkScrollableFrame(painel_resumo, fg_color="transparent", height=120)
    frame_lista.pack(fill="both", expand=True, padx=15, pady=10)
    
    lista_selecionados = ctk.CTkLabel(frame_lista, text="Nenhum assento selecionado", 
                                     font=fonte_global if fonte_global else ("Arial", 14), justify="left", wraplength=250)
    lista_selecionados.pack(anchor="w")
    
    preco_info_frame = ctk.CTkFrame(painel_resumo, fg_color="transparent")
    preco_info_frame.pack(fill="x", padx=15, pady=10)
    
    ctk.CTkLabel(preco_info_frame, text="Preço por assento: R$ 25,00", font=("Arial", 12)).pack(anchor="w", pady=2)
    
    label_total = ctk.CTkLabel(painel_resumo, text="Total: R$ 0,00", font=fonte_global if fonte_global else ("Arial", 20, "bold"))
    label_total.pack(pady=15)
    
    # Botões
    frame_botoes = ctk.CTkFrame(frame_dir, height=100)
    frame_botoes.pack(side="bottom", fill="x", padx=20, pady=0)

    if voltar_callback:
        btn_voltar = ctk.CTkButton(frame_botoes, text="Voltar", font=("Arial", 14, "bold"), 
                                  width=150, height=40, command=voltar_callback, 
                                  fg_color=BTN_COLOR, hover_color=BTN_HOVER, text_color=BTN_TEXT)
        btn_voltar.pack(side="left", padx=10)

    btn_confirmar = ctk.CTkButton(frame_botoes, text="Confirmar", width=150, height=40, 
                                 font=("Arial", 14, "bold"), command=confirmar, 
                                 fg_color=BTN_COLOR, hover_color=BTN_HOVER, text_color=BTN_TEXT)
    btn_confirmar.pack(side="left", padx=20)

    # (font controls moved to top-right)

    # ================== FUNÇÕES RESTANTES DA INTERFACE ==================
    def atualizar_interface():
        """Atualiza a interface com os dados carregados"""
        print("DEBUG: Atualizando interface...")
        
        # Limpar apenas o conteúdo, não os labels do resumo
        for widget in frame_esq.winfo_children()[1:]:
            widget.destroy()
        
        if filme_info:
            try:
                # Carregar cartaz
                caminho_cartaz = filme_info.get("Cartaz_Path", "")
                if caminho_cartaz and os.path.isfile(caminho_cartaz):
                    img = Image.open(caminho_cartaz).resize((280, 350), Image.LANCZOS)
                    cartaz_img = ctk.CTkImage(img, size=(280, 350))
                    label = ctk.CTkLabel(frame_esq, image=cartaz_img, text="")
                    label.pack(pady=10)
                    label.image = cartaz_img
                else:
                    # Placeholder
                    img = Image.new('RGB', (280, 350), (100, 100, 100))
                    cartaz_img = ctk.CTkImage(img, size=(280, 350))
                    label = ctk.CTkLabel(frame_esq, image=cartaz_img, text="Sem imagem")
                    label.pack(pady=10)
                    label.image = cartaz_img
                
                # Informações do filme
                info_frame = ctk.CTkFrame(frame_esq, fg_color="transparent")
                info_frame.pack(fill="x", padx=10, pady=10)

                titulo = filme_info.get("Titulo_Filme", filme_info.get("titulo", "Filme"))
                ctk.CTkLabel(info_frame, text=titulo, 
                            font=("Arial", 16, "bold"), wraplength=280, text_color="black").pack(pady=5)
                
                genero = filme_info.get('Genero', filme_info.get('genero', ''))
                ctk.CTkLabel(info_frame, text=f"Gênero: {genero}", 
                            font=("Arial", 12), wraplength=280, text_color="black").pack(pady=2)
                
                duracao = filme_info.get('Duracao', filme_info.get('duracao', ''))
                ctk.CTkLabel(info_frame, text=f"Duração: {duracao}", 
                            font=("Arial", 12), text_color="black").pack(pady=2)

                # Informações da sessão
                sessao_frame = ctk.CTkFrame(frame_esq, fg_color="transparent")
                sessao_frame.pack(fill="x", padx=10, pady=10)
                
                if sessao_info:
                    tipo = sessao_info.get('Tipo_Sessao', '').capitalize()
                    horario = str(sessao_info.get('Hora_Sessao', ''))[:5]
                    ctk.CTkLabel(sessao_frame, text=f"Tipo: {tipo}", 
                                font=("Arial", 12), text_color="black").pack(pady=2)
                    ctk.CTkLabel(sessao_frame, text=f"Horário: {horario}", 
                                font=("Arial", 12), text_color="black").pack(pady=2)
                
                if sala_info:
                    ctk.CTkLabel(sessao_frame, text=f"Sala: {sala_info.get('Nome_Sala', '')}", 
                                font=("Arial", 12), text_color="black").pack(pady=2)

                # Atualizar resumo
                titulo = filme_info.get("Titulo_Filme", filme_info.get("titulo", "Filme"))
                label_titulo_resumo.configure(text=titulo)
                
                if sessao_info:
                    horario = str(sessao_info.get('Hora_Sessao', ''))[:5]
                    label_horario_resumo.configure(text=f"Horário: {horario}")
                else:
                    label_horario_resumo.configure(text="")
                
                if sala_info:
                    sala_nome = sala_info.get('Nome_Sala', '')
                    label_sala_resumo.configure(text=f"Sala: {sala_nome}")
                else:
                    label_sala_resumo.configure(text="")
                
                print("DEBUG: Interface atualizada com sucesso")
                
            except Exception as e:
                print(f"Erro ao atualizar interface: {e}")
                ctk.CTkLabel(frame_esq, text="Erro ao carregar informações", 
                            font=("Arial", 14), text_color="black").pack(pady=50)
        else:
            ctk.CTkLabel(frame_esq, text="Nenhum filme selecionado", 
                        font=("Arial", 14), text_color="black").pack(pady=50)
            
            # Limpar resumo
            label_titulo_resumo.configure(text="Nenhum filme selecionado")
            label_horario_resumo.configure(text="")
            label_sala_resumo.configure(text="")

    def criar_grade_assentos():
        """Cria a grade de assentos"""
        nonlocal assentos, selecionados
        assentos = {}
        selecionados = []
        
        # Limpar grade (exceto TELA)
        for widget in container_assentos.winfo_children()[1:]:
            widget.destroy()
        
        if assentos_info:
            # Agrupar por linha
            linhas = {}
            for assento in assentos_info:
                linha = assento["Linha"]
                if linha not in linhas:
                    linhas[linha] = []
                linhas[linha].append(assento)
            
            # Criar grade
            for linha in sorted(linhas.keys()):
                linha_frame = ctk.CTkFrame(container_assentos, fg_color="transparent")
                linha_frame.pack(pady=3)
                
                for assento in sorted(linhas[linha], key=lambda x: x["Coluna"]):
                    codigo = f"{assento['Linha']}{assento['Coluna']}"
                    status = assento["Status"]
                    
                    cor = COR_OCUPADO if status == "ocupado" else COR_LIVRE
                    estado = "disabled" if status == "ocupado" else "normal"
                    
                    # Criar botão com ícone
                    botao = ctk.CTkButton(
                        linha_frame, 
                        text=codigo, 
                        width=70, 
                        height=70, 
                        fg_color=cor, 
                        text_color="black", 
                        font=fonte_global if fonte_global else ("Arial", current_font_size, "bold"), 
                        corner_radius=8,
                        state=estado,
                        image=seat_icon,  # Adiciona o ícone aqui
                        compound="top",   # Ícone acima do texto
                        command=lambda c=codigo, id=assento["ID_Assento"]: toggle_assento(c, id)
                    )
                    botao.pack(side="left", padx=2)
                    # Armazenar também o ID_Assento_Sessao para uso posterior
                    assentos[codigo] = (
                        botao,
                        "ocupado" if status == "ocupado" else "livre",
                        assento.get("ID_Assento"),
                        assento.get("ID_Assento_Sessao")
                    )
            
            print(f"DEBUG: Grade criada com {len(assentos)} assentos")
        else:
            ctk.CTkLabel(container_assentos, text="Nenhum assento disponível", 
                        font=("Arial", 14), text_color="white").pack(pady=20)
        
        criar_legenda()
        atualizar_resumo()

    def criar_legenda():
        """Cria a legenda"""
        frame_legenda = ctk.CTkFrame(container_assentos, fg_color="#2b2b2b", 
                                    border_width=2, border_color="#444444", corner_radius=12)
        frame_legenda.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(frame_legenda, text="Legenda dos Assentos", 
                font=("Arial", 14, "bold"), text_color="white").pack(pady=(10, 8))
        
        legenda_frame = ctk.CTkFrame(frame_legenda, fg_color="transparent")
        legenda_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Disponível
        item1 = ctk.CTkFrame(legenda_frame, fg_color="transparent")
        item1.pack(side="left", expand=True, padx=10)
        ctk.CTkLabel(item1, text="●", font=("Arial", 20), text_color=COR_LIVRE).pack(side="left", padx=(0, 5))
        ctk.CTkLabel(item1, text="Disponível", font=("Arial", 12), text_color="white").pack(side="left")
        
        # Selecionado
        item2 = ctk.CTkFrame(legenda_frame, fg_color="transparent")
        item2.pack(side="left", expand=True, padx=10)
        ctk.CTkLabel(item2, text="●", font=("Arial", 20), text_color=COR_SELECIONADO).pack(side="left", padx=(0, 5))
        ctk.CTkLabel(item2, text="Selecionado", font=("Arial", 12), text_color="white").pack(side="left")
        
        # Ocupado
        item3 = ctk.CTkFrame(legenda_frame, fg_color="transparent")
        item3.pack(side="left", expand=True, padx=10)
        ctk.CTkLabel(item3, text="●", font=("Arial", 20), text_color=COR_OCUPADO).pack(side="left", padx=(0, 5))
        ctk.CTkLabel(item3, text="Ocupado", font=("Arial", 12), text_color="white").pack(side="left")

    # ================== INICIALIZAÇÃO ==================
    # Carregar ícone, dados e aplicar fonte inicial
    frame.after(100, lambda: [carregar_icone_assento(), carregar_dados_banco(), aplicar_fonte_local()])
    
    return frame