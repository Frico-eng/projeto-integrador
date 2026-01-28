# main.py
import os
import customtkinter as ctk
from PIL import Image

from utilidades.config import *
from utilidades.ui_helpers import carregar_fundo, carregar_logo, carregar_icone, criar_botao, criar_footer, criar_entry_senha, alternar_tema

from telas.auth import fazer_login
from telas.abrir_cadastro import abrir_cadastro
from telas.catalogo import criar_tela_catalogo
from telas.feedback import criar_tela_feedback
from telas.funcionario import criar_tela_funcionario
from telas.gerente import criar_tela_gerente
from telas.pagamentodocinema import mostrar_confirmacao_pagamento
from telas.agradecimento import mostrar_tela_agradecimento
from telas.seletor_assento import criar_tela_assentos
from telas.relatorio import criar_tela_dashboard
from telas.gestao_funcionarios import criar_tela_gestao_funcionarios

from utilidades.gerenciador_telas import register_screen, show_screen, register_login_entries
import utilidades.gerenciador_telas as gerenciador_telas

# Configurações do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = None
footer_main = None
footer_secondary = None

# Fonte global será criada após inicializar o app
fonte_global = None

# Funções para aumentar/diminuir fonte (limite de 4 cliques em cada direção)
def aumentar_fonte():
    if fonte_global and fonte_global.cget("size") < 22:  # 14 + (4 * 2)
        fonte_global.configure(size=fonte_global.cget("size") + 2)

def diminuir_fonte():
    if fonte_global and fonte_global.cget("size") > 6:  # 14 - (4 * 2)
        fonte_global.configure(size=fonte_global.cget("size") - 2)

# ========================= FUNÇÕES AUXILIARES =========================

# main.py (apenas a função mostrar_pagamento precisa ser atualizada)

def mostrar_pagamento(dados_compra):
    """Recebe dados completos da compra e mostra tela de pagamento"""
    print(f"DEBUG: Mostrando pagamento com dados: {dados_compra}")
    
    # Limpa o frame de pagamento
    from utilidades.gerenciador_telas import screens
    frame = screens["pagamento"]
    for widget in frame.winfo_children():
        widget.destroy()
    
    def finalizar_callback():
        """Callback chamado quando o pagamento é finalizado"""
        mostrar_tela_agradecimento(
            screens["thank_you"], 
            dados_compra=dados_compra,
            voltar_callback=lambda: show_screen("main"),
            feedback_callback=lambda: show_screen("feedback")
        )
        show_screen("thank_you")
    
    # CHAMADA CORRIGIDA: Agora passa apenas dados_compra e callback
    mostrar_confirmacao_pagamento(
        frame,
        dados_compra=dados_compra,
        finalizar_callback=finalizar_callback
    )
    
    show_screen("pagamento")
def criar_tela_assentos_com_pagamento(filme_completo):
    """Cria tela de assentos recebendo o filme completo com horário"""
    
    def avancar_para_pagamento(dados_compra):
        """Callback que recebe os dados completos da compra"""
        print(f"DEBUG: Indo para pagamento com dados completos:")
        print(f"  - Filme objeto: {dados_compra.get('filme', {})}")
        print(f"  - Sessao objeto: {dados_compra.get('sessao', {})}")
        print(f"  - Assentos: {dados_compra.get('assentos', [])}")
        print(f"  - Quantidade: {dados_compra.get('quantidade', 0)}")
        print(f"  - Preço unitário: R$ {dados_compra.get('preco_unitario', 0):.2f}")
        print(f"  - Total: R$ {dados_compra.get('total', 0):.2f}")
        
        # Garantir que temos o horário
        if 'sessao' not in dados_compra:
            dados_compra['sessao'] = filme_completo
            
        mostrar_pagamento(dados_compra)
    
    # Cria a tela de assentos passando o filme completo
    frame = criar_tela_assentos(app,
                               voltar_callback=lambda: show_screen("catalogo"),
                               avancar_callback=avancar_para_pagamento,
                               filme_selecionado=filme_completo)
    
    register_screen("assentos", frame)
    return frame

def on_confirmar_catalogo(filme_selecionado):
    """Callback chamado quando usuário confirma filme e horário no catálogo"""
    print(f"Filme selecionado no catálogo: {filme_selecionado['titulo']}")
    if filme_selecionado and filme_selecionado.get("horario_selecionado"):
        criar_tela_assentos_com_pagamento(filme_selecionado)
        show_screen("assentos")
    else:
        print("Selecione um filme e um horário")

# ========================= INICIALIZAÇÃO DAS TELAS =========================

def inicializar_telas():
    global footer_main, footer_secondary

    # --- Main screen ---
    tela_inicial = ctk.CTkFrame(app, fg_color="transparent")
    carregar_fundo(tela_inicial, BANNER_PATH)

    # Frame lateral direito com login e botões
    right_frame = ctk.CTkFrame(tela_inicial, fg_color="transparent")
    
    # Função para ajustar layout conforme tamanho da janela
    def ajustar_layout_main():
        window_width = tela_inicial.winfo_width()
        
        if window_width < 1300:
            # Layout centralizado para telas pequenas
            right_frame.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.75, anchor="n")
            contato_frame.place_forget()  # Esconde o contato em telas pequenas
        else:
            # Layout lateral para telas maiores
            right_frame.place(relx=0.65, rely=0, relwidth=0.25, relheight=1)
            contato_frame.place(relx=0.5, rely=0.82, anchor="center")  # Mostra o contato em telas grandes
    
    # Inicializar com layout padrão
    right_frame.place(relx=0.65, rely=0, relwidth=0.25, relheight=1)

    carregar_logo(right_frame, LOGO_PATH).pack(pady=(30, 20))

    icone_user = carregar_icone(ICON_USER_PATH)
    icone_regist = carregar_icone(ICON_REGIST_PATH)
    icone_compra = carregar_icone(ICON_COMPRA_PATH)

    # --- Login ---
    login_container = ctk.CTkFrame(right_frame, fg_color="transparent")
    login_container.pack(pady=(0, 15))
    email_entry = ctk.CTkEntry(login_container, placeholder_text="Seu email", height=35)
    email_entry.pack(fill='x', pady=5)
    # Passar caminhos de ícone de exemplo (coloque as imagens em utilidades/images/)
    senha_container, senha_entry, senha_toggle = criar_entry_senha(
        login_container,
        placeholder="Sua senha",
        height=35,
        show_char='•',
        icone_fechado_path=os.path.join(os.path.dirname(__file__), "utilidades", "images", "olho-fechado.png"),
        icone_aberto_path=os.path.join(os.path.dirname(__file__), "utilidades", "images", "olho-aberto.png"),
        icon_size=(20, 20)
    )
    senha_container.pack(fill='x', pady=5)
    resultado_label = ctk.CTkLabel(login_container, text="", font=fonte_global)
    resultado_label.pack(pady=5)
    # Registrar campos de login para limpeza automática (após criar resultado_label)
    from utilidades.gerenciador_telas import register_login_entries
    register_login_entries(
        email_entry,
        senha_entry,
        email_placeholder="Seu email",
        senha_placeholder="Sua senha",
        resultado_label=resultado_label
    )

    botoes_frame = ctk.CTkFrame(login_container, fg_color="transparent")
    botoes_frame.pack(pady=5)
    criar_botao(botoes_frame, "Entrar",
                lambda: fazer_login(email_entry, senha_entry, resultado_label),
                icone_user, font=fonte_global).pack(side="left", padx=5)
    criar_botao(botoes_frame, "Cadastro",
                lambda: show_screen("cadastro"),
                icone_regist, font=fonte_global).pack(side="left", padx=5)

    # Botões extras - APENAS Filmes em cartaz
    criar_botao(right_frame, "Filmes em cartaz", lambda: show_screen("catalogo"), icone_compra, width=250, font=fonte_global).pack(pady=15)

    # Botões para controle de fonte
    frame_controle_fonte = ctk.CTkFrame(right_frame, fg_color="transparent")
    frame_controle_fonte.pack(pady=(0, 10))
    ctk.CTkButton(frame_controle_fonte, text="A+", command=aumentar_fonte, width=50, font=fonte_global).pack(side="left", padx=5)
    ctk.CTkButton(frame_controle_fonte, text="A-", command=diminuir_fonte, width=50, font=fonte_global).pack(side="left", padx=5)

    # Botão para alternar tema claro e escuro
    from utilidades.ui_helpers import alternar_tema
    botao_tema = ctk.CTkButton(
        frame_controle_fonte,
        text="🌙",
        command=lambda: alternar_tema(app, botao_tema),
        width=50,
        font=fonte_global,
        fg_color=BTN_COLOR,
        hover_color=BTN_HOVER,
        text_color=BTN_TEXT
    )
    botao_tema.pack(side="left", padx=5)

    # Contato
    contato_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
    contato_frame.place(relx=0.5, rely=0.82, anchor="center")
    ctk.CTkLabel(contato_frame, text="Entre em contato", font=fonte_global).pack(pady=2)
    ctk.CTkLabel(contato_frame, text="Telefone: 3022-2002", font=fonte_global).pack(pady=2)
    ctk.CTkLabel(contato_frame, text="Endereço: R. Aristides Lobo, 1058 - Campina, Belém - PA, 66017-010", font=fonte_global, wraplength=200).pack(pady=2)
    ctk.CTkLabel(contato_frame, text="E-mail: sistema@cineplus.com.br", font=fonte_global, wraplength=200).pack(pady=2)

    register_screen("main", tela_inicial)
    
    # Vincula o evento de redimensionamento para ajustar layout dinamicamente
    tela_inicial.bind("<Configure>", lambda e: ajustar_layout_main())

    # --- Feedback ---
    feedback_frame = criar_tela_feedback(app, voltar_callback=lambda: show_screen("main"), fonte_global=fonte_global)
    register_screen("feedback", feedback_frame)

    # --- Cadastro ---
    cadastro_frame, btn_voltar_cadastro = abrir_cadastro(app, fonte_global)
    btn_voltar_cadastro.configure(command=lambda: show_screen("main"))
    register_screen("cadastro", cadastro_frame)

    # --- Catalogo ---
    catalogo_frame = ctk.CTkFrame(app, fg_color="transparent")
    catalogo_content = criar_tela_catalogo(
        catalogo_frame,
        voltar_callback=lambda: show_screen("main"),
        confirmar_callback=on_confirmar_catalogo,
        fonte_global=fonte_global
    )
    catalogo_content.pack(fill="both", expand=True)
    register_screen("catalogo", catalogo_frame)

    # --- Funcionario --- (mantido para acesso interno se necessário)
    funcionario_frame = ctk.CTkFrame(app, fg_color="transparent")
    funcionario_content = criar_tela_funcionario(funcionario_frame, voltar_callback=lambda: show_screen("main"), fonte_global=fonte_global)
    funcionario_content.pack(fill="both", expand=True)
    register_screen("funcionario", funcionario_frame)

    # --- Gerente ---
    gerente_frame = ctk.CTkFrame(app, fg_color="transparent")
    gerente_content = criar_tela_gerente(gerente_frame, voltar_callback=lambda: show_screen("main"), fonte_global=fonte_global)
    gerente_content.pack(fill="both", expand=True)
    register_screen("gerente", gerente_frame)

    # --- Gestão de Funcionários ---
    gestao_funcionarios_frame = ctk.CTkFrame(app, fg_color="transparent")
    gestao_funcionarios_content = criar_tela_gestao_funcionarios(gestao_funcionarios_frame, voltar_callback=lambda: show_screen("gerente"), fonte_global=fonte_global)
    gestao_funcionarios_content.pack(fill="both", expand=True)
    register_screen("gestao_funcionarios", gestao_funcionarios_frame)

    # --- Relatorio ---
    relatorio_frame = ctk.CTkFrame(app, fg_color="transparent")
    relatorio_content = criar_tela_dashboard(relatorio_frame, voltar_callback=lambda: show_screen("gerente"), fonte_global=fonte_global)
    relatorio_content.pack(fill="both", expand=True)
    register_screen("relatorio", relatorio_frame)

    # --- Assentos ---
    assentos_frame = ctk.CTkFrame(app, fg_color="transparent")
    register_screen("assentos", assentos_frame)

    # --- Pagamento ---
    pagamento_frame = ctk.CTkFrame(app, fg_color="transparent")
    register_screen("pagamento", pagamento_frame)

    # --- Thank You ---
    thank_you_frame = ctk.CTkFrame(app, fg_color="transparent")
    register_screen("thank_you", thank_you_frame)

    # --- Footers ---
    footer_main, footer_secondary = criar_footer(app)
    # Registrar footers no módulo de gerenciador para que show_screen
    # possa manipular e também limpar campos ao retornar para 'main'.
    try:
        gerenciador_telas.footer_main = footer_main
        gerenciador_telas.footer_secondary = footer_secondary
    except Exception:
        pass

# ========================= INICIALIZAR APLICAÇÃO =========================

def inicializar_app():
    global app, fonte_global
    app = ctk.CTk(fg_color=APP_BG)
    screen_width, screen_height = app.winfo_screenwidth(), app.winfo_screenheight()
    
    # Responsivo: ajusta o tamanho da janela com limite mínimo
    min_width = 800
    min_height = 600
    window_width = max(min_width, int(screen_width * 0.95))
    window_height = max(min_height, int(screen_height * 0.95))
    
    # Centraliza a janela
    x_offset = (screen_width - window_width) // 2
    y_offset = (screen_height - window_height) // 2
    
    app.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")
    app.minsize(min_width, min_height)
    app.title("CinePlus - Sistema de Cinema")

    # Criar fonte global após inicializar o app
    fonte_global = ctk.CTkFont(family="Arial", size=14)

    # Adicionar handler para limpeza ao fechar a aplicação
    def on_closing():
        import matplotlib.pyplot as plt
        # Fechar todas as figuras matplotlib abertas para liberar memória
        plt.close('all')
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)

    inicializar_telas()
    show_screen("main")
    app.mainloop()

# ========================= EXECUÇÃO =========================
if __name__ == "__main__":
    inicializar_app()