import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk # Importa Pillow (PIL) para lidar com JPG

# --- Nomes dos Arquivos de Imagem ---
CAMINHO_OLHO_ABERTO = "olho-aberto.jpg"
CAMINHO_OLHO_FECHADO = "olho-fechado.jpg"
TAMANHO_ICONE = (20, 20) # Tamanho desejado para o ícone

# Variável para controlar o estado da senha (True = oculta/fechada, False = visível/aberta)
senha_oculta = True
# Variáveis globais para armazenar as referências das imagens redimensionadas
img_olho_aberto_tk = None
img_olho_fechado_tk = None

def carregar_imagens():
    """Carrega, redimensiona e converte as imagens para o formato Tkinter."""
    global img_olho_aberto_tk, img_olho_fechado_tk
    
    try:
        # 1. Carregar e redimensionar a imagem de 'olho-aberto'
        img_aberto_pil = Image.open(CAMINHO_OLHO_ABERTO).resize(TAMANHO_ICONE)
        img_olho_aberto_tk = ImageTk.PhotoImage(img_aberto_pil)

        # 2. Carregar e redimensionar a imagem de 'olho-fechado'
        img_fechado_pil = Image.open(CAMINHO_OLHO_FECHADO).resize(TAMANHO_ICONE)
        img_olho_fechado_tk = ImageTk.PhotoImage(img_fechado_pil)
        
        return True
    except FileNotFoundError:
        messagebox.showerror("Erro de Arquivo", "Certifique-se de que 'olho-aberto.jpg' e 'olho-fechado.jpg' estão na mesma pasta do script.")
        return False
    except Exception as e:
        messagebox.showerror("Erro Pillow", f"Erro ao processar as imagens: {e}. Verifique se a biblioteca Pillow está instalada.")
        return False

def alternar_visibilidade_senha():
    """Alterna a visibilidade da senha e o ícone do botão."""
    global senha_oculta
    
    if senha_oculta:
        # Mostrar a senha
        entry_senha.config(show='')
        # Altera o ícone para OLHO ABERTO
        btn_olho.config(image=img_olho_aberto_tk) 
        senha_oculta = False
    else:
        # Ocultar a senha com asteriscos
        entry_senha.config(show='*')
        # Altera o ícone para OLHO FECHADO
        btn_olho.config(image=img_olho_fechado_tk) 
        senha_oculta = True

def tentar_login():
    """Função de exemplo para processar o login."""
    email = entry_email.get()
    senha = entry_senha.get()
    
    if not email or not senha:
        messagebox.showerror("Erro de Login", "Preencha todos os campos!")
    else:
        # Mostra a senha oculta ou visível, dependendo do estado
        senha_display = '*' * len(senha) if senha_oculta else senha
        messagebox.showinfo("Login", f"Tentativa de login com Email: {email} e Senha: {senha_display}")

# --- Configuração da Janela Principal ---
janela = tk.Tk()
janela.title("CINEPLUS - Login")
janela.geometry("400x300")
janela.configure(bg="#2E2E2E") # Fundo escuro

# Carregar imagens antes de criar a interface que as utiliza
if not carregar_imagens():
    janela.destroy()
    exit()

# --- Estilos (Simplificados) ---
cor_fundo_campo = "#4A4A4A" # Cinza escuro para campos de entrada
cor_texto = "white"

# --- Campo de Email ---
label_email = tk.Label(janela, text="Seu email", fg=cor_texto, bg="#2E2E2E")
label_email.pack(pady=(20, 5))

frame_email = tk.Frame(janela, bg=cor_fundo_campo)
frame_email.pack(padx=50, fill='x')

entry_email = tk.Entry(frame_email, bg=cor_fundo_campo, fg=cor_texto, insertbackground=cor_texto, bd=0, width=40)
entry_email.pack(side=tk.LEFT, padx=(10, 5), pady=5, fill='x', expand=True)
# Adicionando um espaço vazio para simular o ícone que não existe neste campo
tk.Label(frame_email, text="  ", bg=cor_fundo_campo).pack(side=tk.RIGHT, padx=5, pady=5)


# --- Campo de Senha ---
label_senha = tk.Label(janela, text="Sua senha", fg=cor_texto, bg="#2E2E2E")
label_senha.pack(pady=5)

frame_senha = tk.Frame(janela, bg=cor_fundo_campo)
frame_senha.pack(padx=50, fill='x')

entry_senha = tk.Entry(frame_senha, bg=cor_fundo_campo, fg=cor_texto, insertbackground=cor_texto, show='*', bd=0, width=40)
entry_senha.pack(side=tk.LEFT, padx=(10, 5), pady=5, fill='x', expand=True)

# Botão para o Ícone de Mostrar/Ocultar Senha
btn_olho = tk.Button(
    frame_senha, 
    image=img_olho_fechado_tk, # Inicia com o olho fechado (senha oculta)
    command=alternar_visibilidade_senha, 
    bd=0, 
    bg=cor_fundo_campo, 
    activebackground=cor_fundo_campo, # Mantém a cor do fundo ao clicar
    cursor="hand2"
)
btn_olho.pack(side=tk.RIGHT, padx=5, pady=5)


# --- Botões de Ação ---
# Simulação dos botões com cores da sua imagem
btn_entrar = tk.Button(janela, text="Entrar", command=tentar_login, bg="#FFC300", fg="black", font=("Arial", 10, "bold"), padx=20, pady=5, bd=0)
btn_entrar.pack(pady=20)
# Apenas um placeholder para o botão de Cadastro
tk.Button(janela, text="Cadastro", bg="#FFC300", fg="black", font=("Arial", 10, "bold"), padx=20, pady=5, bd=0).pack()


# Iniciar o loop principal da interface
janela.mainloop()