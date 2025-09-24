import customtkinter as ctk
from PIL import Image
from mostrar_frame import mostrar_frame

def criar_menu(app):
    # --- Frame central ---
    frame = ctk.CTkFrame(
        master=app,
        width=700,
        height=400,
        corner_radius=15,
        fg_color="#1E1E1E"
    )
    frame.pack(expand=True)

    # Configurar grid para centralizar left e right
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # --- Lado esquerdo: logo ---
    left_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
    left_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

    logo_image = ctk.CTkImage(
        light_image=Image.open("logo_light.png"),
        dark_image=Image.open("logo_dark.png"),
        size=(200, 200)
    )
    logo_label = ctk.CTkLabel(master=left_frame, image=logo_image, text="")
    logo_label.pack(expand=True)

    # --- Lado direito: botões ---
    right_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
    right_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
    right_frame.place(relx=0.55, rely=0.5, anchor="center")
    icone_user = ctk.CTkImage(
        light_image=Image.open("icone_user.png"),
        dark_image=Image.open("icone_user.png"),
        size=(30, 30)
    )
    icone_regist = ctk.CTkImage(
        light_image=Image.open("icone_regist.png"),
        dark_image=Image.open("icone_regist.png"),
        size=(30, 30)
    )
    icone_compra = ctk.CTkImage(
        light_image=Image.open("icone_compra.png"),
        dark_image=Image.open("icone_compra.png"),
        size=(30, 30)
    )

    def criar_botao(master, texto, icone, comando=None):
        return ctk.CTkButton(
            master=master,
            text=texto,
            image=icone,
            font=("Arial", 18, "bold"),
            width=250,
            height=45,
            corner_radius=15,
            fg_color="#F6C148",
            hover_color="#E2952D",
            border_width=2,
            border_color="#E2952D",
            text_color="#1C2732",
            command=comando
        )

    btn_compra = criar_botao(right_frame, "Comprar Agora", icone_compra)
    btn_compra.pack(pady=10)
    btn_user = criar_botao(right_frame, "Log-In", icone_user)
    btn_user.pack(pady=10)
    btn_regist = criar_botao(right_frame, "Registre-se", icone_regist)
    btn_regist.pack(pady=10)

    # --- Footer ---
    footer = ctk.CTkFrame(master=app, height=40, corner_radius=0, fg_color="#121212")
    footer.pack(side="bottom", fill="x")

    link_func = ctk.CTkLabel(
        master=footer,
        text="Para funcionários",
        font=("Arial", 12, "underline"),
        text_color="#3DA597",
        cursor="hand2"
    )
    link_func.pack(pady=8)
    ctk.CTkLabel(footer, text="CinePlus © 2025", text_color="gray").pack(pady=8)

    return frame
