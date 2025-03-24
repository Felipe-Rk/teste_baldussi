from flask import Blueprint
from src.transcription.transc_controller import (
    transcribe, get_all_transcriptions, get_transcription_id, update_transcription, delete_transcription, search_transcriptions
)

transcription_bp = Blueprint('transcription', __name__)

@transcription_bp.route('/transcribe', methods=['POST'])
def transcribe_route():
    return transcribe()

@transcription_bp.route('/', methods=['GET'])
def get_all_transcriptions_route():
    return get_all_transcriptions()

@transcription_bp.route('/<transcription_id>', methods=['GET'])
def get_transcription_id_route(transcription_id):
    return get_transcription_id(transcription_id)

@transcription_bp.route('/<transcription_id>', methods=['PUT'])
def update_transcription_route(transcription_id):
    return update_transcription(transcription_id)

@transcription_bp.route('/<transcription_id>', methods=['DELETE'])
def delete_transcription_route(transcription_id):
    return delete_transcription(transcription_id)

@transcription_bp.route('/search', methods=['GET'])
def search_transcriptions_route():
    return search_transcriptions()
