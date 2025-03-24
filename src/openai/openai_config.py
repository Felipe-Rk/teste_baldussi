import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "whisper-1"

CLASSIFICATIONS = [
    "Tecnologia",
    "Saúde",
    "Educação",
    "Finanças",
    "Entretenimento",
    "Esportes",
    "Negócios",
    "Ciência",
    "Política",
    "Outros"
]

if not OPENAI_API_KEY:
    raise ValueError("A variável OPENAI_API_KEY não foi definida. Verifique o .env")