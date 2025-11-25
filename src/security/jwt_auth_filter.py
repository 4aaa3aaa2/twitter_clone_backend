from flask import Flask, request, g, jsonify
from functools import wraps
from .jwt_service import JwtService
from typing import Optional

app = Flask()
jwt_service = JwtService()

class JwtAuthMiddleWare:

    def register_middleware(self):
        @app.before_request
        def check_jwt_token():
            auth_header: Optional[str] = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer"):
                return None
            
            token: str = auth_header[7:]

            if not jwt_service.is_token_valid(token):
                return jsonify({"error": "Invalid or expired token"}), 401

            user_id: Optional[int] = jwt_service.extract_user_id(token)
            if user_id is None:
                return jsonify({"error": "Invalid token payload"}), 401

            g.current_user_id = user_id
            return None  # request continues          