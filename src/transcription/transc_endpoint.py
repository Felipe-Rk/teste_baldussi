from flask import Blueprint
from .transc_controller import delete_transcription, get_all_transcriptions, get_transcription_id, transcribe, update_transcription

transcription_bp = Blueprint('transcription', __name__)

# transcription_bp.route('/transcribe', methods=['POST'])(transcribe)
# transcription_bp.route('/transcriptions', methods=['GET'])(get_all_transcriptions)
# transcription_bp.route('/transcriptions/<transcription_id>', methods=['GET'])(get_transcription_id)
# transcription_bp.route('/transcriptions/<transcription_id>', methods=['PUT'])(update_transcription)
# transcription_bp.route('/transcriptions/<transcription_id>', methods=['DELETE'])(delete_transcription)
print("Blueprint transcription_bp registrado")
transcription_bp.route('/transcribe', methods=['POST'])(transcribe)
transcription_bp.route('/', methods=['GET'])(get_all_transcriptions)
transcription_bp.route('/<transcription_id>', methods=['GET'])(get_transcription_id)
transcription_bp.route('/<transcription_id>', methods=['PUT'])(update_transcription) 
transcription_bp.route('/<transcription_id>', methods=['DELETE'])(delete_transcription)