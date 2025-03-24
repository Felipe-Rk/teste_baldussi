from flask import Blueprint
from flasgger import swag_from
from src.transcription.transc_controller import (
    transcribe, get_all_transcriptions, get_transcription_id, update_transcription, delete_transcription, search_transcriptions
)

transcription_bp = Blueprint('transcription', __name__)

@transcription_bp.route('/transcribe', methods=['POST'])
@swag_from({
    'tags': ['Transcriptions'],
    'summary': 'Realizar transcrição',
    'description': 'Envia um arquivo de áudio para transcrição.',
    'responses': {
        200: {'description': 'Transcrição realizada com sucesso'},
        400: {'description': 'Erro na transcrição'}
    }
})
def transcribe_route():
    return transcribe()

@transcription_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Transcriptions'],
    'summary': 'Listar todas as transcrições',
    'responses': {
        200: {'description': 'Lista de transcrições retornada com sucesso'},
        404: {'description': 'Nenhuma transcrição encontrada'}
    }
})
def get_all_transcriptions_route():
    return get_all_transcriptions()

@transcription_bp.route('/<transcription_id>', methods=['GET'])
@swag_from({
    'tags': ['Transcriptions'],
    'summary': 'Obter transcrição por ID',
    'responses': {
        200: {'description': 'Transcrição encontrada'},
        404: {'description': 'Transcrição não encontrada'}
    }
})
def get_transcription_id_route(transcription_id):
    return get_transcription_id(transcription_id)

@transcription_bp.route('/<transcription_id>', methods=['PUT'])
@swag_from({
    'tags': ['Transcriptions'],
    'summary': 'Atualizar transcrição',
    'responses': {
        200: {'description': 'Transcrição atualizada com sucesso'},
        400: {'description': 'Falha ao atualizar transcrição'}
    }
})
def update_transcription_route(transcription_id):
    return update_transcription(transcription_id)

@transcription_bp.route('/<transcription_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Transcriptions'],
    'summary': 'Deletar transcrição',
    'responses': {
        200: {'description': 'Transcrição deletada com sucesso'},
        400: {'description': 'Falha ao deletar transcrição'}
    }
})
def delete_transcription_route(transcription_id):
    return delete_transcription(transcription_id)

@transcription_bp.route('/search', methods=['GET'])
@swag_from({
    'tags': ['Transcriptions'],
    'summary': 'Pesquisar transcrições',
    'description': 'Realiza uma pesquisa de transcrições com base em critérios.',
    'responses': {
        200: {'description': 'Resultados da pesquisa retornados com sucesso'},
        404: {'description': 'Nenhuma transcrição encontrada'}
    }
})
def search_transcriptions_route():
    return search_transcriptions()