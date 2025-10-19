import os

# --- App Colors ---
APP_BG = "#1E1E1E"
BTN_COLOR = "#F6C148"
BTN_HOVER = "#E2952D"
BTN_TEXT = "#1C2732"
# Cores para a confirmação de pagamento
COR_FUNDO = "#22313F"     # Azul-petróleo escuro
COR_TEXTO = "#FFFFFF"     # Branco
COR_DESTAQUE = "#F5A623"  # Laranja
# --- Base paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

# Ensure images folder exists
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# --- Image paths ---
BANNER_PATH = os.path.join(IMAGE_DIR, "left_banner.png")
LOGO_PATH = os.path.join(IMAGE_DIR, "logo_dark.png")
ICON_USER_PATH = os.path.join(IMAGE_DIR, "icone_user.png")
ICON_REGIST_PATH = os.path.join(IMAGE_DIR, "icone_regist.png")
ICON_COMPRA_PATH = os.path.join(IMAGE_DIR, "icone_compra.png")
