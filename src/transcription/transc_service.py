from flask_jwt_extended import get_jwt_identity
from src.database.mongo.mongo_config import setup_mongo_database
from src.openai.openai_service import transcribe_audio, classify_transcription
from transcription.transc_entity import Transcription

def handle_transcription(file):
    try:
        user_id = get_jwt_identity()

        db = setup_mongo_database()
        collection = db['transcriptions']
        transcription = Transcription(
            audio_file=file.filename,
            transcription=None,
            classification=None,
            status='pendente',
            user_id=user_id
        )
        transcription_id = collection.insert_one(transcription.to_dict()).inserted_id

        transcription_text, classification = transcribe_audio(file)

        if not transcription_text:
            transcription.status = 'falhou'
            transcription.error_message = 'Falha ao transcrever áudio'
            collection.update_one({'_id': transcription_id}, {'$set': transcription.to_dict()})
            return {'error': 'Falha ao transcrever áudio'}

        if not classification:
            transcription.status = 'falhou'
            transcription.error_message = 'Falha ao classificar transcrição'
            collection.update_one({'_id': transcription_id}, {'$set': transcription.to_dict()})
            return {'error': 'Falha ao classificar transcrição'}

        transcription.transcription = transcription_text
        transcription.classification = classification
        transcription.status = 'realizada'
        collection.update_one({'_id': transcription_id}, {'$set': transcription.to_dict()})

        return {
            'message': 'Transcrição realizada com sucesso!',
            'transcription_id': str(transcription_id),
            'transcription': transcription_text,
            'classification': classification
        }

    except Exception as e:
        transcription.status = 'falhou'
        transcription.error_message = str(e)
        collection.update_one({'_id': transcription_id}, {'$set': transcription.to_dict()})
        return {'error': f'Erro ao transcrever áudio: {str(e)}'}