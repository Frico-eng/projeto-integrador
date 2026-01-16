import os

# --- App Colors ---
# Tema Escuro (padrão)
DARK_MODE = {
    "APP_BG": "#1E1E1E",
    "BTN_COLOR": "#F6C148",
    "BTN_HOVER": "#E2952D",
    "BTN_TEXT": "#1C2732",
    "COR_FUNDO": "#22313F",     # Azul-petróleo escuro
    "COR_TEXTO": "#FFFFFF",     # Branco
    "COR_DESTAQUE": "#F5A623",  # Laranja
    "FOOTER_COLOR": "#121212",
    "LABEL_TEXT": "#FFFFFF"
}

# Tema Claro
LIGHT_MODE = {
    "APP_BG": "#F0F0F0",
    "BTN_COLOR": "#F6C148",
    "BTN_HOVER": "#E2952D",
    "BTN_TEXT": "#1C2732",
    "COR_FUNDO": "#E8EAF6",     # Azul claro
    "COR_TEXTO": "#1C1C1C",     # Preto
    "COR_DESTAQUE": "#F5A623",  # Laranja
    "FOOTER_COLOR": "#EEEEEE",
    "LABEL_TEXT": "#1C1C1C"
}

# Cores padrão (tema escuro)
APP_BG = DARK_MODE["APP_BG"]
BTN_COLOR = DARK_MODE["BTN_COLOR"]
BTN_HOVER = DARK_MODE["BTN_HOVER"]
BTN_TEXT = DARK_MODE["BTN_TEXT"]
# Cores para a confirmação de pagamento
COR_FUNDO = DARK_MODE["COR_FUNDO"]     # Azul-petróleo escuro
COR_TEXTO = DARK_MODE["COR_TEXTO"]     # Branco
COR_DESTAQUE = DARK_MODE["COR_DESTAQUE"]  # Laranja

# Estado do tema global
tema_atual = "dark"
# --- Base paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

# Ensure images folder exists
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# --- Image paths ---
BANNER_PATH = os.path.join(IMAGE_DIR, "left_banner.png")
LOGO_PATH = os.path.join(IMAGE_DIR, "logo_dark.png")
ICON_USER_PATH = os.path.join(IMAGE_DIR, "user.png")
ICON_REGIST_PATH = os.path.join(IMAGE_DIR, "clipboard-list.png")
ICON_COMPRA_PATH = os.path.join(IMAGE_DIR, "movie.png")
