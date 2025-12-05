
from flask import request, jsonify
from src.security.jwt_service import JwtService as jwt_service
class GetAuthUserId:
    @staticmethod
    def get_auth_user_id():
        auth_header = request.headers.get('Authorization')
        print(f"Received Authorization header: {auth_header}")
        if not auth_header or not auth_header.startswith('Bearer '):
            raise ValueError("Missing or invalid Authorization header")

        token = auth_header.replace('Bearer ', '')
        if not jwt_service.is_token_valid(token):
            raise ValueError("Invalid token")

        try:
            user_id = jwt_service.extract_user_id(token)
        except Exception as e:
            raise ValueError(f"Failed to extract user ID: {str(e)}")

        return user_id