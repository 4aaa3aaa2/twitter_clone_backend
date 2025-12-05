from flask import request, jsonify
from functools import wraps
from .jwt_service import JwtService
jwt_service = JwtService()

class SecurityConfig:
    

    @staticmethod
    def security_filter_chain():
        """
        相当于 Spring SecurityFilterChain。
        - 禁用 CSRF（Flask 默认不启用 CSRF）
        - 放行 /api/auth/** 和 /api/posts/delete
        - 其他请求也允许访问（permitAll）
        - 添加 JWT 过滤器
        """
        def jwt_auth_filter():
            path = request.path

            # 放行无需验证的路径
            if path.startswith("/api/auth/") or path == "/api/posts/delete":
                return None

            # 获取 Authorization Header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None  # 原配置 permitAll，不强制认证

            token = auth_header.split(" ")[1]

            try:
                request.user = jwt_service.verify_token(token)
            except Exception:
                return jsonify({"error": "Invalid token"}), 401

        return jwt_auth_filter()