from flask import Blueprint
from src.user.user_controller import get_all_users, get_user, update_user, delete_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def get_all_users_route():
    return get_all_users()

@user_bp.route('/<user_id>', methods=['GET'])
def get_user_route(user_id):
    return get_user(user_id)

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user_route(user_id):
    return update_user(user_id)

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    return delete_user(user_id)
