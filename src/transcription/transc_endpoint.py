from flask import Blueprint
from .transc_controller import transcribe

transcription_bp = Blueprint('transcription', __name__)

# Registra o endpoint de transcrição
transcription_bp.route('/transcribe', methods=['POST'])(transcribe)