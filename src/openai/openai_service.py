import openai
from src.openai.openai_config import OPENAI_API_KEY, OPENAI_MODEL

# Configura a chave da API da OpenAI
openai.api_key = OPENAI_API_KEY

def transcribe_audio(file):
    try:
        print(f"Arquivo recebido: {file.filename}")  
        file.seek(0)  # Garante que o ponteiro do arquivo está no início

        # Envio correto do arquivo para a API
        response = openai.Audio.transcribe(
            model=OPENAI_MODEL, 
            file=file  # Enviando como um arquivo binário
        )

        print("Resposta da API:", response)  
        return response['text'] 

    except Exception as e:
        print(f"Erro ao transcrever áudio: {e}")
        return None