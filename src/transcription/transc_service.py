from flask_jwt_extended import get_jwt_identity
from src.database.mongo.mongo_config import setup_mongo_database
from src.openai.openai_service import transcribe_audio

def handle_transcription(file):

    try:
        user_id = get_jwt_identity()
        transcription = transcribe_audio(file)

        if not transcription:
            return {'error': 'Falha ao transcrever áudio'}

        db = setup_mongo_database()
        collection = db['transcriptions']
        
        result = collection.insert_one({
            'audio_file': file.filename,
            'transcription': transcription,
            'status': 'realizada',
            'user_id': user_id
        })

        return {
            'message': 'Transcrição realizada com sucesso!',
            'transcription_id': str(result.inserted_id)
        }

    except Exception as e:
        return {'error': f'Erro ao transcrever áudio: {str(e)}'}