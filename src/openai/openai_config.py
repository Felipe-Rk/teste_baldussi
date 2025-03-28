import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "whisper-1"

CLASSIFICATIONS = [
    "Tecnologia",
    "Saude",
    "Educacao",
    "Financas",
    "Entretenimento",
    "Esportes",
    "Negocios",
    "Ciencia",
    "Politica",
    "Outros"
]

if not OPENAI_API_KEY:
    raise ValueError("A variável OPENAI_API_KEY não foi definida. Verifique o .env")