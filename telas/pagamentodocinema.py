import os
import qrcode
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import A5, portrait
from reportlab.pdfgen import canvas
import shutil
import sys
import fitz  # PyMuPDF
import tempfile

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
    """Gera imagem do comprovante para preview"""
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
    """Converte páginas do PDF em imagens PIL com qualidade aprimorada"""
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
    
    # Canvas principal
    canvas = ctk.CTkCanvas(canvas_frame, bg="white")
    canvas.pack(side="left", fill="both", expand=True)
    images_frame = ctk.CTkFrame(canvas, fg_color="white")
    canvas.create_window((0, 0), window=images_frame, anchor="nw")
    imagens = pdf_para_imagens(caminho_pdf, zoom=0.8)
    
    # Exibir imagens no canvas
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
            elif sys.platform == "darwin":
                os.system(f"open '{caminho_pdf}'")
            else:
                os.system(f"xdg-open '{caminho_pdf}'")
    
    def salvar_como():

        arquivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("Todos os arquivos", "*.*")],
            initialfile=os.path.basename(caminho_pdf)
        )
        if arquivo:
            try:
                shutil.copy2(caminho_pdf, arquivo)
                messagebox.showinfo("Sucesso", f"PDF salvo em:\n{arquivo}")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar:\n{str(e)}")
    
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
def mostrar_confirmacao_pagamento(parent, dados_compra=None, finalizar_callback=None):
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
    
    # Container principal
    container = ctk.CTkFrame(frame, fg_color="#2b2b2b", corner_radius=15, width=1100, height=800)
    container.place(relx=0.5, rely=0.5, anchor="center")
    container.pack_propagate(False)
    
    # Título
    ctk.CTkLabel(container, text="✅ Pagamento Confirmado!", 
                 font=("Arial", 28, "bold"), text_color="#27AE60").pack(pady=(30, 10))
    ctk.CTkLabel(container, text="Seu ingresso foi reservado com sucesso",
                 font=("Arial", 18), text_color=COR_TEXTO).pack()
    
    # Frame de conteúdo
    content_frame = ctk.CTkFrame(container, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)
    
    # ===== LADO ESQUERDO: INFORMAÇÕES =====
    info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    info_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
    
    ctk.CTkLabel(info_frame, text="📋 Detalhes da Compra",
                 font=("Arial", 20, "bold"), text_color=COR_DESTAQUE).pack(anchor="w", pady=(0, 20))
    
    informacoes = [
        ("🎬 Filme:", filme),
        ("🕒 Horário:", str(horario)[:5]),
        ("💺 Assentos:", ", ".join(assentos) if assentos else "Nenhum"),
        ("💰 Preço unitário:", f"R$ {preco_unit:.2f}"),
        ("💵 Total:", f"R$ {total:.2f}")
    ]
    
    for label, valor in informacoes:
        linha = ctk.CTkFrame(info_frame, fg_color="transparent")
        linha.pack(fill="x", pady=10)
        ctk.CTkLabel(linha, text=label, font=("Arial", 16, "bold"), 
                    text_color=COR_TEXTO, width=180, anchor="w").pack(side="left")
        ctk.CTkLabel(linha, text=valor, font=("Arial", 16), 
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
                     font=("Arial", 16, "bold"), text_color=COR_TEXTO).pack(pady=5)
    except Exception as e:
        ctk.CTkLabel(qr_frame, text="Erro ao gerar QR Code",
                     font=("Arial", 14), text_color="#e74c3c").pack(pady=20)
    
    # ===== BOTÕES =====
    btn_frame = ctk.CTkFrame(container, fg_color="transparent")
    btn_frame.pack(fill="x", pady=30, padx=40)
    
    def finalizar_compra():
        """Gera comprovante e atualiza interface"""
        nonlocal pdf_gerado
        
        try:
            # Gerar PDF
            pdf_gerado = gerar_comprovante_pdf(
                filme, 
                str(horario)[:5], 
                assentos, 
                preco_unit
            )
            
            # Atualizar botões
            btn_finalizar.configure(state="disabled", text="✅ Compra Finalizada")
            btn_visualizar.configure(state="normal", text="📄 Abrir Comprovante")
            
            messagebox.showinfo("Sucesso", 
                f"Compra finalizada!\nComprovante gerado: {os.path.basename(pdf_gerado)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao finalizar compra:\n{str(e)}")
    
    def visualizar_comprovante_btn():
        """Abre visualização do comprovante dentro do programa"""
        if pdf_gerado and os.path.exists(pdf_gerado):
            visualizar_pdf_janela(frame, pdf_gerado, dados_compra)
        else:
            messagebox.showwarning("Atenção", "Finalize a compra primeiro para gerar o comprovante.")
    
    def voltar_ao_menu():
        """Volta para tela anterior"""
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
        font=("Arial", 16, "bold"),
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
        font=("Arial", 16, "bold"),
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
        font=("Arial", 16, "bold"),
        fg_color="#7f8c8d",
        hover_color="#6c7a7d",
        text_color=COR_TEXTO,
        height=50,
        width=200
    )
    btn_voltar.pack(side="left", padx=10)
    
    return frame