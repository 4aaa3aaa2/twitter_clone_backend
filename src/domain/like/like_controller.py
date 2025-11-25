
from flask import request, jsonify, Blueprint
from src.security.jwt_service import JwtService
from src.util.get_auth_user_id import GetAuthUserId

from src.domain.post.post import Post
from src.domain.post.post_dto import PostDTO 
from .like import Like
from .like_repository import LikeRepository
from .like_service import LikeService
from .new_like import NewLike

like_bp = Blueprint("like_bp",__name__, url_prefix="/api/likes")

like_service = LikeService()

class LikeController:

    @like_bp.route("/create",methods=["POST"])
    def create_like(self):
        new_like = request.get_json()
        auth_user_id: int = GetAuthUserId.get_auth_user_id()
        liked_post_id: int = new_like.get("liked_post_id")

        try:
            post_to_return: PostDTO = like_service.add_new_like(auth_user_id, liked_post_id)
            return jsonify(post_to_return)
        except ValueError as e:
            return jsonify(str(e))

    @like_bp.route("/delete", methods=["POST"])
    def remove_like(self):
        new_like = request.get_json()
        auth_user_id: int = GetAuthUserId.get_auth_user_id()
        liked_post_id: int = new_like.get("liked_post_id")
        try:
            post_to_return = like_service.delete_like(auth_user_id,liked_post_id)
            return jsonify(post_to_return)
        except ValueError as e:
            return jsonify(str(e))
