from auth.auth_service import auth_user, register_user
from flask import request, jsonify


def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    token = auth_user(email, password)

    if token:
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Credenciais invalidas'}), 401

def register():
    data = request.get_json()
    if register_user(data):
        return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

    return jsonify({'message': 'Falha ao registrar usuário'}), 400