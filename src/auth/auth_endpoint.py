from flask import Blueprint
from .auth_controller import login, register

# Cria um Blueprint para autenticação
auth_bp = Blueprint('auth', __name__)

# Registra os endpoints de autenticação
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/register', methods=['POST'])(register)