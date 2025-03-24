from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.permissions import role_required, check_if_admin
from user.user_service import get_user_id, get_users, delete_user_service, update_user_service


@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()

    if current_user_id == user_id or check_if_admin(current_user_id):
        user = get_user_id(user_id)
        if user:
            print('🔹 Consultando usuario por id...')
            return jsonify(user), 200
        
        print("❌ Nenhum usuario encontrando.")
        return jsonify({'message': 'Usuário não encontrado!'}), 404
    
    print("❌ Acesso negado!.")
    return jsonify({'message': 'Acesso negado!'}), 403

@jwt_required()
def get_all_users():
    current_user_id = get_jwt_identity()
    print('🔹 Consultando todos os usuários...')

    if check_if_admin(current_user_id):
        page = max(request.args.get('page', default=1, type=int), 1)
        per_page = min(max(request.args.get('per_page', default=10, type=int), 1), 50)
        
        # 🔹 Verifique se a função `get_users()` está buscando TODOS os usuários
        users, total = get_users(page, per_page, admin=True)  # Passamos admin=True

        if not users:
            print("❌ Nenhum usuário encontrado.")
            return jsonify({'message': 'Nenhum usuário encontrado'}), 404
        
        print("✅ Admin: Usuários listados com sucesso!.")
        return jsonify({
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total // per_page) + (1 if total % per_page > 0 else 0),
            'data': users
        }), 200
    else:
        # Usuário comum vê apenas seus próprios dados
        user = get_user_id(current_user_id)
        print('🔹 Consultando dados do usuário...')
        if user:
            print("✅ User: Usuário listado com sucesso!.")
            return jsonify(user), 200
        return jsonify({'message': 'Usuário não encontrado'}), 404

@jwt_required()
@role_required('admin')
def update_user(user_id):
    current_user_id = get_jwt_identity()
    print(f'🔹 Atualizando usuario id:{user_id} ...')
    if current_user_id != user_id and not check_if_admin(current_user_id):
        print("❌ Acesso negado!.")
        return jsonify({'message': 'Acesso negado!'}), 403

    updates = request.get_json()
    if update_user_service(user_id, updates):
        print("✅ Admin: Usuarios atualizado com sucesso!.")
        return jsonify({'message': 'Usuário atualizado com sucesso!'}), 200
    print("❌ Falha ao atualizar usuario!.")
    return jsonify({'message': 'Falha ao atualizar usuário'}), 400

@jwt_required()
@role_required('admin')
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    print('🔹 Consultando usuario...')
    if current_user_id != user_id and not check_if_admin(current_user_id):
        print("❌ Acesso negado!.")
        return jsonify({'message': 'Acesso negado!'}), 403

    if delete_user_service(user_id):
        print("✅ Admin: Usuario deletado com sucesso!.")
        return jsonify({'message': 'Usuário deletado com sucesso!'}), 200
    
    print("❌ Erro ao deletar usuario!.")
    return jsonify({'message': 'Falha ao deletar usuário!'}), 400
