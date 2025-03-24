from auth.auth_service import auth_user, register_user
from flask import request, jsonify


def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email e senha são obrigatórios'}), 400

    token = auth_user(email, password)
    if token:
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Credenciais invalidas'}), 401

def register():
    data = request.get_json()

    if not data.get('cpf') or not data.get('nome') or not ('email') or not data.get('senha'):
        return jsonify({'message': 'Todos os campos são obrigatórios'}), 400

    if register_user(data):
        return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

    return jsonify({'message': 'Falha ao registrar usuário'}), 400