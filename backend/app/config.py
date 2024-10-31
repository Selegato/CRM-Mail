import os

import pytz
from dotenv import load_dotenv

from app.utils import create_temp_dir

# Carrega as variáveis de ambiente
load_dotenv()

# Define o fuso horário do Brasil
BR_TZ = pytz.timezone("America/Sao_Paulo")

# Configurações do banco de dados
DB_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME")

# Configurações de SMTP
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Diretório temporário para salvar anexos
TEMP_DIR = create_temp_dir()

# Tipos de arquivos permitidos para upload
ALLOWED_MIME_TYPES = {"image/png", "image/jpg", "image/jpeg", "image/heic"}

#numero maximo de arquivos permitidos
MAX_FILES = 4
MAX_SIZE= 1 * 1024 * 1024  # 1MB