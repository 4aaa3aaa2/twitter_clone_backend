from flask import request, jsonify, Blueprint
from src.security.jwt_service import JwtService
from src.util.get_auth_user_id import GetAuthUserId

from src.domain.user.user import User
from src.domain.user.user_dto import UserDTO
from src.domain.user.user_service import UserService
from .follow import Follow
from .follow_repository import FollowRepository
from .new_follow import NewFollow
from .follow_service import FollowService

follow_bp = Blueprint("follow_bp", __name__, url_prefix="/api/follow")


follow_service = FollowService()
user_service = UserService()

class FollowController:

    @follow_bp.route("/follow", methods=["POST"])
    def create_follow():
        new_follow = request.get_json()
        followed_id = new_follow.get("followed_id")
        auth_user_id: int = GetAuthUserId.get_auth_user_id()

        try:
            followed_user_to_return: UserDTO = follow_service.add_new_follow(auth_user_id, followed_id)
            return jsonify(followed_user_to_return)
        except ValueError as e:
            return jsonify(error = str(e))
        