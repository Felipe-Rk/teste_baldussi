from pymongo import MongoClient
from bson import ObjectId

class Transcription:
    def __init__(self, audio_file, transcription, classification, status, user_id, error_message=None):
        self.audio_file = audio_file
        self.transcription = transcription
        self.classification = classification
        self.status = status
        self.user_id = user_id
        self.error_message = error_message

    def to_dict(self):
        return {
            'audio_file': self.audio_file,
            'transcription': self.transcription,
            'classification': self.classification,
            'status': self.status,
            'user_id': self.user_id,
            'error_message': self.error_message
        }

    @staticmethod
    def from_dict(data):
        return Transcription(
            audio_file=data.get('audio_file'),
            transcription=data.get('transcription'),
            classification=data.get('classification'),
            status=data.get('status'),
            user_id=data.get('user_id'),
            error_message=data.get('error_message')
        )