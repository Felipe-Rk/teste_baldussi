from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.openai.openai_service import transcribe_audio
from src.transcription.transc_service import handle_transcription

SUPPORTED_FORMATS = ['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']

@jwt_required()
def transcribe():
    if 'file' not in request.files:
        return jsonify({'message': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'Nome do arquivo inválido'}), 400

    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in SUPPORTED_FORMATS:
        return jsonify({'message': f'Formato não suportado. Suportados: {SUPPORTED_FORMATS}'}), 400

    file.seek(0)

    result = handle_transcription(file)

    if 'error' in result:
        return jsonify({'message': result['error']}), 500

    return jsonify({
        'message': result['message'],
        'transcription_id': result['transcription_id']
    }), 201