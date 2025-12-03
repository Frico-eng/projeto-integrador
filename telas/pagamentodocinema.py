import sys
import os
import threading
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import qrcode
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from utilidades.config import *
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import A5, portrait
from reportlab.pdfgen import canvas
import shutil
from crud.crud_ingressos import inserir_ingresso, verificar_ingresso_existente

# Definir diretórios
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "utilidades", "images")

# ================== CONSTANTES DE CORES ==================
COR_FUNDO = "#1C1C1C"  # Cinza escuro igual tela de assentos
COR_TEXTO = "#ECF0F1"   # Texto claro
COR_DESTAQUE = "#F6C148" # Amarelo/laranja para destaque
COR_BOTAO = "#F6C148"
COR_BOTAO_HOVER = "#E2952D"
COR_TEXTO_BOTAO = "#1C2732"

# === FUNÇÃO PARA GERAR COMPROVANTE PDF ===
# === FUNÇÃO PARA GERAR COMPROVANTE PDF COM QR CODE ===
def gerar_comprovante(filme, horario, assentos, preco_por_assento=25.00, logo_path="logo.png"):
    total = len(assentos) * preco_por_assento
    nome_arquivo = f"Comprovante_{filme.replace(' ', '_')}_{datetime.now().strftime('%H%M%S')}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=portrait(A5))
    
    # Dimensões da página A5 em portrait
    largura, altura = portrait(A5)
    
    # === GERAR QR CODE ===
    try:
        # Conteúdo do QR Code
        conteudo_qr = (
            f"CINEPLUS - COMPROVANTE\n"
            f"Filme: {filme}\n"
            f"Horário: {horario}\n"
            f"Assentos: {', '.join(assentos)}\n"
            f"Quantidade: {len(assentos)}\n"
            f"Total: R$ {total:.2f}\n"
            f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
            f"ID: {datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        
        # Gerar QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(conteudo_qr)
        qr.make(fit=True)
        
        # Criar imagem do QR Code
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Salvar temporariamente
        qr_temp_path = f"temp_qr_{datetime.now().strftime('%H%M%S')}.png"
        qr_img.save(qr_temp_path)
        
    except Exception as e:
        print(f"Erro ao gerar QR Code: {e}")
        qr_temp_path = None
    
    # === LOGO DO CINEPLUS ===
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 70, 420, width=80, height=80, mask='auto')
    
    # === QR CODE (lado direito) ===
    if qr_temp_path and os.path.exists(qr_temp_path):
        c.drawImage(qr_temp_path, 165, 180, width=100, height=100, mask='auto')
        # Remover arquivo temporário após uso
        try:
            os.remove(qr_temp_path)
        except:
            pass
    
    # === TÍTULO DO CINEMA ===
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(largura/2, 550, "🎬 CinePlus - Comprovante de Ingresso 🎬")
    c.line(10, 530, largura-10, 530)
    
    # === LINHA DE CÓDIGO ===
    c.setFont("Helvetica", 10)
    codigo = f"REF: {datetime.now().strftime('%Y%m%d%H%M%S')}"
    c.drawCentredString(largura/2, 510, codigo)
    
    # === DADOS DO FILME ===
    c.setFont("Helvetica", 14)
    
    # Filme (com quebra de linha se necessário)
    filme_texto = f"Filme: {filme}"
    if len(filme_texto) > 40:
        c.setFont("Helvetica", 12)
    c.drawCentredString(largura/2, 480, filme_texto)
    c.setFont("Helvetica", 14)
    
    c.drawCentredString(largura/2, 455, f"Horário: {horario}")
    
    # Assentos (com tratamento para muitos assentos)
    assentos_texto = f"Assentos: {', '.join(assentos)}"
    if len(assentos_texto) > 50:
        c.setFont("Helvetica", 12)
        # Dividir em duas linhas se necessário
        if len(assentos_texto) > 100:
            metade = len(assentos) // 2
            linha1 = ', '.join(assentos[:metade])
            linha2 = ', '.join(assentos[metade:])
            c.drawCentredString(largura/2, 430, f"Assentos: {linha1}")
            c.drawCentredString(largura/2, 410, linha2)
        else:
            c.drawCentredString(largura/2, 430, assentos_texto)
        c.setFont("Helvetica", 14)
    else:
        c.drawCentredString(largura/2, 430, assentos_texto)
    
    y_pos = 400 if len(assentos_texto) <= 50 else 390
    
    c.drawCentredString(largura/2, y_pos, f"Preço por assento: R$ {preco_por_assento:.2f}")
    c.drawCentredString(largura/2, y_pos-25, f"Total: R$ {total:.2f}")
    
    data_compra = datetime.now().strftime('%d/%m/%Y %H:%M')
    c.drawCentredString(largura/2, y_pos-50, f"Data da compra: {data_compra}")
    
    # === RODAPÉ COM INFORMAÇÕES DO QR CODE ===
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(largura/2, 280, "Use o QR Code para validação rápida na entrada")
    
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(largura/2, 120, "Apresente este comprovante na entrada da sessão.")
    c.drawCentredString(largura/2, 100, "Agradecemos sua preferência! Bom filme! 🍿")
    
    # === INFORMAÇÕES ADICIONAIS ===
    c.setFont("Helvetica", 9)
    c.drawCentredString(largura/2, 70, "Em caso de dúvidas, entre em contato: (11) 9999-9999")
    c.drawCentredString(largura/2, 55, "cinema@cineplus.com")
    
    # === LINHA DE SEGURANÇA ===
    c.setFont("Helvetica", 8)
    seguranca = "Documento válido apenas para a sessão e data especificadas"
    c.drawCentredString(largura/2, 35, seguranca)
    
    c.save()
    return nome_arquivo
# === FUNÇÃO PARA GERAR IMAGEM DO COMPROVANTE ===
def gerar_imagem_comprovante(filme, horario, assentos, preco_por_assento=25.00, tamanho=(400, 280)):
    try:
        total = len(assentos) * preco_por_assento
        
        # Criar uma imagem em branco
        largura, altura = tamanho
        img = Image.new('RGB', (largura, altura), color='#FFFFFF')
        draw = ImageDraw.Draw(img)
        
        # Tentar carregar fontes
        try:
            # Tentar fontes comuns do Windows
            font_paths = [
                "arial.ttf",
                "C:/Windows/Fonts/arial.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                "/System/Library/Fonts/Helvetica.ttc"
            ]
            
            font_titulo = None
            for path in font_paths:
                try:
                    font_titulo = ImageFont.truetype(path, 18)
                    break
                except:
                    continue
            
            if font_titulo is None:
                font_titulo = ImageFont.load_default()
                
            font_normal = ImageFont.truetype("arial.ttf", 14) if os.path.exists("arial.ttf") else ImageFont.load_default()
            font_pequena = ImageFont.truetype("arial.ttf", 11) if os.path.exists("arial.ttf") else ImageFont.load_default()
            
        except:
            # Usar fonte padrão se não encontrar outras
            font_titulo = ImageFont.load_default()
            font_normal = ImageFont.load_default()
            font_pequena = ImageFont.load_default()
        
        # Cores
        cor_titulo = "#000000"
        cor_texto = "#333333"
        cor_destaque = "#F6C148"
        cor_fundo = "#F8F8F8"
        cor_sucesso = "#27AE60"
        
        # Desenhar fundo com bordas arredondadas
        draw.rectangle([(0, 0), (largura, altura)], fill=cor_fundo, outline="#DDDDDD", width=2)
        
        # Cabeçalho com cor de destaque
        draw.rectangle([(0, 0), (largura, 50)], fill=cor_destaque)
        
        # Título centralizado
        titulo_texto = "🎬 CinePlus - Comprovante 🎬"
        bbox = draw.textbbox((0, 0), titulo_texto, font=font_titulo)
        text_width = bbox[2] - bbox[0]
        text_x = (largura - text_width) // 2
        draw.text((text_x, 25), titulo_texto, fill=cor_titulo, font=font_titulo, anchor="mm")
        
        # Informações da compra
        y_pos = 70
        espacamento = 28
        
        # Filme (pode ser truncado se muito longo)
        filme_display = filme[:25] + "..." if len(filme) > 25 else filme
        draw.text((20, y_pos), "🎬 Filme:", fill="#000000", font=font_normal)
        draw.text((120, y_pos), f"{filme_display}", fill=cor_texto, font=font_normal)
        y_pos += espacamento
        
        # Horário
        draw.text((20, y_pos), "🕒 Horário:", fill="#000000", font=font_normal)
        draw.text((120, y_pos), f"{horario}", fill=cor_texto, font=font_normal)
        y_pos += espacamento
        
        # Assentos (pode ser truncado se muitos)
        assentos_texto = ', '.join(assentos)
        if len(assentos_texto) > 20:
            assentos_texto = assentos_texto[:20] + "..."
        draw.text((20, y_pos), "💺 Assentos:", fill="#000000", font=font_normal)
        draw.text((120, y_pos), f"{assentos_texto}", fill=cor_texto, font=font_normal)
        y_pos += espacamento
        
        # Preço unitário
        draw.text((20, y_pos), "💰 Unitário:", fill="#000000", font=font_normal)
        draw.text((120, y_pos), f"R$ {preco_por_assento:.2f}", fill=cor_texto, font=font_normal)
        y_pos += espacamento
        
        # Total (em destaque)
        draw.text((20, y_pos), "💵 Total:", fill="#000000", font=font_normal)
        draw.text((120, y_pos), f"R$ {total:.2f}", fill=cor_sucesso, font=font_normal)
        y_pos += espacamento + 10
        
        # Linha divisória
        draw.line([(20, y_pos), (largura-20, y_pos)], fill="#CCCCCC", width=2)
        y_pos += 20
        
        # Data da compra
        data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
        draw.text((largura//2, y_pos), f"📅 {data_atual}", 
                 fill="#666666", font=font_pequena, anchor="mm")
        y_pos += 25
        
        # Rodapé
        draw.text((largura//2, altura-25), "Apresente este QR Code na entrada", 
                 fill="#666666", font=font_pequena, anchor="mm")
        
        # Converter para CTkImage
        imagem_ctk = ctk.CTkImage(img, size=tamanho)
        return imagem_ctk
        
    except Exception as e:
        print(f"Erro ao gerar imagem do comprovante: {e}")
        # Retornar uma imagem de fallback simples
        img_fallback = Image.new('RGB', tamanho, color='#F8F8F8')
        draw = ImageDraw.Draw(img_fallback)
        draw.rectangle([(0, 0), (largura, altura)], outline="#DDDDDD", width=2)
        
        # Texto de fallback
        bbox = draw.textbbox((0, 0), "Comprovante Gerado", font=ImageFont.load_default())
        text_width = bbox[2] - bbox[0]
        text_x = (largura - text_width) // 2
        text_y = altura // 2
        
        draw.text((text_x, text_y), "Comprovante Gerado", 
                 fill="#666666", font=ImageFont.load_default(), anchor="mm")
        
        return ctk.CTkImage(img_fallback, size=tamanho)

# === FUNÇÃO PARA VISUALIZAR COMPROVANTE EM TELA CHEIA ===
def visualizar_comprovante_tela_cheia(parent, caminho_pdf, dados_compra):
    """
    Abre uma janela modal para visualizar o comprovante
    
    Args:
        parent: Janela/Frame pai
        caminho_pdf: Caminho do arquivo PDF
        dados_compra: Dados da compra para recriar visualização
    """
    # Criar janela modal
    janela_pdf = ctk.CTkToplevel(parent)
    janela_pdf.title("Visualizar Comprovante")
    janela_pdf.geometry("900x700")
    janela_pdf.resizable(True, True)
    janela_pdf.transient(parent)
    janela_pdf.grab_set()
    
    # Centralizar na tela
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()
    
    janela_width = 900
    janela_height = 700
    
    x = parent_x + (parent_width - janela_width) // 2
    y = parent_y + (parent_height - janela_height) // 2
    
    janela_pdf.geometry(f"{janela_width}x{janela_height}+{x}+{y}")
    
    # Configurar layout
    janela_pdf.configure(fg_color=COR_FUNDO)
    
    # Frame principal
    frame_principal = ctk.CTkFrame(janela_pdf, fg_color=COR_FUNDO)
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
    ctk.CTkLabel(
        frame_principal,
        text="📄 Comprovante de Compra - CinePlus",
        font=("Arial", 24, "bold"),
        text_color=COR_DESTAQUE
    ).pack(pady=(0, 20))
    
    # Frame para conteúdo do comprovante
    frame_comprovante = ctk.CTkFrame(frame_principal, fg_color="#FFFFFF", corner_radius=15)
    frame_comprovante.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Criar uma visualização detalhada do comprovante
    try:
        # Extrair dados da compra
        filme = dados_compra.get("filme", {}).get("Titulo_Filme", "Filme não especificado")
        horario = dados_compra.get("sessao", {}).get("Hora_Sessao", "Horário não especificado")
        assentos = dados_compra.get("assentos", [])
        preco = dados_compra.get("preco_unitario", 25.00)
        total = dados_compra.get("total", len(assentos) * preco)
        
        # Formatar horário
        if isinstance(horario, datetime):
            horario_texto = horario.strftime('%H:%M')
        else:
            horario_texto = str(horario)
        
        # Gerar imagem maior do comprovante
        imagem_comprovante = gerar_imagem_comprovante(
            filme, 
            horario_texto, 
            assentos, 
            preco, 
            tamanho=(800, 500)
        )
        
        # Exibir imagem
        label_imagem = ctk.CTkLabel(
            frame_comprovante, 
            image=imagem_comprovante,
            text="",
            fg_color="#FFFFFF"
        )
        label_imagem.image = imagem_comprovante
        label_imagem.pack(pady=20, padx=20)
        
    except Exception as e:
        print(f"Erro ao criar visualização: {e}")
        ctk.CTkLabel(
            frame_comprovante,
            text="✅ Comprovante Gerado com Sucesso!",
            font=("Arial", 18, "bold"),
            text_color="#27AE60",
            fg_color="#FFFFFF"
        ).pack(pady=50)
        
        ctk.CTkLabel(
            frame_comprovante,
            text=f"Arquivo: {os.path.basename(caminho_pdf)}",
            font=("Arial", 14),
            text_color="#333333",
            fg_color="#FFFFFF"
        ).pack(pady=10)
    
    # Informações do arquivo
    info_frame = ctk.CTkFrame(frame_principal, fg_color="transparent")
    info_frame.pack(fill="x", pady=(15, 10))
    
    ctk.CTkLabel(
        info_frame,
        text=f"📁 Arquivo salvo em: {os.path.abspath(caminho_pdf)}",
        font=("Arial", 12),
        text_color=COR_TEXTO,
        wraplength=800
    ).pack(pady=5)
    
    ctk.CTkLabel(
        info_frame,
        text="💡 Dica: Salve ou imprima este comprovante para apresentar na entrada do cinema",
        font=("Arial", 11, "italic"),
        text_color="#95a5a6"
    ).pack(pady=5)
    
    # Frame para botões
    frame_botoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_botoes.pack(pady=20)
    
    def abrir_pdf_externo():
        """Abre o PDF no visualizador padrão do sistema"""
        try:
            if os.path.exists(caminho_pdf):
                if sys.platform == "win32":
                    os.startfile(caminho_pdf)
                elif sys.platform == "darwin":  # macOS
                    os.system(f"open '{caminho_pdf}'")
                else:  # Linux
                    os.system(f"xdg-open '{caminho_pdf}'")
            else:
                messagebox.showwarning("Atenção", f"Arquivo não encontrado:\n{caminho_pdf}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o PDF:\n{str(e)}")
    
    def salvar_como():
        """Permite ao usuário escolher onde salvar o PDF"""
        arquivo_destino = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=os.path.basename(caminho_pdf)
        )
        
        if arquivo_destino:
            try:
                shutil.copy2(caminho_pdf, arquivo_destino)
                messagebox.showinfo("Sucesso", f"✅ PDF salvo em:\n{arquivo_destino}")
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao salvar arquivo:\n{str(e)}")
    
    def imprimir_comprovante():
        """Opção para imprimir o comprovante"""
        try:
            if os.path.exists(caminho_pdf):
                resposta = messagebox.askyesno(
                    "Imprimir", 
                    f"Deseja imprimir o comprovante?\n\n"
                    f"O arquivo será aberto no visualizador padrão de PDF,\n"
                    f"onde você pode usar a opção de impressão."
                )
                
                if resposta:
                    abrir_pdf_externo()
            else:
                messagebox.showwarning("Atenção", "Arquivo PDF não encontrado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao imprimir:\n{str(e)}")
    
    def enviar_por_email():
        """Simula envio por email"""
        messagebox.showinfo(
            "Enviar por Email", 
            "Funcionalidade de email será implementada em breve.\n\n"
            "Por enquanto, use a opção 'Salvar Como' para guardar seu comprovante."
        )
    
    # Botões em linha
    ctk.CTkButton(
        frame_botoes,
        text="🔓 Abrir PDF",
        command=abrir_pdf_externo,
        font=("Arial", 14),
        fg_color="#3498db",
        hover_color="#2980b9",
        width=140,
        height=40
    ).pack(side="left", padx=5)
    
    ctk.CTkButton(
        frame_botoes,
        text="💾 Salvar Como",
        command=salvar_como,
        font=("Arial", 14),
        fg_color="#27ae60",
        hover_color="#219653",
        width=140,
        height=40
    ).pack(side="left", padx=5)
    
    ctk.CTkButton(
        frame_botoes,
        text="🖨️ Imprimir",
        command=imprimir_comprovante,
        font=("Arial", 14),
        fg_color="#9b59b6",
        hover_color="#8e44ad",
        width=120,
        height=40
    ).pack(side="left", padx=5)
    
    ctk.CTkButton(
        frame_botoes,
        text="📧 Enviar Email",
        command=enviar_por_email,
        font=("Arial", 14),
        fg_color="#e67e22",
        hover_color="#d35400",
        width=140,
        height=40
    ).pack(side="left", padx=5)
    
    ctk.CTkButton(
        frame_botoes,
        text="✖️ Fechar",
        command=janela_pdf.destroy,
        font=("Arial", 14),
        fg_color="#7f8c8d",
        hover_color="#6c7a7d",
        width=100,
        height=40
    ).pack(side="left", padx=5)

# === FUNÇÃO PARA INSERIR INGRESSOS NO BANCO ===
def inserir_ingressos_no_banco(dados_compra):
    """
    Insere os ingressos no banco de dados usando a função inserir_ingresso
    
    Args:
        dados_compra: dicionário com todas as informações da compra
        
    Returns:
        tuple: (sucesso, lista_ids_ingressos) ou (False, mensagem_erro)
    """
    try:
        print("DEBUG: Iniciando inserção de ingressos no banco...")
        
        # Extrair informações necessárias
        sessao_obj = dados_compra.get("sessao", {})
        assentos = dados_compra.get("assentos", [])
        preco_unit = dados_compra.get("preco_unitario", 25.00)
        
        # IDs essenciais
        id_sessao = sessao_obj.get("ID_Sessao")
        id_cliente = 1  # TODO: Substituir pelo ID do cliente logado
        
        if not id_sessao:
            return False, "ID da sessão não encontrado"
        
        if not assentos:
            return False, "Nenhum assento selecionado"
        
        print(f"DEBUG: Inserindo ingressos para sessão {id_sessao}, cliente {id_cliente}")
        print(f"DEBUG: Assentos: {assentos}")
        
        # Buscar IDs dos assentos_sessao
        from crud.crud_assento_sessao import listar_assentos_por_sessao
        
        assentos_sessao = listar_assentos_por_sessao(id_sessao)
        print(f"DEBUG: {len(assentos_sessao)} assentos encontrados na sessão")
        
        # Mapear código do assento para ID_Assento_Sessao
        mapa_assentos = {}
        for assento in assentos_sessao:
            codigo = f"{assento['Linha']}{assento['Coluna']}"
            mapa_assentos[codigo] = assento['ID_Assento_Sessao']
        
        print(f"DEBUG: Mapa de assentos: {mapa_assentos}")
        
        # Lista para armazenar confirmações
        ingressos_inseridos = []
        assentos_nao_encontrados = []
        
        for codigo_assento in assentos:
            id_assento_sessao = mapa_assentos.get(codigo_assento)
            
            if id_assento_sessao:
                # Verificar se o ingresso já existe
                if not verificar_ingresso_existente(id_sessao, id_assento_sessao):
                    # Inserir cada ingresso individualmente
                    sucesso = inserir_ingresso(id_sessao, id_cliente, id_assento_sessao, preco_unit)
                    
                    if sucesso:
                        print(f"DEBUG: Ingresso inserido para assento {codigo_assento}")
                        ingressos_inseridos.append(codigo_assento)
                    else:
                        print(f"ERRO: Falha ao inserir ingresso para assento {codigo_assento}")
                        return False, f"Falha ao reservar assento {codigo_assento}"
                else:
                    print(f"AVISO: Ingresso já existe para assento {codigo_assento}")
                    return False, f"Assento {codigo_assento} já possui ingresso vendido"
            else:
                assentos_nao_encontrados.append(codigo_assento)
                print(f"ERRO: Assento {codigo_assento} não encontrado na sessão")
        
        if assentos_nao_encontrados:
            return False, f"Assentos não encontrados: {', '.join(assentos_nao_encontrados)}"
        
        if not ingressos_inseridos:
            return False, "Nenhum ingresso válido para inserir"
        
        print(f"DEBUG: {len(ingressos_inseridos)} ingressos inseridos com sucesso!")
        return True, ingressos_inseridos
            
    except Exception as e:
        print(f"ERRO: Exceção ao inserir ingressos: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Erro interno: {str(e)}"

# === FUNÇÃO PRINCIPAL PARA MOSTRAR CONFIRMAÇÃO DE PAGAMENTO ===
def mostrar_confirmacao_pagamento(parent, dados_compra=None, finalizar_callback=None):
    """
    Mostra a tela de confirmação de pagamento dentro de um frame existente
    
    Args:
        parent: CTkFrame onde o conteúdo será exibido
        dados_compra: dicionário com todas as informações da compra
        finalizar_callback: função a ser chamada ao finalizar
    """
    # Limpar frame pai
    for widget in parent.winfo_children():
        widget.destroy()

    # ====== VALIDAÇÃO DOS DADOS ======
    if not dados_compra:
        print("ERRO: Nenhum dado de compra fornecido!")
        # Criar dados padrão para evitar erro
        dados_compra = {
            'filme': {'Titulo_Filme': 'Filme não especificado'},
            'sessao': {'horario_selecionado': 'Horário não especificado'},
            'assentos': [],
            'quantidade': 0,
            'preco_unitario': 25.00,
            'total': 0
        }

    # ====== EXTRAIR INFORMAÇÕES DO DADOS_COMPRA ======
    filme_obj = dados_compra.get("filme", {})
    sessao_obj = dados_compra.get("sessao", {})
    
    # Obter título do filme
    titulo_filme = filme_obj.get("Titulo_Filme") or filme_obj.get("titulo") or "Filme não especificado"
    
    # Extrair horário de forma robusta
    horario = "Horário não especificado"
    
    # Tentar extrair horário da sessão
    if sessao_obj:
        if sessao_obj.get('Hora_Sessao'):
            horario = str(sessao_obj['Hora_Sessao'])[:5]  # Formata para HH:MM
        elif sessao_obj.get('horario_selecionado'):
            horario = sessao_obj['horario_selecionado']
    
    # Se não encontrou na sessão, tentar no filme
    if horario == "Horário não especificado" and filme_obj.get('horario_selecionado'):
        horario = filme_obj['horario_selecionado']
    
    # Obter informações da sala se disponível
    sala_obj = dados_compra.get("sala", {})
    nome_sala = sala_obj.get("Nome_Sala", "")
    
    assentos = dados_compra.get("assentos", [])
    qtd_ingressos = dados_compra.get("quantidade", len(assentos))
    preco_unit = dados_compra.get("preco_unitario", 25.00)
    total = dados_compra.get("total", qtd_ingressos * preco_unit)

    print(f"DEBUG: Dados extraídos para pagamento:")
    print(f"  - Título: {titulo_filme}")
    print(f"  - Horário: {horario}")
    print(f"  - Sala: {nome_sala}")
    print(f"  - Assentos: {assentos}")
    print(f"  - Quantidade: {qtd_ingressos}")
    print(f"  - Preço unitário: R$ {preco_unit:.2f}")
    print(f"  - Total: R$ {total:.2f}")
    
    # Variável para armazenar o caminho do PDF gerado
    pdf_gerado = None

    # ====== CONFIGURAR FRAME PRINCIPAL ======
    frame = ctk.CTkFrame(parent, fg_color=COR_FUNDO, width=1800, height=900)
    frame.pack_propagate(False)
    frame.pack(fill="both", expand=True)

    # ====== IMAGEM DE FUNDO ======
    caixa_path = os.path.join(IMAGE_DIR, "caixa.png")
    
    try:
        bg_image = Image.open(caixa_path)
        bg_photo = ctk.CTkImage(bg_image, size=(1800, 900))
        
        bg_label = ctk.CTkLabel(frame, image=bg_photo, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_photo
        
    except Exception as e:
        print(f"Erro ao carregar imagem de fundo: {e}")
        # Já temos COR_FUNDO como fallback

    # ====== CONTAINER PRINCIPAL PARA CONTEÚDO ======
    container_principal = ctk.CTkFrame(
        frame, 
        fg_color="#2b2b2b",
        bg_color="transparent",
        corner_radius=15,
        width=1100,  # Aumentado para caber mais conteúdo
        height=800
    )
    container_principal.place(relx=0.5, rely=0.5, anchor="center")
    container_principal.pack_propagate(False)

    # ====== CABEÇALHO ======
    header_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    header_frame.pack(fill="x", pady=(30, 20), padx=40)

    ctk.CTkLabel(
        header_frame,
        text="✅ Pagamento Confirmado!",
        font=("Arial", 28, "bold"),
        text_color="#27AE60"
    ).pack(pady=10)

    ctk.CTkLabel(
        header_frame,
        text="Seu ingresso foi reservado com sucesso",
        font=("Arial", 18),
        text_color=COR_TEXTO
    ).pack()

    # ====== CONTEÚDO PRINCIPAL ======
    content_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)

    # ====== LADO ESQUERDO: INFORMAÇÕES ======
    info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    info_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

    # Informações da compra
    ctk.CTkLabel(
        info_frame,
        text="📋 Detalhes da Compra",
        font=("Arial", 20, "bold"),
        text_color=COR_DESTAQUE
    ).pack(anchor="w", pady=(0, 20))

    # Construir lista de informações
    informacoes = [
        ("🎬 Filme:", titulo_filme),
        ("🕒 Horário:", horario),
        ("🎫 Quantidade:", f"{qtd_ingressos} ingressos"),
        ("💰 Preço unitário:", f"R$ {preco_unit:.2f}"),
        ("💵 Total:", f"R$ {total:.2f}")
    ]

    # Adicionar sala se disponível
    if nome_sala:
        informacoes.insert(2, ("🎪 Sala:", nome_sala))

    # Adicionar assentos se disponível
    if assentos:
        informacoes.insert(3 if nome_sala else 2, ("💺 Assentos:", ", ".join(assentos)))

    for label, valor in informacoes:
        linha_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        linha_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            linha_frame, 
            text=label, 
            font=("Arial", 16, "bold"),
            text_color=COR_TEXTO, 
            width=180, 
            anchor="w"
        ).pack(side="left")

        ctk.CTkLabel(
            linha_frame, 
            text=valor, 
            font=("Arial", 16),
            text_color=COR_TEXTO, 
            anchor="w",
            wraplength=400
        ).pack(side="left", fill="x", expand=True)

    # Espaçamento
    ctk.CTkLabel(info_frame, text="", height=30).pack()

    # Instruções
    ctk.CTkLabel(
        info_frame,
        text="📱 Apresente o QR Code na entrada do cinema",
        font=("Arial", 16, "bold"),
        text_color=COR_DESTAQUE,
        justify="left",
        wraplength=400
    ).pack(anchor="w", pady=10)

    ctk.CTkLabel(
        info_frame,
        text="💡 Clique em 'Finalizar Compra' para gerar seu comprovante",
        font=("Arial", 14),
        text_color="#95a5a6",
        justify="left",
        wraplength=400
    ).pack(anchor="w", pady=5)

    # ====== LADO DIREITO: QR CODE E MINIATURA COMPROVANTE ======
    lado_direito_frame = ctk.CTkFrame(content_frame, fg_color="transparent", width=400)
    lado_direito_frame.pack(side="right", fill="y", padx=(20, 0))
    lado_direito_frame.pack_propagate(False)

    # Frame para QR Code
    qr_frame = ctk.CTkFrame(lado_direito_frame, fg_color="transparent")
    qr_frame.pack(fill="x", pady=(0, 20))

    # Gerar QR Code
    conteudo = (
        f"CINEPLUS COMPRA\n"
        f"Filme: {titulo_filme}\n"
        f"Horário: {horario}\n"
        f"Sala: {nome_sala}\n"
        f"Assentos: {', '.join(assentos)}\n"
        f"Qtd: {qtd_ingressos}\n"
        f"Total: R$ {total:.2f}\n"
        f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    try:
        qr_img = qrcode.make(conteudo)
        qr_img_path = "temp_qr_code.png"
        qr_img.save(qr_img_path)

        img = Image.open(qr_img_path).resize((280, 280))
        qr_photo = ctk.CTkImage(img, size=(280, 280))
        
        qr_label = ctk.CTkLabel(qr_frame, image=qr_photo, text="")
        qr_label.image = qr_photo
        qr_label.pack()

        ctk.CTkLabel(
            qr_frame,
            text="QR Code do Ingresso",
            font=("Arial", 16, "bold"),
            text_color=COR_TEXTO
        ).pack(pady=5)

    except Exception as e:
        print(f"Erro ao carregar QR code: {e}")
        ctk.CTkLabel(
            qr_frame,
            text="Erro ao gerar QR Code",
            font=("Arial", 14),
            text_color="#e74c3c"
        ).pack(pady=20)

    # Frame para visualização do comprovante (miniatura)
    pdf_frame = ctk.CTkFrame(lado_direito_frame, fg_color="#1a1a1a", corner_radius=10)
    pdf_frame.pack(fill="both", expand=True)

    ctk.CTkLabel(
        pdf_frame,
        text="📄 Comprovante",
        font=("Arial", 16, "bold"),
        text_color=COR_DESTAQUE
    ).pack(pady=15)

    # Placeholder para miniatura do comprovante
    pdf_miniatura_label = ctk.CTkLabel(
        pdf_frame,
        text="O comprovante será gerado após finalizar a compra",
        font=("Arial", 12, "italic"),
        text_color="#95a5a6",
        wraplength=350,
        height=180
    )
    pdf_miniatura_label.pack(expand=True, pady=10, padx=10)

    # Função para atualizar a miniatura do comprovante
    def atualizar_miniatura_comprovante():
        """Atualiza a miniatura do comprovante na tela"""
        # Extrair dados para gerar a imagem
        horario_texto = str(horario)[:5] if ":" in str(horario) else horario
        
        # Gerar imagem do comprovante
        imagem_comprovante = gerar_imagem_comprovante(
            titulo_filme, 
            horario_texto, 
            assentos, 
            preco_por_assento=preco_unit, 
            tamanho=(350, 200)
        )
        
        if imagem_comprovante:
            pdf_miniatura_label.configure(
                image=imagem_comprovante, 
                text="",
                height=200
            )
            pdf_miniatura_label.image = imagem_comprovante

    # ====== BOTÕES DE AÇÃO ======
    btn_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    btn_frame.pack(fill="x", pady=30, padx=40)

    def finalizar_com_comprovante():
        """Gera comprovante, insere no banco e atualiza a interface"""
        nonlocal pdf_gerado
        
        try:
            # 1. Primeiro inserir no banco
            print("DEBUG: Inserindo ingressos no banco...")
            sucesso, resultado = inserir_ingressos_no_banco(dados_compra)
            
            if not sucesso:
                messagebox.showerror("Erro", f"Erro ao registrar ingressos:\n{resultado}")
                return
            
            # 2. Gerar comprovante PDF
            print("DEBUG: Gerando comprovante...")
            horario_texto = str(horario)[:5] if ":" in str(horario) else horario
            pdf_gerado = gerar_comprovante(
                titulo_filme, 
                horario_texto, 
                assentos, 
                preco_por_assento=preco_unit, 
                logo_path="logo.png"
            )
            
            # 3. Atualizar miniatura do comprovante
            atualizar_miniatura_comprovante()
            
            # 4. Atualizar botões
            btn_finalizar.configure(state="disabled", text="✅ Compra Finalizada")
            btn_visualizar_pdf.configure(state="normal")
            
            # 5. Mostrar mensagem de sucesso
            messagebox.showinfo(
                "✅ Sucesso", 
                f"Compra finalizada com sucesso!\n\n"
                f"• {len(assentos)} ingressos registrados\n"
                f"• Comprovante gerado: {os.path.basename(pdf_gerado)}\n\n"
                f"Clique em 'Visualizar Comprovante' para ver detalhes."
            )
            
        except Exception as e:
            print(f"Erro ao finalizar compra: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao finalizar compra:\n{str(e)}")

    def visualizar_comprovante():
        """Abre o comprovante para visualização"""
        if pdf_gerado and os.path.exists(pdf_gerado):
            visualizar_comprovante_tela_cheia(frame, pdf_gerado, dados_compra)
        else:
            messagebox.showwarning("Atenção", "Por favor, finalize a compra primeiro para gerar o comprovante.")

    def voltar_menu():
        """Volta ao menu principal"""
        if finalizar_callback:
            finalizar_callback()

    # Botão para finalizar compra (gerar PDF)
    btn_finalizar = ctk.CTkButton(
        btn_frame,
        text="✅ Finalizar Compra e Gerar Comprovante",
        command=finalizar_com_comprovante,
        font=("Arial", 16, "bold"),
        fg_color=COR_BOTAO,
        hover_color=COR_BOTAO_HOVER,
        text_color=COR_TEXTO_BOTAO,
        height=50,
        width=300,
        corner_radius=10
    )
    btn_finalizar.pack(side="left", padx=10)

    # Botão para visualizar comprovante (inicialmente desabilitado)
    btn_visualizar_pdf = ctk.CTkButton(
        btn_frame,
        text="📄 Visualizar Comprovante",
        command=visualizar_comprovante,
        font=("Arial", 16, "bold"),
        fg_color="#3498db",
        hover_color="#2980b9",
        text_color=COR_TEXTO,
        height=50,
        width=250,
        corner_radius=10,
        state="disabled"  # Inicialmente desabilitado
    )
    btn_visualizar_pdf.pack(side="left", padx=10)

    # Botão para voltar ao menu
    btn_voltar = ctk.CTkButton(
        btn_frame,
        text="🏠 Voltar ao Menu",
        command=voltar_menu,
        font=("Arial", 16, "bold"),
        fg_color="#7f8c8d",
        hover_color="#6c7a7d",
        text_color=COR_TEXTO,
        height=50,
        width=200,
        corner_radius=10
    )
    btn_voltar.pack(side="left", padx=10)

    # Configurar fullscreen
    parent.master.attributes('-fullscreen', True)
    
    return frame