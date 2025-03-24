# from flask import Blueprint
# from src.user.user_controller import get_all_users, get_user, update_user, delete_user

# user_bp = Blueprint('user', __name__)

# @user_bp.route('/', methods=['GET'])
# def get_all_users_route():
#     return get_all_users()

# @user_bp.route('/<user_id>', methods=['GET'])
# def get_user_route(user_id):
#     return get_user(user_id)

# @user_bp.route('/<user_id>', methods=['PUT'])
# def update_user_route(user_id):
#     return update_user(user_id)

# @user_bp.route('/<user_id>', methods=['DELETE'])
# def delete_user_route(user_id):
#     return delete_user(user_id)
from flask import Blueprint
from flasgger import swag_from
from src.user.user_controller import get_all_users, get_user, update_user, delete_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Listar todos os usuários',
    'responses': {
        200: {'description': 'Lista de usuários retornada com sucesso'},
        404: {'description': 'Nenhum usuário encontrado'}
    }
})

def get_all_users_route():
    return get_all_users()

@user_bp.route('/<user_id>', methods=['GET'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Obter usuário por ID',
    'responses': {
        200: {'description': 'Usuário encontrado'},
        404: {'description': 'Usuário não encontrado'}
    }
})
def get_user_route(user_id):
    return get_user(user_id)

@user_bp.route('/<user_id>', methods=['PUT'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Atualizar usuário',
    'responses': {
        200: {'description': 'Usuário atualizado com sucesso'},
        400: {'description': 'Falha ao atualizar usuário'}
    }
})
def update_user_route(user_id):
    return update_user(user_id)

@user_bp.route('/<user_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Deletar usuário',
    'responses': {
        200: {'description': 'Usuário deletado com sucesso'},
        400: {'description': 'Falha ao deletar usuário'}
    }
})
def delete_user_route(user_id):
    return delete_user(user_id)
