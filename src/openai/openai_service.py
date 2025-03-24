from openai import OpenAI
from src.openai.openai_config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def transcribe_audio(file):

    try:
        print(f"Arquivo recebido: {file.filename}")
        file.seek(0) 

        file_bytes = file.read()

        print("Enviando arquivo para a API da OpenAI...")
        response = client.audio.transcriptions.create(
            model=OPENAI_MODEL,
            file=("audio_file", file_bytes, "audio/ogg") 
        )
        print("Resposta da API:", response)

        return response.text 

    except Exception as e:
        print(f"Erro ao transcrever áudio: {e}")
        return None