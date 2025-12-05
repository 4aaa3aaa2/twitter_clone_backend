# src/security/jwt_middleware.py
'''
from flask import request, g, jsonify,Flask
from functools import wraps
from .jwt_service import JwtService
from typing import Optional

jwt_service = JwtService()

class JwtAuthMiddleware:
    def __init__(self, app):
        self.app = app
        self.register_middleware(app)

    def register_middleware(self):
        @self.app.before_request
        def check_jwt_token():
            print("JWT middleware triggered")  # 每个请求都会打印
            auth_header: Optional[str] = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                # 不阻止请求，只是没有认证信息
                print("No Authorization header or invalid format")
                g.current_user_id = None
                return None

            token = auth_header[7:]
            if not jwt_service.is_token_valid(token):
                print("Invalid JWT token")
                g.current_user_id = None
                return None

            user_id: Optional[int] = jwt_service.extract_user_id(token)
            if user_id is None:
                print("Invalid token payload")
                g.current_user_id = None
                return None

            # JWT 有效，存储 user_id
            g.current_user_id = user_id
            print(f"Authenticated user_id: {user_id}")
            return None
        




'''
from flask import Flask, request, g, jsonify
from functools import wraps
import jwt
from .jwt_service import JwtService

SECRET_KEY = "my-test-secret"

class JwtAuthMiddleware:
    def register_middleware(self, app: Flask):
        @app.before_request
        def check_jwt_token():
            auth_header = request.headers.get("Authorization")
            print("Received Authorization header:", auth_header)
            print("---------*********————————————")

            if request.method == "OPTIONS":
            # 直接跳过 OPTIONS 预检请求
                return None
            
            print("JWT middleware triggered")
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                print("No Authorization header or invalid format")
                g.current_user_id = None
                return None

            token = auth_header[7:]
            if not JwtService.is_token_valid(token):
                print("Token invalid")
                return jsonify({"error": "Invalid or expired token"}), 401

            g.current_user_id = JwtService.extract_user_id(token)
            print("Authenticated user_id:", g.current_user_id)
            return None