import qrcode
import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime
from config import *

def mostrar_confirmacao_pagamento(parent, filme, horario, qtd_ingressos, preco_unit):
    """
    Mostra a tela de confirmação de pagamento dentro de um frame existente
    Args:
        parent: CTkFrame onde o conteúdo será exibido
        filme: Nome do filme
        horario: Data e hora da sessão
        qtd_ingressos: Quantidade de ingressos
        preco_unit: Preço unitário do ingresso
    """
    # Limpar frame pai
    for widget in parent.winfo_children():
        widget.destroy()

    total = qtd_ingressos * preco_unit

    # ====== Gera QR Code ======
    conteudo = (
        f"COMPRA CINEPLUS\nFilme: {filme}\n"
        f"Horário: {horario}\n"
        f"Qtd: {qtd_ingressos}\n"
        f"Total: R$ {total:.2f}\n"
    )
    qr_img = qrcode.make(conteudo)
    qr_img_path = "temp_qr_code.png"
    qr_img.save(qr_img_path)

    # Cabeçalho
    ctk.CTkLabel(
        parent,
        text="✅ Pagamento Confirmado!",
        font=("Arial", 18, "bold"),
        text_color="#28a745",
        fg_color="transparent"
    ).pack(pady=20)

    # Informações detalhadas
    info_frame = ctk.CTkFrame(parent, fg_color="transparent")
    info_frame.pack(pady=10, padx=20, fill="x")

    informacoes = [
        ("🎬 Filme:", filme),
        ("🕒 Horário:", horario),
        ("🎫 Quantidade:", f"{qtd_ingressos} ingressos"),
        ("💰 Preço unitário:", f"R$ {preco_unit:.2f}"),
        ("💵 Total:", f"R$ {total:.2f}")
    ]

    for label, valor in informacoes:
        linha_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        linha_frame.pack(fill="x", pady=2)

        ctk.CTkLabel(linha_frame, text=label, font=("Arial", 12, "bold"),
                     text_color=COR_TEXTO, width=120, anchor="w").pack(side="left")

        ctk.CTkLabel(linha_frame, text=valor, font=("Arial", 12),
                     text_color=COR_TEXTO, anchor="w").pack(side="left")

    # QR Code
    try:
        img = Image.open(qr_img_path).resize((220, 220))
        qr_photo = ImageTk.PhotoImage(img)
        qr_label = ctk.CTkLabel(parent, image=qr_photo, text="")
        qr_label.image = qr_photo  # manter referência
        qr_label.pack(pady=20)
    except Exception as e:
        print(f"Erro ao carregar QR code: {e}")

    # Instruções
    ctk.CTkLabel(
        parent,
        text="📱 Apresente este QR code na entrada do cinema",
        font=("Arial", 11, "bold"),
        text_color=COR_DESTAQUE
    ).pack(pady=5)

    # Botão para avançar para Thank You
    ctk.CTkButton(
        parent,
        text="Finalizar",
        command=lambda: show_screen("thank_you"),
        font=("Arial", 14, "bold"),
        fg_color=COR_DESTAQUE,
        hover_color="#ffa94d",
        text_color=COR_FUNDO,
        height=35,
        width=120,
    ).pack(pady=15)
