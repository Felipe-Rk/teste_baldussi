from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from src.database.mysql.mysql_config import setup_mysql_database


def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            conect = setup_mysql_database()
            cursor = conect.cursor(dictionary = True)
            cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            conect.close()

            if user and user['role'] == required_role:
                return f(*args, **kwargs)
            return jsonify({'message': 'Acesso negado!'}), 403
        return wrapper
    return decorator