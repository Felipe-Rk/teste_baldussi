from flask import request, jsonify
from flask_jwt_extended import jwt_required
from auth.permissions import role_required
from user.user_service import get_user_id, get_users, delete_user_service, update_user_service


@jwt_required()
@role_required('admin')
def get_all_users():
    users = get_users()
    return jsonify(users), 200

@jwt_required()
def get_user(user_id):
    user = get_user_id(user_id)
    if user:
        return jsonify(user), 200
    return ({'message': 'Usuário não encontrado!'}), 404

@jwt_required()
@role_required('admin')
def update_user(user_id):
    updates = request.get_json()
    if update_user_service(user_id, updates):
        return jsonify({'message': 'Usuário atualizado com sucesso!'}), 200
    return jsonify({'message': 'Falha ao atualizar usuário'}), 400

@jwt_required()
def delete_user(user_id):
    if delete_user_service(user_id):
        return jsonify({'message': 'Usuário deletado com sucesso!'}), 200
    return jsonify({'message': 'Falha ao deletar usuário!'}), 400
