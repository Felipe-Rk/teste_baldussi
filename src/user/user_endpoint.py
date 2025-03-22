from flask import Blueprint
from .user_controller import get_all_users, get_user, update_user, delete_user

user_bp = Blueprint('user', __name__)

user_bp.route('/users', methods=['GET'])(get_all_users)
user_bp.route('/users/<int:user_id>', methods=['GET'])(get_user)
user_bp.route('/users/<int:user_id>', methods=['PUT'])(update_user)
user_bp.route('/users/<int:user_id>', methods=['DELETE'])(delete_user)