import jwt
from datetime import datetime, timedelta,timezone
from flask import current_app

expiration_min = 60*24

class JwtService:

    @staticmethod
    def get_secret_key():
        print("loaded SECRET:",current_app.config.get("JWT_SECRET", "your-default-jwt-secret"))
        return current_app.config.get("JWT_SECRET", "your-default-jwt-secret")
    
    @staticmethod
    def create_token( user_id: int)-> str:
        print("crating a token")
        now = datetime.now(timezone.utc)
        print("see current time", now.timestamp())
        exp = now + timedelta(minutes= expiration_min)
        payload = {"sub": str(user_id), "iat": now.timestamp(), "exp": exp.timestamp()}

        token = jwt.encode(payload, JwtService.get_secret_key(), algorithm="HS512")
        print("token generated", str(token))
        return token if isinstance(token, str) else token.decode("utf-8")
    
    @staticmethod
    def is_token_valid(token: str) -> bool:
        print("Checking token validity:", token)
        try:
            # 打印 token header
            header = jwt.get_unverified_header(token)
            print("JWT header:", header)
            payload = jwt.decode(token,algorithms=["HS512"], options={"verify_signature": False})
            print("UNVERIFIED PAYLOAD:", payload)
            # 尝试 decode
            decoded = jwt.decode(token, JwtService.get_secret_key(), algorithms=["HS512"])
            print("JWT payload:", decoded)
            return True
        except jwt.ExpiredSignatureError:
            print("Token expired")
            return False
        except jwt.InvalidTokenError as e:
            print("Invalid token error:", e)
            return False

    @staticmethod
    def extract_user_id( token: str)-> int:
        print("extract user id get token", token)
        print(".............")
        try:
            decoded = jwt.decode(token, JwtService.get_secret_key(), algorithms=["HS512"])
            return int(decoded.get("sub"))
        except jwt.PyJWTError:
            return None

