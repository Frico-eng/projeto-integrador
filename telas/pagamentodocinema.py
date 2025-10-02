import sys
import os

# Adiciona o diretório pai ao Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import qrcode
import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime
from utilidades.config import *

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
    qr_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    qr_frame.pack(side="right", fill="y", padx=(20, 0))

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
        
        qr_label = ctk.CTkLabel(qr_frame, image=qr_photo, text="")
        qr_label.image = qr_photo
        qr_label.pack(pady=10)

        ctk.CTkLabel(
            qr_frame,
            text="QR Code do Ingresso",
            font=("Arial", 16, "bold"),
            text_color=COR_TEXTO
        ).pack(pady=10)

    except Exception as e:
        print(f"Erro ao carregar QR code: {e}")
        ctk.CTkLabel(
            qr_frame,
            text="Erro ao gerar QR Code",
            font=("Arial", 14),
            text_color="#e74c3c"
        ).pack(pady=50)

    # ====== BOTÃO FINALIZAR ======
    btn_frame = ctk.CTkFrame(container_principal, fg_color="transparent")
    btn_frame.pack(fill="x", pady=30, padx=40)

    ctk.CTkButton(
        btn_frame,
        text="Finalizar Compra",
        command=finalizar_callback if finalizar_callback else lambda: print("Finalizar clicado"),
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