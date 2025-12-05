from flask import   request, jsonify, Blueprint
from typing import List

from .user_service import UserService
from .user_repository import UserRepository

user_bp = Blueprint("user_bp",__name__, url_prefix="/api/users")
#initialize the imported models

user_service = UserService()
user_repository = UserRepository()

class UserController:

    @user_bp.route('/get-user', methods=['GET'])
    def get_user_by_id():
        user_id = request.args.get('id', type=int)
        #return jsonify(f"id got {user_id}")
        if user_id is None:
            return jsonify({"error": "Missing id parameter"}), 400
        result  = UserService.generate_user_dto_by_user_id(id=user_id)
        if result == None:
            return jsonify({"message":f"user with id {user_id} not exist"})
        return jsonify(result)
        

    @user_bp.route('/get-users', methods=['POST'])
    def get_users():
        ids = request.json
        if not isinstance(ids, list):
            return jsonify({"error": "Expected a JSON list of IDs"}), 400
        result = user_service.find_all_user_dto_by_ids(ids)
        return jsonify(result)

    @user_bp.route('/get-top-five', methods=['GET'])
    def get_top_five_users():
        # The Java code uses a large follower count threshold and limit 4
        result = user_repository.find_user_ids_by_follower_count(99999, 4)
        return jsonify(result)

    @user_bp.route('/get-admin-user', methods=['GET'])
    def get_admin_user():
        user_id = request.args.get('id', type=int)
        if user_id is None:
            return jsonify({"error": "Missing id parameter"}), 400
        print(f"Booyah {user_id}")
        user_service.generate_feed(user_id)
        result = user_service.generate_user_dto_by_user_id(user_id)
        return jsonify(result)

    @user_bp.route('/search', methods=['GET'])
    def search_users():
        query = request.args.get('q', default="")
        result = user_service.search_users_by_name(query)
        return jsonify(result)

    @user_bp.route('/get-discover', methods=['GET'])
    def get_feed_page():
        cursor = request.args.get('cursor', default=0, type=int)
        limit = request.args.get('limit', default=10, type=int)
        print(f"Received request for cursor: {cursor} limit {limit}")
        result = user_service.get_paginated_top_users(cursor, limit)
        return jsonify(result)