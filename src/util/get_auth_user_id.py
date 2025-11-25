
from flask import request, jsonify
from src.security.jwt_service import JwtService as jwt_service
class GetAuthUserId:
    @staticmethod
    def get_auth_user_id():
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise ValueError("Missing or invalid Authorization header")

        token = auth_header.replace('Bearer ', '')
        if not jwt_service.is_token_valid(token):
            raise ValueError("Invalid token")

        return jwt_service.extract_user_id(token)