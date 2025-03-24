from src.database.mysql.mysql_config import setup_mysql_database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

def auth_user(email, password):
    conect = setup_mysql_database()
    cursor = conect.cursor(dictionary = True)
    
    cursor.execute(" SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conect.close()

    if user and check_password_hash(user['senha'], password):
        return create_access_token(identity = str(user['id']))
    return None

def register_user(user_data):
    conect = setup_mysql_database()
    cursor = conect.cursor()

    hashed_password = generate_password_hash(user_data['senha'], method = 'pbkdf2:sha256')
    role = user_data.get('role', 'user')
    
    cursor.execute(
        "INSERT INTO users (cpf, nome, email, senha, role) VALUES (%s, %s, %s, %s, %s)",
        (user_data['cpf'], user_data['nome'], user_data['email'], hashed_password, role)
    )
    conect.commit()
    cursor.close()
    conect.close()
    return True