from src.domain.post.post_dto import PostDTO
from src.domain.post.post import Post
from .bookmark import Bookmark
from .new_bookmark import NewBookmark
from .bookmark_service import BookmarkService
from src.util.get_auth_user_id import GetAuthUserId


from flask import request, jsonify, Blueprint

from src.security.jwt_service import JwtService

bookmark_bp = Blueprint("bookmark_bp", __name__, url_prefix="/api/bookmarks")

bookmark_service = BookmarkService()
jwt_service = JwtService()

class BookmarkController:

    @bookmark_bp.route("/create", methods=["POST"])
    def create_bookmark(self):
        body: dict[str:str] = request.get_json()
        new_bookmark_post: int = body.get("bookmarked_post")

        auth_user_id = GetAuthUserId.get_auth_user_id()

        try:
            bookmark_to_return: PostDTO = self.bookmark_service.add_new_bookmark(auth_user_id,new_bookmark_post)
            return jsonify(bookmark_to_return)
        
        except ValueError as e:
            return jsonify(error=str(e)+"errors in creating bookmark"), 409
    

    @bookmark_bp.route("/delete", methods=["POST"])
    def delete_bookmark(self):
        body: dict[str:str] = request.get_json()
        new_bookmark_post: int = body.get("bookmarked_post")

        auth_user_id: int = GetAuthUserId.get_auth_user_id()
        result: PostDTO = self.bookmark_service.delete_bookmark(auth_user_id, new_bookmark_post)
        return jsonify(result)




 