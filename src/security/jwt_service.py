import jwt
from datetime import datetime, timedelta
from flask import current_app

expiration_min = 60*24

class JwtService:

    @staticmethod
    def get_secret_key():
        return current_app.config.get("JWT_SECRET", "your-default-jwt-secret")
    @staticmethod
    def create_token( user_id: int)-> str:
        now = datetime.now()
        exp = now + timedelta(minutes= expiration_min)
        payload = {"sub": str(user_id), "iat": now, "exp": exp}

        token = jwt.encode(payload, JwtService.get_secret_key(), algorithm="HS256")
        return token if isinstance(token, str) else token.decode("utf-8")
    @staticmethod
    def is_token_valid( token:str)->bool:
        try: 
            jwt.decode(token, JwtService.get_secret_key, algorithms=["HS256"])
            return True
        except jwt.PyJWTError:
            return False
    @staticmethod
    def extract_user_id( token: str)-> int:
        try:
            decoded = jwt.decode(token, JwtService.get_secret_key(), algorithms=["HS256"])
            return int(decoded.get("sub"))
        except jwt.PyJWTError:
            return None

