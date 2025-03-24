from flask import Blueprint
from flasgger import swag_from
from src.auth.auth_controller import login, register

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Login do usuário',
    'description': 'Autentica um usuário com email e senha',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Login bem-sucedido'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Credenciais inválidas'}
    }
})
def login_route():
    return login()

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Registro de usuário',
    'description': 'Registra um novo usuário no sistema',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'cpf': {'type': 'string'},
                    'nome': {'type': 'string'},
                    'email': {'type': 'string'},
                    'senha': {'type': 'string'},
                    'role': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Usuário registrado com sucesso'},
        400: {'description': 'Dados inválidos'},
        409: {'description': 'Usuário já cadastrado'}
    }
})
def register_route():
    return register()