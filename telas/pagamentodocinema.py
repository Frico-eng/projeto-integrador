import os
import qrcode
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk
from datetime import datetime
from tkinter import messagebox
from reportlab.lib.pagesizes import A5, portrait
from reportlab.pdfgen import canvas
import sys
import fitz 
from crud.crud_ingressos import processar_compra_ingressos
from utilidades.session import get_user_id

# Configurações básicas
COR_FUNDO = "#1C1C1C"
COR_TEXTO = "#ECF0F1"
COR_DESTAQUE = "#F6C148"
COR_BOTAO = "#F6C148"
COR_BOTAO_HOVER = "#E2952D"

# ============ FUNÇÕES AUXILIARES ============
def gerar_comprovante_pdf(filme, horario, assentos, preco_por_assento=25.00):
    """Gera um PDF do comprovante com QR Code"""
    total = len(assentos) * preco_por_assento
    nome_arquivo = f"Comprovante_{datetime.now().strftime('%H%M%S')}.pdf"
    
    # Criar PDF
    c = canvas.Canvas(nome_arquivo, pagesize=portrait(A5))
    largura, altura = portrait(A5)
    
    # Gerar QR Code
    try:
        conteudo_qr = f"CINEPLUS\nFilme: {filme}\nHorário: {horario}\nAssentos: {', '.join(assentos)}\nTotal: R$ {total:.2f}"
        qr = qrcode.make(conteudo_qr)
        qr_temp = f"temp_qr_{datetime.now().strftime('%H%M%S')}.png"
        qr.save(qr_temp)
        c.drawImage(qr_temp, 165, 180, width=100, height=100)
        os.remove(qr_temp)
    except:
        pass
    
    # Conteúdo do PDF
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(largura/2, 550, "🎬 CinePlus - Comprovante 🎬")
    
    c.setFont("Helvetica", 14)
    c.drawCentredString(largura/2, 480, f"Filme: {filme}")
    c.drawCentredString(largura/2, 455, f"Horário: {horario}")
    c.drawCentredString(largura/2, 430, f"Assentos: {', '.join(assentos)}")
    c.drawCentredString(largura/2, 400, f"Total: R$ {total:.2f}")
    
    data_compra = datetime.now().strftime('%d/%m/%Y %H:%M')
    c.drawCentredString(largura/2, 370, f"Data: {data_compra}")
    
    c.save()
    return nome_arquivo

def gerar_imagem_comprovante(filme, horario, assentos, preco_por_assento=25.00):
    total = len(assentos) * preco_por_assento
    largura, altura = 400, 280
    
    img = Image.new('RGB', (largura, altura), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Desenhar fundo
    draw.rectangle([(0, 0), (largura, altura)], fill="#F8F8F8", outline="#DDDDDD", width=2)
    draw.rectangle([(0, 0), (largura, 50)], fill=COR_DESTAQUE)
    
    # Adicionar texto
    titulo_texto = "🎬 CinePlus - Comprovante 🎬"
    draw.text((largura//2, 25), titulo_texto, fill="#000000", anchor="mm")
    
    y_pos = 70
    espacamento = 28
    
    info = [
        ("🎬 Filme:", filme[:25] + "..." if len(filme) > 25 else filme),
        ("🕒 Horário:", horario),
        ("💺 Assentos:", ', '.join(assentos)[:20] + "..." if len(', '.join(assentos)) > 20 else ', '.join(assentos)),
        ("💰 Unitário:", f"R$ {preco_por_assento:.2f}"),
        ("💵 Total:", f"R$ {total:.2f}")
    ]
    
    for label, valor in info:
        draw.text((20, y_pos), label, fill="#000000")
        draw.text((120, y_pos), valor, fill="#333333")
        y_pos += espacamento
    
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
    draw.text((largura//2, altura-25), f"📅 {data_atual}", fill="#666666", anchor="mm")
    
    return ctk.CTkImage(img, size=(largura, altura))

def pdf_para_imagens(pdf_path, zoom=2.0):
    images = []
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Configurações de renderização para melhor qualidade
            mat = fitz.Matrix(zoom, zoom)  # Aumenta a resolução
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            # Converter para imagem PIL
            img_data = pix.samples
            img = Image.frombytes("RGB", [pix.width, pix.height], img_data)
            images.append(img)
        doc.close()
    except Exception as e:
        print(f"Erro ao converter PDF: {e}")
    return images

def visualizar_pdf_janela(parent, caminho_pdf, dados_compra):
    if not os.path.exists(caminho_pdf):
        messagebox.showerror("Erro", "Arquivo PDF não encontrado!")
        return
    
    janela = ctk.CTkToplevel(parent)
    janela.title("Visualizar Comprovante PDF - CinePlus")
    janela.geometry("430x750")
    janela.grab_set()
    janela.resizable(False, False)
    main_frame = ctk.CTkFrame(janela, fg_color=COR_FUNDO)
    main_frame.pack(fill="both", expand=True, padx=0, pady=10)
    header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    header_frame.pack(fill="x", pady=(5, 15))
    
    ctk.CTkLabel(header_frame, text="Visualizador de Comprovante", 
             font=("Arial", 22, "bold"), text_color=COR_DESTAQUE
            ).pack(anchor="center", padx=10, pady=10)
    
    # Frame para o PDF
    pdf_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b", corner_radius=10)
    pdf_frame.pack(fill="both", expand=True, padx=10, pady=5)
    canvas_frame = ctk.CTkFrame(pdf_frame, fg_color="#FFFFFF")
    canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)
    canvas = ctk.CTkCanvas(canvas_frame, bg="white")
    canvas.pack(side="left", fill="both", expand=True)
    images_frame = ctk.CTkFrame(canvas, fg_color="white")
    canvas.create_window((0, 0), window=images_frame, anchor="nw")
    imagens = pdf_para_imagens(caminho_pdf, zoom=0.8)

    photo_images = []
    y_offset = 10
    
    for i, img in enumerate(imagens):
        # Redimensionar mantendo proporção para caber na janela
        largura_max = 400
        proporcao = largura_max / img.width
        nova_largura = int(img.width * proporcao)
        nova_altura = int(img.height * proporcao)
        
        img_resized = img.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
        
        # Converter para PhotoImage
        photo = ImageTk.PhotoImage(img_resized)
        photo_images.append(photo)  # Manter referência

        label = ctk.CTkLabel(images_frame, image=photo, text="")
        label.image = photo
        label.pack(pady=(0, 10))
        
        # Adicionar número da página
        page_label = ctk.CTkLabel(images_frame, 
                                 text=f"Página {i+1} de {len(imagens)}",
                                 font=("Arial", 12),
                                 text_color="#666666")
        page_label.pack(pady=(0, 20))
        
        y_offset += nova_altura + 40
    
    # Configurar scrollregion
    images_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    # Botões de controle
    btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    btn_frame.pack(fill="x", pady=15)
    
    def abrir_externo():
        if os.path.exists(caminho_pdf):
            if sys.platform == "win32":
                os.startfile(caminho_pdf)
    
    def imprimir_pdf():
        if os.path.exists(caminho_pdf):
            resposta = messagebox.askyesno("Imprimir", 
                "Deseja imprimir o comprovante?\nO PDF será aberto no visualizador padrão para impressão.")
            if resposta:
                abrir_externo()
    
    # Botões
        ctk.CTkButton(btn_frame, text="Imprimir", command=imprimir_pdf,
                      fg_color="#3498db", hover_color="#2980b9",
                      width=120).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Abrir Externo", command=abrir_externo,
                      fg_color="#9b59b6", hover_color="#8e44ad",
                      width=120).pack(side="left", padx=5)

    ctk.CTkButton(btn_frame, text="Fechar", command=janela.destroy,
                  fg_color="#e74c3c", hover_color="#c0392b",
                  width=120).pack(side="left", padx=5)
    
    # Manter referência às imagens
    janela.photo_images = photo_images

# ============ TELA PRINCIPAL DE CONFIRMAÇÃO ============
def mostrar_confirmacao_pagamento(parent, dados_compra=None, finalizar_callback=None, fonte_global=None):
    # Limpar tela anterior
    for widget in parent.winfo_children():
        widget.destroy()
    
    # Dados padrão se não fornecidos
    if not dados_compra:
        dados_compra = {
            'filme': {'Titulo_Filme': 'Filme não especificado'},
            'sessao': {'Hora_Sessao': 'Horário não especificado'},
            'assentos': [],
            'preco_unitario': 25.00,
            'total': 0
        }
    
    # Extrair dados
    filme = dados_compra.get("filme", {}).get("Titulo_Filme", "Filme")
    horario = dados_compra.get("sessao", {}).get("Hora_Sessao", "Horário")
    assentos = dados_compra.get("assentos", [])
    preco_unit = dados_compra.get("preco_unitario", 25.00)
    total = dados_compra.get("total", len(assentos) * preco_unit)
    
    # Variável para o PDF gerado
    pdf_gerado = None
    
    # ===== CONFIGURAR INTERFACE =====
    frame = ctk.CTkFrame(parent, fg_color=COR_FUNDO, width=1800, height=900)
    frame.pack_propagate(False)
    frame.pack(fill="both", expand=True)

    # Se não foi passada `fonte_global`, tentar obter a fonte global do módulo main
    if fonte_global is None:
        try:
            import main as main_mod
            fonte_global = getattr(main_mod, "fonte_global", None)
        except Exception:
            fonte_global = None

    # Fonte local quando fonte_global não for fornecida
    current_font_size = fonte_global.cget("size") if fonte_global else 14

    def aplicar_fonte_local():
        fs = current_font_size
        def _apply_font(widget):
            try:
                widget.configure(font=("Arial", fs))
            except Exception:
                pass
            for child in widget.winfo_children():
                _apply_font(child)

        try:
            _apply_font(frame)
        except Exception as e:
            print(f"DEBUG: aplicar_fonte_local pagamentodocinema erro: {e}")

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
    
    # Container principal
    container = ctk.CTkFrame(frame, fg_color="#2b2b2b", corner_radius=15, width=1100, height=800)
    container.place(relx=0.5, rely=0.5, anchor="center")
    container.pack_propagate(False)
    
    # Top bar: title left, font controls right
    top_bar = ctk.CTkFrame(container, fg_color="transparent")
    top_bar.pack(fill="x", pady=(20, 6), padx=20)

    ctk.CTkLabel(top_bar, text="✅ Pagamento Confirmado!", 
                 font=fonte_global if fonte_global else ("Arial", 28, "bold"), text_color="#27AE60").pack(side="left")
    ctk.CTkLabel(top_bar, text="Seu ingresso foi reservado com sucesso",
                 font=fonte_global if fonte_global else ("Arial", 18), text_color=COR_TEXTO).pack(side="left", padx=20)

    # Font controls top-right (always visible)
    controls_top = ctk.CTkFrame(top_bar, fg_color="transparent")
    controls_top.pack(side="right")
    ctk.CTkButton(controls_top, text="A+", command=aumentar_fonte, width=50, font=fonte_global if fonte_global else None).pack(side="left", padx=4)
    ctk.CTkButton(controls_top, text="A-", command=diminuir_fonte, width=50, font=fonte_global if fonte_global else None).pack(side="left", padx=4)
    
    # Frame de conteúdo
    content_frame = ctk.CTkFrame(container, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)
    
    # ===== LADO ESQUERDO: INFORMAÇÕES =====
    info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    info_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
    ctk.CTkLabel(info_frame, text="📋 Detalhes da Compra",
                font=fonte_global, text_color=COR_DESTAQUE).pack(anchor="w", pady=(0, 20))

    # Frame para filme
    filme_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
    filme_frame.pack(fill="x", pady=10)
    ctk.CTkLabel(filme_frame, text="🎬 Filme:", font=fonte_global, 
            text_color=COR_TEXTO, width=180, anchor="w").pack(side="left")
    ctk.CTkLabel(filme_frame, text=filme, font=fonte_global, 
            text_color=COR_TEXTO, anchor="w").pack(side="left")

    # Frame para horário
    horario_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
    horario_frame.pack(fill="x", pady=10)
    ctk.CTkLabel(horario_frame, text="🕒 Horário:", font=fonte_global, 
            text_color=COR_TEXTO, width=180, anchor="w").pack(side="left")
    ctk.CTkLabel(horario_frame, text=str(horario)[:5], font=fonte_global, 
            text_color=COR_TEXTO, anchor="w").pack(side="left")

    # Frame para assentos
    assentos_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
    assentos_frame.pack(fill="x", pady=10)
    ctk.CTkLabel(assentos_frame, text="💺 Assentos:", font=fonte_global, 
            text_color=COR_TEXTO, width=180, anchor="w").pack(side="left")
    assentos_texto = ", ".join(assentos) if assentos else "Nenhum"
    ctk.CTkLabel(assentos_frame, text=assentos_texto, font=fonte_global, 
            text_color=COR_TEXTO, anchor="w").pack(side="left")

    # Frame para preço unitário
    preco_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
    preco_frame.pack(fill="x", pady=10)
    ctk.CTkLabel(preco_frame, text="💰 Preço unitário:", font=fonte_global, 
            text_color=COR_TEXTO, width=180, anchor="w").pack(side="left")
    ctk.CTkLabel(preco_frame, text=f"R$ {preco_unit:.2f}", font=fonte_global, 
            text_color=COR_TEXTO, anchor="w").pack(side="left")

    # Frame para total
    total_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
    total_frame.pack(fill="x", pady=10)
    ctk.CTkLabel(total_frame, text="💵 Total:", font=fonte_global, 
            text_color=COR_TEXTO, width=180, anchor="w").pack(side="left")
    ctk.CTkLabel(total_frame, text=f"R$ {total:.2f}", font=fonte_global, 
        text_color=COR_TEXTO, anchor="w").pack(side="left")
    
    # ===== LADO DIREITO: QR CODE =====
    qr_frame = ctk.CTkFrame(content_frame, fg_color="transparent", width=400)
    qr_frame.pack(side="right", fill="y")
    
    # Gerar QR Code
    try:
        conteudo = f"CINEPLUS\nFilme: {filme}\nHorário: {horario}\nAssentos: {', '.join(assentos)}\nTotal: R$ {total:.2f}"
        qr_img = qrcode.make(conteudo)
        qr_img.save("temp_qr.png")
        
        img = Image.open("temp_qr.png").resize((280, 280))
        qr_photo = ctk.CTkImage(img, size=(280, 280))
        
        ctk.CTkLabel(qr_frame, image=qr_photo, text="").pack()
        ctk.CTkLabel(qr_frame, text="QR Code do Ingresso",
                 font=fonte_global if fonte_global else ("Arial", 16, "bold"), text_color=COR_TEXTO).pack(pady=5)
    except Exception as e:
        ctk.CTkLabel(qr_frame, text="Erro ao gerar QR Code",
                     font=("Arial", 14), text_color="#e74c3c").pack(pady=20)
    
    # ===== BOTÕES =====
    btn_frame = ctk.CTkFrame(container, fg_color="transparent")
    btn_frame.pack(fill="x", pady=30, padx=40)
    
    def finalizar_compra():
        nonlocal pdf_gerado
        
        try:
            # Primeiro, salvar os ingressos no banco
            id_cliente = get_user_id()
            if not id_cliente:
                messagebox.showerror("Erro", "Nenhum usuário logado. Faça login antes de finalizar a compra.")
                return

            id_sessao = dados_compra.get('sessao', {}).get('ID_Sessao')
            lista_assentos_ids = dados_compra.get('assentos_ids_sessao', [])

            success, ids_criados, mensagem = processar_compra_ingressos(
                id_cliente,
                id_sessao,
                lista_assentos_ids,
                preco_unit
            )

            if not success:
                messagebox.showerror("Erro", f"Falha ao salvar ingressos: {mensagem}")
                return

            # Salvo com sucesso; anotar IDs no dados_compra e gerar comprovante
            dados_compra['ids_ingressos'] = ids_criados
            pdf_gerado = gerar_comprovante_pdf(
                filme, 
                str(horario)[:5], 
                assentos, 
                preco_unit
            )

            # Atualizar botões
            btn_finalizar.configure(state="disabled", text="✅ Compra Finalizada")
            btn_visualizar.configure(state="normal", text="📄 Abrir Comprovante")

            messagebox.showinfo("Sucesso", mensagem)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao finalizar compra:\n{str(e)}")
    
    def visualizar_comprovante_btn():
        if pdf_gerado and os.path.exists(pdf_gerado):
            visualizar_pdf_janela(frame, pdf_gerado, dados_compra)
        else:
            messagebox.showwarning("Atenção", "Finalize a compra primeiro para gerar o comprovante.")
    
    def voltar_ao_menu():
        # Limpar arquivo temporário se existir
        if os.path.exists("temp_qr.png"):
            try:
                os.remove("temp_qr.png")
            except:
                pass
        
        if finalizar_callback:
            finalizar_callback()
    
    # Botão Finalizar
    btn_finalizar = ctk.CTkButton(
        btn_frame,
        text="✅ Finalizar Compra",
        command=finalizar_compra,
        font=fonte_global if fonte_global else ("Arial", 16, "bold"),
        fg_color=COR_BOTAO,
        hover_color=COR_BOTAO_HOVER,
        text_color="#1C2732",
        height=50,
        width=250
    )
    btn_finalizar.pack(side="left", padx=10)
    
    # Botão Visualizar (inicialmente desabilitado)
    btn_visualizar = ctk.CTkButton(
        btn_frame,
        text="📄 Visualizar Comprovante",
        command=visualizar_comprovante_btn,
        font=fonte_global if fonte_global else ("Arial", 16, "bold"),
        fg_color="#3498db",
        hover_color="#2980b9",
        text_color=COR_TEXTO,
        height=50,
        width=250,
        state="disabled"
    )
    btn_visualizar.pack(side="left", padx=10)
    
    # Botão Voltar
    btn_voltar = ctk.CTkButton(
        btn_frame,
        text="Avançar",
        command=voltar_ao_menu,
        font=fonte_global if fonte_global else ("Arial", 16, "bold"),
        fg_color="#7f8c8d",
        hover_color="#6c7a7d",
        text_color=COR_TEXTO,
        height=50,
        width=200
    )
    btn_voltar.pack(side="left", padx=10)
    
    # Aplicar fonte inicial para caso de fonte local
    try:
        aplicar_fonte_local()
    except Exception:
        pass

    return frame