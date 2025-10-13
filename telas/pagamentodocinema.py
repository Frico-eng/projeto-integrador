import sys
import os
import threading
import time

# Adiciona o diretório pai ao Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import qrcode
import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime
from utilidades.config import *
from tkinter import messagebox
from reportlab.lib.pagesizes import A5, landscape
from reportlab.pdfgen import canvas
from datetime import datetime

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

def gerar_comprovante(filme, horario, assentos, preco_por_assento=25.00, logo_path="logo.png"):
    total = len(assentos) * preco_por_assento
    nome_arquivo = f"Comprovante_{filme.replace(' ', '')}{datetime.now().strftime('%H%M%S')}.pdf"

    # Usar A5 landscape (420 x 297 pontos)
    c = canvas.Canvas(nome_arquivo, pagesize=landscape(A5))
    width, height = landscape(A5)  # 420 x 297

    # Margens
    margem_esq = 30
    margem_dir = 30
    largura_util = width - margem_esq - margem_dir

    # === LOGO DO CINEPLUS ===
    if os.path.exists(logo_path):
        c.drawImage(logo_path, margem_esq, height - 80, width=50, height=50, mask='auto')

    # === TÍTULO DO CINEMA ===
    c.setFont("Helvetica-Bold", 16)
    titulo = "🎬 CinePlus - Comprovante de Ingresso 🎬"
    c.drawCentredString(width / 2, height - 60, titulo)

    # Linha divisória
    c.line(margem_esq, height - 75, width - margem_dir, height - 75)

    # === DADOS DO FILME ===
    y_pos = height - 110
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margem_esq, y_pos, "Detalhes da Compra:")
    y_pos -= 25

    def quebrar_texto(texto, largura_max):
        lines = []
        words = texto.split()
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if c.stringWidth(test_line, "Helvetica", 10) <= largura_max:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return lines

    # Filme
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margem_esq, y_pos, "Filme:")
    c.setFont("Helvetica", 10)
    for line in quebrar_texto(filme, largura_util - 80):
        c.drawString(margem_esq + 50, y_pos, line)
        y_pos -= 15
    y_pos -= 5

    # Horário
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margem_esq, y_pos, "Horário:")
    c.setFont("Helvetica", 10)
    c.drawString(margem_esq + 50, y_pos, horario)
    y_pos -= 20

    # Assentos
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margem_esq, y_pos, "Assentos:")
    c.setFont("Helvetica", 10)
    for line in quebrar_texto(', '.join(assentos), largura_util - 80):
        c.drawString(margem_esq + 50, y_pos, line)
        y_pos -= 15
    y_pos -= 5

    # Preço e total
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margem_esq, y_pos, "Preço unitário:")
    c.setFont("Helvetica", 10)
    c.drawString(margem_esq + 70, y_pos, f"R$ {preco_por_assento:.2f}")
    y_pos -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(margem_esq, y_pos, "Total:")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margem_esq + 70, y_pos, f"R$ {total:.2f}")
    y_pos -= 25

    c.setFont("Helvetica-Bold", 10)
    c.drawString(margem_esq, y_pos, "Data da compra:")
    c.setFont("Helvetica", 10)
    c.drawString(margem_esq + 70, y_pos, datetime.now().strftime('%d/%m/%Y %H:%M'))
    y_pos -= 30

    # === QR CODE ===
    conteudo_qr = (
        f"CinePlus\nFilme: {filme}\nHorário: {horario}\n"
        f"Assentos: {', '.join(assentos)}\nTotal: R$ {total:.2f}\n"
        f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
    try:
        qr_img = qrcode.make(conteudo_qr)
        temp_qr_path = "temp_qr_code_pdf.png"
        qr_img.save(temp_qr_path)

        # Inserir o QR code no canto direito do PDF
        qr_size = 100
        c.drawImage(temp_qr_path, width - margem_dir - qr_size, 60, width=qr_size, height=qr_size, mask='auto')

        # Mensagem sob o QR
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(width - margem_dir - qr_size/2, 50, "Apresente este QR Code na entrada")

        # Excluir QR temporário após salvar
        os.remove(temp_qr_path)
    except Exception as e:
        print(f"Erro ao gerar QR code: {e}")

    # === RODAPÉ ===
    rodape_y = 40
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width / 2, rodape_y, "Agradecemos sua preferência! Bom filme! 🍿")

    # Linha final
    c.line(margem_esq, 30, width - margem_dir, 30)

    c.save()
    return nome_arquivo


def mostrar_confirmacao_pagamento(parent, filme, horario, qtd_ingressos, preco_unit, assentos=None, total=None, finalizar_callback=None):
    """
    Mostra a tela de confirmação de pagamento dentro de um frame existente
    """
    # Limpar frame pai
    for widget in parent.winfo_children():
        widget.destroy()

    # Calcular total se não fornecido
    if total is None:
        total = qtd_ingressos * preco_unit

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
        fg_color="#2b2b2b",  # Cinza mais escuro para o container
        bg_color="transparent",
        corner_radius=15,
        width=800,
        height=700
    )
    container_principal.place(relx=0.5, rely=0.5, anchor="center")
    container_principal.pack_propagate(False)

    # ====== CABEÇALHO ======
    header_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    header_frame.pack(fill="x", pady=(30, 20), padx=40)

    ctk.CTkLabel(
        header_frame,
        text="✅ Pagamento Confirmado!",
        font=("Arial", 24, "bold"),
        text_color="#27AE60"  # Verde para sucesso
    ).pack(pady=10)

    ctk.CTkLabel(
        header_frame,
        text="Seu ingresso foi reservado com sucesso",
        font=("Arial", 16),
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
        font=("Arial", 18, "bold"),
        text_color=COR_DESTAQUE
    ).pack(anchor="w", pady=(0, 15))

    informacoes = [
        ("🎬 Filme:", filme),
        ("🕒 Horário:", horario),
        ("🎫 Quantidade:", f"{qtd_ingressos} ingressos"),
        ("💰 Preço unitário:", f"R$ {preco_unit:.2f}"),
        ("💵 Total:", f"R$ {total:.2f}")
    ]

    # Adicionar assentos se disponível
    if assentos:
        informacoes.insert(2, ("💺 Assentos:", ", ".join(assentos)))

    for label, valor in informacoes:
        linha_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        linha_frame.pack(fill="x", pady=8)

        ctk.CTkLabel(
            linha_frame, 
            text=label, 
            font=("Arial", 14, "bold"),
            text_color=COR_TEXTO, 
            width=150, 
            anchor="w"
        ).pack(side="left")

        ctk.CTkLabel(
            linha_frame, 
            text=valor, 
            font=("Arial", 14),
            text_color=COR_TEXTO, 
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

    # Espaçamento
    ctk.CTkLabel(info_frame, text="", height=20).pack()

    # Instruções
    ctk.CTkLabel(
        info_frame,
        text="📱 Apresente este QR code na entrada do cinema",
        font=("Arial", 14, "bold"),
        text_color=COR_DESTAQUE,
        justify="left",
        wraplength=400
    ).pack(anchor="w", pady=10)

        # ====== LADO DIREITO: QR CODE ======
    qr_frame = ctk.CTkFrame(content_frame, fg_color="transparent", width=300)
    qr_frame.pack(side="right", fill="y", padx=(20, 0))
    qr_frame.pack_propagate(False)

    # Subframe centralizado para QR code e textos
    qr_inner_frame = ctk.CTkFrame(qr_frame, fg_color="transparent")
    qr_inner_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Gerar QR Code
    conteudo = (
        f"COMPRA CINEPLUS\nFilme: {filme}\n"
        f"Horário: {horario}\n"
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
        
        qr_label = ctk.CTkLabel(qr_inner_frame, image=qr_photo, text="")
        qr_label.image = qr_photo
        qr_label.pack(pady=10)

        ctk.CTkLabel(
            qr_inner_frame,
            text="QR Code do Ingresso",
            font=("Arial", 16, "bold"),
            text_color=COR_TEXTO
        ).pack(pady=10)

    except Exception as e:
        print(f"Erro ao carregar QR code: {e}")
        ctk.CTkLabel(
            qr_inner_frame,
            text="Erro ao gerar QR Code",
            font=("Arial", 14),
            text_color="#e74c3c"
        ).pack(pady=50)


    # ====== BOTÃO FINALIZAR ======
    btn_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    btn_frame.pack(fill="x", pady=30, padx=40)

    def finalizar_com_compravante():
        # Gerar comprovante apenas quando o usuário clicar em finalizar
        nome_arquivo = gerar_comprovante(filme, horario, assentos, preco_por_assento=preco_unit, logo_path="logo.png")
        messagebox.showinfo("Sucesso", f"Comprovante gerado com sucesso!\nArquivo: {nome_arquivo}")
        
        # Chamar o callback original se existir
        if finalizar_callback:
            finalizar_callback()

    ctk.CTkButton(
        btn_frame,
        text="Finalizar Compra",
        command=finalizar_com_compravante,
        font=("Arial", 16, "bold"),
        fg_color=COR_BOTAO,
        hover_color=COR_BOTAO_HOVER,
        text_color=COR_TEXTO_BOTAO,
        height=45,
        width=200,
        corner_radius=10
    ).pack(pady=10)

    # Configurar fullscreen
    parent.master.attributes('-fullscreen', True)
    
    return frame