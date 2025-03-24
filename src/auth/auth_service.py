from src.database.mysql.mysql_config import get_mysql_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from mysql.connector import IntegrityError
from flask import jsonify

def auth_user(email, password):
    conect = get_mysql_connection()
    cursor = conect.cursor(dictionary = True)
    
    cursor.execute(" SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conect.close()

    if user and check_password_hash(user['senha'], password):
        return create_access_token(identity = str(user['id']))
    return None

def register_user(user_data):
    conect = get_mysql_connection()
    cursor = conect.cursor(dictionary=True)

    # Verifica se já existe um usuário com o mesmo nome ou e-mail
    cursor.execute("SELECT * FROM users WHERE nome = %s OR email = %s", (user_data['nome'], user_data['email']))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conect.close()
        return jsonify({"message": "Nome ou e-mail já estão cadastrados."}), 409  # Código HTTP 409 - Conflito

    hashed_password = generate_password_hash(user_data['senha'], method='pbkdf2:sha256')
    role = user_data.get('role', 'user')

    try:
        cursor.execute(
            "INSERT INTO users (cpf, nome, email, senha, role) VALUES (%s, %s, %s, %s, %s)",
            (user_data['cpf'], user_data['nome'], user_data['email'], hashed_password, role)
        )
        conect.commit()
        return jsonify({"message": "Usuário registrado com sucesso!"}), 201  # Código HTTP 201 - Criado
    except IntegrityError as e:
        conect.rollback()
        return jsonify({"message": "Erro ao registrar usuário: " + str(e)}), 500  # Código HTTP 500 - Erro do servidor
    finally:
        cursor.close()
        conect.close()