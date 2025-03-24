import unicodedata
from bson import ObjectId
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from utils.permissions import role_required, check_if_admin
from src.database.mysql.mysql_config import get_mysql_connection
from src.database.mongo.mongo_config import setup_mongo_database
from src.transcription.transc_service import handle_transcription

SUPPORTED_FORMATS = ['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']

@jwt_required()
def transcribe():
    if 'file' not in request.files:
        print("❌ Nenhum arquivo encontrado.")
        return jsonify({'message': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    
    if file.filename == '':
        print("❌ Nome de arquivo invalido.")
        return jsonify({'message': 'Nome do arquivo inválido'}), 400

    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension not in SUPPORTED_FORMATS:
        return jsonify({'message': f'Formato não suportado. Suportados: {SUPPORTED_FORMATS}'}), 400

    file.seek(0)

    result = handle_transcription(file)

    if 'error' in result:
        return jsonify({'message': result['error']}), 500

    print("✅ Transcrição criada com sucesso!.")
    return jsonify({
        'message': result['message'],
        'transcription_id': result['transcription_id']
    }), 201


@jwt_required()
def get_all_transcriptions():
    print('🔹 Consultando todas transcrições...')

    user_id = get_jwt_identity() 
    page = max(request.args.get('page', default=1, type=int), 1)
    per_page = min(max(request.args.get('per_page', default=10, type=int), 1), 50)

    db = setup_mongo_database()
    collection = db['transcriptions']
    print(f"Conectado à coleção: {collection.name}")

    offset = (page - 1) * per_page

    query = {} if check_if_admin(user_id) else {'user_id': user_id}

    total = collection.count_documents(query)

    transcriptions = list(
        collection.find(query)
        .skip((page - 1) * per_page)
        .limit(per_page)
    )

    if not transcriptions:
        print("❌ Nenhum arquivo encontrado.")
        return jsonify({'message': 'Nenhuma transcrição encontrada'}), 404

    for transcription in transcriptions:
        transcription['_id'] = str(transcription['_id'])

    print(f"✅ Transcrições listadas! Total{total}.")
    return jsonify({
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total // per_page) + (1 if total % per_page > 0 else 0),
        'data': transcriptions
    }), 200

@jwt_required()
def get_transcription_id(transcription_id):

    print('🔹 Consultando transcrições por id...')
    try:
        obj_id = ObjectId(transcription_id)
    except:
        print("❌ Id invalido!.")
        return jsonify({'message': 'ID inválido'}), 400

    db = setup_mongo_database()
    collection = db['transcriptions']

    user_id = get_jwt_identity()

    conect = get_mysql_connection()()
    cursor = conect.cursor(dictionary=True)
    cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conect.close()

    query = {'_id': obj_id} if check_if_admin(user_id) else {'_id': obj_id, 'user_id': user_id}
    transcription = collection.find_one(query)

    if not transcription:
        print("❌ Acesso negado!.")
        return jsonify({'message': 'Acesso negado!'}), 404

    transcription['_id'] = str(transcription['_id'])
    print("✅ Transcrição encontrada!.")
    return jsonify(transcription), 200

@jwt_required()
@role_required('admin')
def update_transcription(transcription_id):

    print('🔹 Atualizando transcrição...')
    try:
        obj_id = ObjectId(transcription_id)
    except:
        print("❌ Id invalido.")
        return jsonify({'message': 'ID inválido'}), 400
    
    data = request.get_json()
    if not data:
        print("❌ Nenhum dado fornecido para atualização.")
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
        print("❌ Nenhuma transcvrição atualizada.")
        return jsonify({'message': 'Nenhuma transcrição atualizada'}), 404
    
    print("✅ Admin: Transcrição ataulizada com sucesso!.")
    return jsonify({'message': 'Transcrição atualizada com sucesso'}), 200


@jwt_required()
@role_required('admin')
def delete_transcription(transcription_id):

    print('🔹 Consultando transcrições...')
    try:
        obj_id = ObjectId(transcription_id)
    except:
        print("❌ Id invalido.")
        return jsonify({'message': 'ID inválido'}), 400
    
    db = setup_mongo_database()
    collection = db['transcriptions']
    
    result = collection.delete_one({'_id': obj_id})
    
    if result.deleted_count == 0:
        print("❌ Nenhuma transcrição encontrada.")
        return jsonify({'message': 'Transcrição não encontrada'}), 404
    
    print("✅ Admin: Transcrição deletada com sucesso!.")
    return jsonify({'message': 'Transcrição deletada com sucesso'}), 200

@jwt_required()
def search_transcriptions():
    print('🔹 Consultando transcrições por classificação ou palavra...')

    keyword = request.args.get('keyword')
    classification = request.args.get('classification')

    page = max(request.args.get('page', default=1, type=int), 1)
    per_page = min(max(request.args.get('per_page', default=10, type=int), 1), 50)

    if not keyword and not classification:
        print("❌ Informe uma classificação ou palavra.")
        return jsonify({'message': 'Informe uma palavra-chave ou uma classificação'}), 400

    user_id = get_jwt_identity() 
    is_admin = check_if_admin(user_id)

    db = setup_mongo_database()
    collection = db['transcriptions']

    query = {}

    def normalize_text(text):
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    if keyword and classification:
        # Se ambos forem fornecidos, busca por palavra dentro da classificação
        normalized_keyword = normalize_text(keyword)
        normalized_classification = normalize_text(classification)

        query['$and'] = [
            {'classification': {'$regex': normalized_classification, '$options': 'i'}},
            {'transcription': {'$regex': normalized_keyword, '$options': 'i'}}
        ]

    elif keyword:
        # Busca apenas pela palavra na transcrição
        normalized_keyword = normalize_text(keyword)
        query['transcription'] = {'$regex': normalized_keyword, '$options': 'i'}

    elif classification:
        # Busca apenas pela classificação
        normalized_classification = normalize_text(classification)
        query['classification'] = {'$regex': normalized_classification, '$options': 'i'}

    if not is_admin:
        print("❌ Usuário sem permissão para consulta.")
        query['user_id'] = user_id

    total = collection.count_documents(query)

    transcriptions = list(
        collection.find(query)
        .skip((page - 1) * per_page)
        .limit(per_page)
    )

    if not transcriptions:
        print("❌ Transcrição não encontrada.")
        return jsonify({'message': 'Transcrição não encontrada'}), 404

    for transcription in transcriptions:
        transcription['_id'] = str(transcription['_id'])

    print("✅ Transcrições listadas com sucesso.")
    return jsonify({
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total // per_page) + (1 if total % per_page > 0 else 0),
        'data': transcriptions
    }), 200