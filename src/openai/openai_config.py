# Chave da API da OpenAI
import openai


OPENAI_API_KEY = "chave"
try:
    models = openai.Model.list()
    print("Chave da API válida. Modelos disponíveis:", models)
except Exception as e:
    print("Erro ao verificar a chave da API:", e)

OPENAI_MODEL = "whisper-1"  # Modelo de transcrição de áudio