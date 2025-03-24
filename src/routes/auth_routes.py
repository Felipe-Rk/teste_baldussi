from flask import Blueprint
from src.auth.auth_controller import login, register

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/register', methods=['POST'])(register)