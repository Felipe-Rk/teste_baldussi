
from openai import OpenAI
from src.openai.openai_config import OPENAI_API_KEY, OPENAI_MODEL, CLASSIFICATIONS

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

        transcription_text = response.text.strip()
        print("Transcrição recebida:", transcription_text)

        classification = classify_transcription(transcription_text)

        return transcription_text, classification  

    except Exception as e:
        print(f"Erro ao transcrever áudio: {e}")
        return None, None  

def classify_transcription(transcription_text):
    """
    Classifica a transcrição por assunto utilizando a API da OpenAI.
    Retorna uma das classificações fixas.
    """
    try:
        print("Classificando transcrição por assunto...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Classifique a transcrição por assunto. Use uma das seguintes categorias: {', '.join(CLASSIFICATIONS)}"},
                {"role": "user", "content": transcription_text}
            ]
        )
        classification = response.choices[0].message.content.strip()

        # Verifica se a classificação está na lista de CLASSIFICATIONS
        if classification not in CLASSIFICATIONS:
            classification = "Outros"

        print(f"Classificação obtida: {classification}")
        return classification

    except Exception as e:
        print(f"Erro ao classificar transcrição: {e}")
        return None
