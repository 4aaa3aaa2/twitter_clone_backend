#from src.domain.user.user import User
#from src.domain.user.user_dto import UserDTO
from src.domain.user.user_service import UserService
from src.domain.user.user_repository import UserRepository
from src.security.jwt_service import JwtService
from .auth_service import AuthService

from flask import request, jsonify, Blueprint
#from twitter_clone_app import app
from typing import Optional
from werkzeug.datastructures import FileStorage

auth_bp = Blueprint("auth_bp",__name__, url_prefix="/api/auth")

auth_service = AuthService()
user_service = UserService()
jwt_service = JwtService()
user_repository = UserRepository()

class AuthController:

    @auth_bp.route("/google-login", methods=["POST"])
    def authenticate_with_google():
        from src.domain.user.user_dto import UserDTO
        from src.domain.user.user import User
        print("request from google login",request)
        body: dict[str:str] = request.get_json()
        access_token: Optional[str] = body.get("token")
        #return jsonify({"token": access_token})
        print(f"Access Token: {access_token}")
        print(" ")
        authenticated_user: User = auth_service.authenicate_google_user(access_token)

        if authenticated_user:
            dto_to_return = user_service.generate_user_dto_by_user_id(authenticated_user.id)
            token = jwt_service.create_token(dto_to_return.id)  # Create JWT token
            return jsonify({"token": token, "user": dto_to_return})  # Respond with token and user data
        else:
            return jsonify({"error": "User authentication failed"}), 400
    
    @auth_bp.route("/test-login", methods=["POST"])
    def test_login():
        body = request.get_json()
        email = body.get("email")

        if not email or email==" ":
            return jsonify({"error": "Missing email"}), 400

        user = user_repository.find_by_email(email)
        if not user:
            user = auth_service.create_test_user(email)
        print(f"test user id {user.id}")

        dto = user_service.generate_user_dto_by_user_id(user.id)
        token = jwt_service.create_token(dto.id)

        return jsonify({"token": token, "user": dto})


    @auth_bp.route("/update-profile", methods=["POST"])
    def update_profile():
        profile_picture: Optional[FileStorage] = request.files.get("profile_picture")
        banner_image: Optional[FileStorage] = request.files.get("banner_image")
        display_name: str = request.form.get("display_name","")
        username: str = request.form.get("username","")
        bio: str = request.form.get("bio","")

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify(error="Missing or invalid Authorization header"), 401
        token = auth_header.replace('Bearer ', '')
        if not jwt_service.is_token_valid(token):
            return jsonify(error="Invalid token"), 401
        auth_user_id = jwt_service.extract_user_id(token)

        print(f"authenticating user {auth_user_id}")
        user_service.update_user_profile(auth_user_id,profile_picture,banner_image,display_name,username, bio)

        new_user_dto = user_service.generate_user_dto_by_user_id(auth_user_id)
        return jsonify(new_user_dto)
    

    @auth_bp.route("/me", methods=["GET"])
    def get_authenticated_user():
        from src.domain.user.user_dto import UserDTO
        print("~~~~~~~")
        print("/me API called")
        print("~~~~~~~")
        print("request from /me:" ,request)
        print("~~~~~~~")
        auth_header: str = request.headers.get("Authorization")
        print("auth header from /me request:", auth_header)
        print("~~~~~~~")
        if not auth_header or not auth_header.startswith("Bearer"):
            return jsonify(error="missing or invalid authorization header"),401
        #token: str = auth_header.replace("Bearer", "")
        token = auth_header.split(" ")[1]
        user_id = JwtService.extract_user_id(token)
        print("user_id from token:", user_id)
        user = user_repository.find_by_id(user_id)
        print("user from db:", user)

        if not jwt_service.is_token_valid(token):
            return jsonify(error = "invalid token"),401
        
        user_id: int = jwt_service.extract_user_id(token)
        dto: UserDTO = user_service.generate_user_dto_by_user_id(user_id)

        return jsonify(dto)
    
    @auth_bp.route("/demo-signup", methods=["POST"])
    def authenticate_with_temp_signup():
        from src.domain.user.user_dto import UserDTO
        from src.domain.user.user import User
        new_temp_user: User = auth_service.register_temp_user()
        dto_to_return: UserDTO = user_service.generate_user_dto_by_user_id(new_temp_user.id)
        token: str = jwt_service.create_token(new_temp_user.id)
        return jsonify(token=token,user=dto_to_return)
    

    
    @auth_bp.route("/mock-login")
    def mock_login():
        import jwt
        # 给前端一个测试 token
        token = jwt.encode({"user_id": 42}, "my-test-secret", algorithm="HS256")
        return jsonify({"token": token})


        
