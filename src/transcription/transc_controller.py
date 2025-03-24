from bson import ObjectId
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from auth.permissions import role_required
from src.database.mysql.mysql_config import setup_mysql_database
from src.database.mongo.mongo_config import setup_mongo_database
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


@jwt_required()
@role_required('admin')
def get_all_transcriptions():
    print('iniciando consulta')
    user_id = get_jwt_identity() 
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    db = setup_mongo_database()
    collection = db['transcriptions']
    print(f"Conectado à coleção: {collection.name}")
    offset = (page - 1) * per_page
    
    query = {}
    if not is_admin(user_id): 
        query['user_id'] = user_id
    
    transcriptions = list(collection.find(query).skip(offset).limit(per_page))

    for transcription in transcriptions:
        transcription['_id'] = str(transcription['_id'])
    
    return jsonify(transcriptions), 200

def is_admin(user_id):

    conect = setup_mysql_database()
    cursor = conect.cursor(dictionary=True)
    cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conect.close()
    
    return user and user['role'] == 'admin'

@jwt_required()
def get_transcription_id(transcription_id):
    try:
        obj_id = ObjectId(transcription_id)
    except:
        return jsonify({'message': 'ID inválido'}), 400

    db = setup_mongo_database()
    collection = db['transcriptions']

    user_id = get_jwt_identity()

    conect = setup_mysql_database()
    cursor = conect.cursor(dictionary=True)
    cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conect.close()

    if user and user['role'] == 'admin':
        transcription = collection.find_one({'_id': obj_id})
    else:
        transcription = collection.find_one({'_id': obj_id, 'user_id': user_id})

    if not transcription:
        return jsonify({'message': 'Acesso negado!'}), 404

    transcription['_id'] = str(transcription['_id'])
    return jsonify(transcription), 200

@jwt_required()
@role_required('admin')
def update_transcription(transcription_id):
    try:
        obj_id = ObjectId(transcription_id)
    except:
        return jsonify({'message': 'ID inválido'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Nenhum dado fornecido para atualização'}), 400
    
    db = setup_mongo_database()
    collection = db['transcriptions']
    
    update_data = {}
    if 'transcription' in data:
        update_data['transcription'] = data['transcription']
    if 'status' in data:
        update_data['status'] = data['status']
    
    if not update_data:
        return jsonify({'message': 'Nenhum campo válido para atualização'}), 400
    
    result = collection.update_one({'_id': obj_id}, {'$set': update_data})
    
    if result.modified_count == 0:
        return jsonify({'message': 'Nenhuma transcrição atualizada'}), 404
    
    return jsonify({'message': 'Transcrição atualizada com sucesso'}), 200


@jwt_required()
@role_required('admin')
def delete_transcription(transcription_id):
    try:
        obj_id = ObjectId(transcription_id)
    except:
        return jsonify({'message': 'ID inválido'}), 400
    
    db = setup_mongo_database()
    collection = db['transcriptions']
    
    result = collection.delete_one({'_id': obj_id})
    
    if result.deleted_count == 0:
        return jsonify({'message': 'Transcrição não encontrada'}), 404
    
    return jsonify({'message': 'Transcrição deletada com sucesso'}), 200

@jwt_required()
def search_transcriptions():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'message': 'Palavra-chave não fornecida'}), 400

    user_id = get_jwt_identity() 

    is_admin = check_if_admin(user_id)

    db = setup_mongo_database()
    collection = db['transcriptions']

    query = {'transcription': {'$regex': keyword, '$options': 'i'}}

    if not is_admin:
        query['user_id'] = user_id

    transcriptions = list(collection.find(query))

    if transcriptions == []:
        return jsonify({'message': 'Transcrição não encontrada'}), 404

    for transcription in transcriptions:
        transcription['_id'] = str(transcription['_id'])

    return jsonify(transcriptions), 200

#################### COLOCAR FUNÇÃO NO PERMISSIONS E AJUSTAR FUNÇÕES QUE VERIFIQUEM A ROLE
def check_if_admin(user_id):
    """
    Verifica se o usuário é um administrador.
    """
    conect = setup_mysql_database()
    cursor = conect.cursor(dictionary=True)
    cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conect.close()

    return user and user['role'] == 'admin'